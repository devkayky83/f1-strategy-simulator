# Modelo de Dados para Pit Stops

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class PitStop(Base):
    # Representa um pit stop individual dentro de uma estratégia
    
    __tablename__ = "pit_stops"
    
    id = Column(Integer, primary_key=True, index=True)
    
    strategy_id = Column(Integer, ForeignKey("strategies.id"), nullable=False)
    
    lap_number = Column(Integer, nullable=False)
    tire_compound_id = Column(Integer, ForeignKey("tire_compounds.id"), nullable=False)
    tire_compound_name = Column(String(20))
    
    tire_age_at_stop = Column(Integer)
    tire_degradation = Column(Float)
    
    pit_duration = Column(Float, default=2.5)
    total_time_loss = Column(Float)
    
    fuel_added = Column(Float, default=0.0)
    
    stop_type = Column(String(20), default="planned")
    
    notes = Column(String(200))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    strategy = relationship("Strategy", back_populates="pit_stops")
    
    
    def __repr__(self):
        return f"<PitStop(lap={self.lap_number}, compound='{self.tire_compound_name}')>"
    
    
    def to_dict(self):
        return {
            "id": self.id,
            "strategy_id": self.strategy_id,
            "lap_number": self.lap_number,
            "tire_compound_name": self.tire_compound_name,
            "tire_age_at_stop": self.tire_age_at_stop,
            "tire_degradation": self.tire_degradation,
            "pit_duration": self.pit_duration,
            "total_time_loss": self.total_time_loss,
            "fuel_added": self.fuel_added,
            "stop_type": self.stop_type,
            "notes": self.notes,
        }