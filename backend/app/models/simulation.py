# Modelos de Dados para Simulações de Corridas

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, String, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
from typing import Dict, List, Any


class Simulation(Base):
    
    __tablename__ = "Simulations"
    
    id = Column(Integer, primary_key=True, index=True)
    
    strategy_id = Column(Integer, ForeignKey("strategies.id"), nullable=False)
    
    simulation_speed = Column(Float, default=1.0)
    randon_seed = Column(Integer)

    track_temperature = Column(Float, default=25.0)
    air_temperature = Column(Float, default=20.0)
    weather_condition = Column(String(20), default="dry")
    
    safety_car_laps = Column(JSON)
    virtual_safety_car_laps = Column(JSON)
    incidents = Column(JSON)
    
    lap_times = Column(JSON)
    tire_ages = Column(JSON)
    tire_compounds = Column(JSON)
    tire_degradation_data = Column(JSON)
    fuel_loads = Column(JSON)
    positions = Column(JSON)
    
    # Telemetria de Dados
    sector_times = Column(JSON) 
    speed_trap = Column(JSON)
    
    total_race_time = Column(Float)
    total_race_time_formatted = Column(String(20))
    average_lap_time = Column(Float)
    fastest_lap_time = Column(Float)
    fastest_lap_number = Column(Integer)
    slowest_lap_time = Column(Float)
    
    total_tire_life = Column(JSON)
    compounds_used = Column(JSON)
    
    total_distance = Column(Float)
    average_speed = Column(Float)
    fuel_efficiency = Column(Float)
    
    is_completed = Column(Boolean, default=False)
    completed_laps = Column(Integer, default=0)
    status = Column(String(20), default="pending")
    
    # Comparação de diferentes simulações
    comparison_group_id = Column(String(50))
    
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    strategy = relationship("Strategy", back_populates="simulations")
    
    
    def __repr__(self):
        return f"<Simulation(id={self.id}, strategy_id={self.strategy_id}, status='{self.status}')>"
    
    
    def add_lap_data(
        self, 
        lap: int, 
        lap_time: float, 
        tire_age: int, 
        tire_compound: str, 
        degradation: float, 
        fuel_load: float
    ):
        # Adiciona os dados de uma volta à simulação
        
        if not self.lap_times:
            self.lap_times = []
        if not self.tire_ages:
            self.tire_ages = []
        if not self.tire_compounds:
            self.tire_compounds = []
        if not self.tire_degradation_data:
            self.tire_degradation_data = []
        if not self.fuel_loads:
            self.fuel_loads = []
            
        self.lap_times.append(lap_time)
        self.tire_ages.append(tire_age)
        self.tire_compounds.append(tire_compound)
        self.tire_degradation_data.append(degradation)
        self.fuel_loads.append(fuel_load)
        
        self.completed_laps = lap
        
    
    def add_safety_car(self, lap: int, duration: int = 3):
        
        if not self.safety_car_laps:
            self.safety_car_laps = []
            
        self.safety_car_laps.append({
            "start_lap": lap,
            "duration": duration   
        })
        
    
    def get_lap_time(self, lap: int) -> float:
        
        if self.lap_times and 0 <= lap - 1 < len(self.lap_times):
            return self.lap_times[lap - 1]
        return 0.0
    
    
    def calculate_statistics(self):
        
        # Chamado após a simulação ser concluída para calcular as estatísticas finais
        
        if not self.lap_times or len(self.lap_times) == 0:
            return
        
        self.total_race_time = sum(self.lap_times)
        
        hours = int(self.total_race_time // 3600)
        minutes = int((self.total_race_time % 3600) // 60)
        seconds = self.total_race_time % 60
        self.total_race_time_formatted = f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"
        
        self.average_lap_time = sum(self.lap_times) / len(self.lap_times)
        
        self.fastest_lap_time = min(self.lap_times)
        self.fastest_lap_number = self.lap_times.index(self.fastest_lap_time) + 1
        self.slowest_lap_time = max(self.lap_times)
        
        if self.total_distance and self.total_race_time:
            self.average_speed = (self.total_distance / self.total_race_time) * 3600
            
        if self.fuel_loads and len(self.fuel_loads) >= 2:
            fuel_used = self.fuel_loads[0] - self.fuel_loads[-1]
            if fuel_used > 0:
                self.fuel_efficiency = self.total_distance / fuel_used
                
        
    def to_dict(self, include_telemetry: bool = False) -> Dict[str, Any]:
        
        base_dict = {
            "id": self.id,
            "strategy_id": self.strategy_id,
            "simulation_speed": self.simulation_speed,
            "track_temperature": self.track_temperature,
            "air_temperature": self.air_temperature,
            "weather_condition": self.weather_condition,
            "total_race_time": self.total_race_time,
            "total_race_time_formatted": self.total_race_time_formatted,
            "average_lap_time": self.average_lap_time,
            "fastest_lap_time": self.fastest_lap_time,
            "fastest_lap_number": self.fastest_lap_number,
            "average_speed": self.average_speed,
            "completed_laps": self.completed_laps,
            "status": self.status,
            "is_completed": self.is_completed,
        }
        
        if include_telemetry:
            base_dict.update({
                "lap_times": self.lap_times,
                "tire_ages": self.tire_ages,
                "tire_compounds": self.tire_compounds,
                "tire_degradation_data": self.tire_degradation_data,
                "fuel_loads": self.fuel_loads,
                "safety_car_laps": self.safety_car_laps,
                "incidents": self.incidents,
            })
            
        return base_dict