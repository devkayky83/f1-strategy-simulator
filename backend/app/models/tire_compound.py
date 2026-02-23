# Models de Dados para Compostos de Pneus de F1

from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base

class TireCompound(Base):
    __tablename__ = "tire_compounds"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), nullable=False, unique=True)
    display_name = Column(String(50))
    
    base_grip = Column(Float, nullable=False)
    degradation_rate = Column(Float, nullable=False)
    optimal_life = Column(Integer, nullable=False)
    
    optimal_temp_min = Column(Float, default=80.0)
    optimal_temp_max = Column(Float, default=110.0)
    working_range_min = Column(Float, default=70.0)
    working_range_max = Column(Float, default=120.0)
    
    color_code = Column(String(7))
    color_name = Column(String(20))
    
    weight = Column(Float)
    construction = Column(String(50))
    
    # Cliff-effect (Quando o pneu "cai de performance")
    cliff_lap = Column(Integer)
    cliff_factor = Column(Float, default=0.5)
    
    warm_up_laps = Column(Integer, default=1)
    warm_up_penalty = Column(Float, default=0.5)
    
    dry_performance = Column(Float, default=1.0)
    wet_performance = Column(Float, default=0.0)
    
    description = Column(Text)
    typical_usage = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    
    def __repr__(self):
        return f"<TireCompound(name='{self.name}', display_name='{self.display_name}')>"
    
    
    def calculate_degradation(self, lap: int, track_factor: float = 1.0) -> float:
        # Calcula a degradação do pneu com base na volta atual e um fator de pista
        
        base_degradation = self.degradation_rate * lap * track_factor
        
        # Aplica o efeito cliff se o pneu passou da vida útil
        if lap > self.cliff_lap:
            laps_over_cliff = lap - self.cliff_lap
            cliff_degradation = self.degradation_rate * laps_over_cliff * self.cliff_factor * track_factor
            return base_degradation + cliff_degradation
        
        return base_degradation
    
    
    def is_suitable_for_conditions(self, temperature: float, is_wet: bool) -> bool:
        # Verifica se o composto de pneu é adequado para as condições de temperatura e pista
        
        if is_wet and self.wet_performance <= 0.5:
            return False
        
        if not is_wet and self.dry_performance <= 0.5:
            return False
        
        if temperature < self.working_range_min or temperature > self.working_range_max:
            return False
        
        return True
    
    
    def grip_multiplier(self, temperature: float) -> float:
        # Calcula um multiplicador de grip (Aderência) com base na temperatura
        
        if self.optimal_temp_min <= temperature <= self.optimal_temp_max:
            return self.base_grip
        
        if temperature < self.optimal_temp_min: # Se estiver abaixo, o grip é menor
            temperature_diff = self.optimal_temp_min - temperature
            penalty = temperature_diff * 0.01
            return max(0.7, self.base_grip - penalty)
        
        if temperature > self.optimal_temp_max: # Se estiver acima demais, é superaquecimento 
            temperature_diff = temperature - self.optimal_temp_max
            penalty = temperature_diff * 0.015
            return max(0.6, self.base_grip - penalty)
        
        return self.base_grip
    
    
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "display_name": self.display_name,
            "base_grip": self.base_grip,
            "degradation_rate": self.degradation_rate,
            "optimal_life": self.optimal_life,
            "optimal_temp_min": self.optimal_temp_min,
            "optimal_temp_max": self.optimal_temp_max,
            "color_code": self.color_code,
            "color_name": self.color_name,
            "cliff_lap": self.cliff_lap,
            "cliff_factor": self.cliff_factor,
            "warm_up_laps": self.warm_up_laps,
            "dry_performance": self.dry_performance,
            "wet_performance": self.wet_performance,
            "description": self.description,
        }