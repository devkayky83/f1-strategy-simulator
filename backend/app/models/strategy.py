# Módelo de Dados para Estratégias de Corrida

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
from typing import Dict, List, Any


class Strategy(Base):
    # Representa uma estratégia de corrida criada pelo usuário
    
    __tablename__ = "strategies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    
    circuit_id = Column(Integer, ForeignKey("circuits.id"), nullable=False)
    
    total_pit_stops = Column(Integer, nullable=False)
    strategy_data = Column(JSON)
    
    final_time = Column(Float)
    total_race_time = Column(String(20))
    average_lap_time = Column(Float)
    fastest_lap = Column(Float)
    slowest_lap = Column(Float)
    
    total_tire_changes = Column(Integer)
    total_pit_time = Column(Float)
    fuel_used = Column(Float)
    
    is_completed = Column(Integer, default=False)
    is_optimal = Column(Integer, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    circuit = relationship("Circuit", back_populates="strategies")
    pit_stops = relationship("PitStop", back_populates="strategy", cascade="all, delete-orphan")
    simulations = relationship("Simulation", back_populates="strategy", cascade="all, delete-orphan")
    
    
    def __repr__(self):
        return f"<Strategy(name='{self.name}', circuit='{self.circuit.name if self.circuit else 'N/A'}')>"
    
    
    def add_pit_stop(self, lap: int, compound_name: str, duration: float = 2.5) -> Dict:
        # Adiciona um pit stop à estratégia
        
        if not self.strategy_data:
            self.strategy_data = {"pit_stops": []}
            
        pit_stop = {
            "lap": lap,
            "compound": compound_name, 
            "duration": duration,
            "tire_age_at_stop": 0, # Cálculado na simulação
        }
        
        self.strategy_data["pit_stops"].append(pit_stop)
        self.total_pit_stops = len(self.strategy_data["pit_stops"])
        
        return pit_stop
    
    
    def get_tire_compound_at_lap(self, lap: int) -> str:
        # Retorna qual composto de pneu está sendo usado em uma determinada volta
        
        if not self.strategy_data or "pit_stops" not in self.strategy_data:
            return "C3" # Composto padrão
        
        pit_stops = sorted(self.strategy_data["pit_stops"], key=lambda x: x["lap"])
        
        current_compound = pit_stops[0]["compound"] if pit_stops else "C3"
        
        for pit_stop in pit_stops:
            if lap >= pit_stop["lap"]:
                current_compound = pit_stop["compound"]
        
        return current_compound
    
    
    def validate_strategy(self, total_laps: int) -> tuple[bool, List[str]]:
        # Validação através das regras da F1
        
        errors = []
        
        if not self.strategy_data or "pit_stops" not in self.strategy_data:
            errors.append("Estrátegia deve ter pelo menos um pit stop.")
            return False, errors
        
        pit_stops = self.strategy_data["pit_stops"]
        
        if len(pit_stops) < 1:
            errors.append("Estratégia deve ter pelo menos um pit stop.")
            
        for pit_stop in pit_stops:
            if pit_stop["lap"] < 1 or pit_stop["lap"] > total_laps:
                errors.append(f"Pit Stop na volta {pit_stop["lap"]} está fora do intevalo permitido (1-{total_laps}).")
                
        laps = [pit_stop["lap"] for pit_stop in pit_stops]
        if len(laps) != len(set(laps)):
            errors.append("Não pode haver dois pit stops ou mais na mesma volta.")
            
        compounds = set([pit_stop["compound"] for pit_stop in pit_stops])
        if len(compounds) < 2:
            errors.append("Estratégia deve incluir pelo menos dois compostos de pneus diferentes.")
            
        return len(errors) == 0, errors
    
    
    def calculate_total_pit_time(self, circuit_pit_loss: float) -> float:
        # Calcula o tempo total perdido nos pit stops

        if not self.strategy_data or "pit_stops" not in self.strategy_data:
            return 0.0
        
        total = 0.0
        for pit_stop in self.strategy_data["pit_stops"]:
            total += pit_stop.get("duration", 2.5) + circuit_pit_loss
            
        return total
    
    
    def to_dict(self) -> Dict[str, Any]:
        
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "circuit_id": self.circuit_id,
            "circuit_name": self.circuit.name if self.circuit else None,
            "total_pit_stops": self.total_pit_stops,
            "strategy_data": self.strategy_data,
            "final_time": self.final_time,
            "total_race_time": self.total_race_time,
            "average_lap_time": self.average_lap_time,
            "fastest_lap": self.fastest_lap,
            "slowest_lap": self.slowest_lap,
            "total_tire_changes": self.total_tire_changes,
            "total_pit_time": self.total_pit_time,
            "fuel_used": self.fuel_used,
            "is_completed": self.is_completed,
            "is_optimal": self.is_optimal,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }