from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Date, Time, BigInteger


class Base(DeclarativeBase):
    pass


class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    client = Column(String, nullable=False)
    doctor = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    chatid = Column(BigInteger, nullable=False)
    name = Column(String, nullable=False)


class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    speciality = Column(String, nullable=False)
    office = Column(Integer)