# Models de Dados para Circuitos de F1

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Circuit(Base):
    __tablename__ = "circuits"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    country = Column(String(50), nullable=False)
    city = Column(String(50))
    
    lap_distance = Column(Float, nullable=False)
    total_laps = Column(Integer, nullable=False)
    total_distance = Column(Float, nullable=False)
    
    base_lap_time = Column(Float, nullable=False)
    track_record = Column(Float)
    record_holder = Column(String(100))
    record_year = Column(Integer)
    
    tire_wear_factor = Column(Float, default=1.0)
    fuel_effect = Column(Float, default=0.03)
    pit_loss_time = Column(Float, default=22.0)
    
    number_of_turns = Column(Integer)
    longest_straight = Column(Float)
    drs_zones = Column(Integer, default=2)
    
    track_type = Column(String(20))
    direction = Column(String(20))
    track_surface = Column(String(50))
    
    typical_temp = Column(Float)
    rain_probability = Column(Float, default=0.1)
    
    first_grand_prix = Column(Integer)
    number_of_races = Column(Integer, default=0)
    description = Column(Text)
    
    elevation_change = Column(Float)
    
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    strategies = relationship("Strategy", back_populates="circuit")
    
    
    def __repr__(self):
        return f"<Circuit(name='{self.name}', country='{self.country}')>"
    
    @property
    def average_speed(self) -> float: # Calcula a velocidade média em Km/h
        if self.base_lap_time > 0:
            return (self.lap_distance / self.base_lap_time) * 3600
        return 0.0
    
    
    @property
    def total_race_time_estimate(self) -> float: # Estima o tempo total de corrida em segundos
        return self.base_lap_time * self.total_laps
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "country": self.country,
            "city": self.city,
            "lap_distance": self.lap_distance,
            "total_laps": self.total_laps,
            "total_distance": self.total_distance,
            "base_lap_time": self.base_lap_time,
            "track_record": self.track_record,
            "record_holder": self.record_holder,
            "record_year": self.record_year,
            "tire_wear_factor": self.tire_wear_factor,
            "fuel_effect": self.fuel_effect,
            "pit_loss_time": self.pit_loss_time,
            "number_of_turns": self.number_of_turns,
            "longest_straight": self.longest_straight,
            "drs_zones": self.drs_zones,
            "track_type": self.track_type,
            "direction": self.direction,
            "typical_temp": self.typical_temp,
            "rain_probability": self.rain_probability,
            "average_speed": self.average_speed,
            "is_active": self.is_active,
        }