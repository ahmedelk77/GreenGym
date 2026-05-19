from sqlalchemy import Column, String, Float, Integer, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class GymHall(Base):
    __tablename__ = "gym_hall"

    id = Column(Integer, primary_key=True)
    country = Column(String)
    electricity_tariff_type = Column(String)  # Ex: "flat", "tiered", "time_based", "subscription"
    currency = Column(String)
    max_energy_consumption = Column(Float, nullable=True)  # For users with existing gyms
    has_piezo = Column(Boolean)
    has_cardio_machines = Column(Boolean)
    is_existing_gym = Column(Boolean)  # True: existing, False: planned, None: transitional

    lighting_type = Column(String, nullable=True)
    ventilation_type = Column(String, nullable=True)
    has_collective_classes = Column(Boolean, nullable=True)
    extra_spaces = Column(String, nullable=True)  # Describes additional intensive-use zones

    piezo = relationship("PiezoData", back_populates="gym", uselist=False)
    cardio = relationship("CardioData", back_populates="gym", uselist=False)
    tariff_tiers = relationship("TariffTier", back_populates="gym")

class PiezoData(Base):
    __tablename__ = "piezo_data"

    id = Column(Integer, primary_key=True)
    gym_id = Column(Integer, ForeignKey("gym_hall.id"))
    surface_m2 = Column(Float)
    production_per_m2 = Column(Float)
    passages_per_day = Column(Float)
    opening_days = Column(Float)

    gym = relationship("GymHall", back_populates="piezo")

class CardioData(Base):
    __tablename__ = "cardio_data"

    id = Column(Integer, primary_key=True)
    gym_id = Column(Integer, ForeignKey("gym_hall.id"))
    machine_count = Column(Integer)
    avg_power_watt = Column(Float)
    avg_usage_hours_per_day = Column(Float)
    opening_days = Column(Float)
    efficiency = Column(Float)

    gym = relationship("GymHall", back_populates="cardio")

class TariffTier(Base):
    __tablename__ = "tariff_tier"

    id = Column(Integer, primary_key=True)
    gym_id = Column(Integer, ForeignKey("gym_hall.id"))
    max_kwh = Column(Float)
    price_per_kwh = Column(Float)

    gym = relationship("GymHall", back_populates="tariff_tiers")