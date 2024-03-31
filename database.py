from typing import Any

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import select, update, ScalarResult

from config import settings
from models import *


engine = create_async_engine(
    url=settings.DB_URL,
    echo=False,
    pool_size=5,
    max_overflow=10
)


async def get_employees():
    async with AsyncSession(autoflush=False, bind=engine) as db:
        q = select(Employee)
        res = await db.execute(q)

        return res.scalars()


async def create_appointment(client, doctor, date, time) -> bool:
    async with AsyncSession(autoflush=False, bind=engine) as db:
        q = select(Appointment).where(Appointment.doctor == doctor)
        appointments = await db.execute(q)
        for appointment in appointments.scalars():
            if appointment.date == date and appointment.time == time:
                return False

        appointment = Appointment(client=client, doctor=doctor, date=date, time=time)
        try:
            db.add(appointment)
            await db.commit()
        except ValueError:
            return False
        return True


async def get_appointments(name: str, role:str) -> ScalarResult[Any]:
    async with AsyncSession(autoflush=False, bind=engine) as db:
        q = select(Appointment).where(Appointment.doctor == name if role == 'doctor' else Appointment.client == name)
        appointments = await db.execute(q)
        return appointments.scalars()


async def get_name(chatid: int, fallback_name: str) -> str:
    async with AsyncSession(autoflush=False, bind=engine) as db:
        q = select(Client).where(Client.chatid == chatid)
        res = await db.execute(q)
        res = res.scalar()
        if res:
            return res.name
        elif fallback_name:
            client = Client(chatid=chatid, name=fallback_name)
            db.add(client)
            await db.commit()
            return fallback_name
        else:
            return None


async def set_name(chatid: int, name: str):
    async with AsyncSession(autoflush=False, bind=engine) as db:
        q = select(Client).where(Client.chatid == chatid)
        res = await db.execute(q)
        if res.scalar():
            q = update(Client).where(Client.chatid == chatid).values(name=name)
            await db.execute(q)
            await db.commit()
        else:
            client = Client(chatid=chatid, name=name)
            db.add(client)
            await db.commit()
