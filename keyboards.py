import datetime

from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
import pandas as pd

import database


async def employees() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    empls = await database.get_employees()
    for employee in empls:
        empl_name = employee.name
        surname = employee.name.split()[0]
        speciality = employee.speciality
        builder.button(text=f'{speciality} - {surname}', callback_data=f'{empl_name}')

    builder.adjust(1)
    return builder.as_markup()


def date() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    dates = [datetime.datetime.strftime(day, '%Y-%m-%d') for day in pd.date_range(datetime.date.today(), periods=7)]
    for day in dates:
        builder.button(text=day)

    builder.button(text='Отмена')
    builder.adjust(1)
    return builder.as_markup()


async def time(doctor: str, date: str) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    timestamps = []
    for hour in range(8, 20+1):
        timestamps.append(f'{hour}:00')
        timestamps.append(f'{hour}:30')

    for timestamp in timestamps:
        if await database.check_time(doctor, date, timestamp):
            builder.button(text=timestamp)

    builder.button(text='Отмена')
    builder.adjust(2)
    return builder.as_markup()


async def name(chatid, fallback_name) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    res = await database.get_name(chatid, fallback_name)

    builder.button(text=res)

    builder.adjust(1)
    return builder.as_markup()


def main() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='Мои записи')
    builder.button(text='Записаться')

    builder.adjust(1)
    return builder.as_markup()
