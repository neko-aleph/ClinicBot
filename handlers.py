from aiogram import types, Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import database
import keyboards as kb
import datetime


router = Router()


class Rec(StatesGroup):
    doctor = State()
    date = State()
    time = State()
    client = State()


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Rec.doctor)
    await message.answer(f'Здравствуйте, {message.from_user.full_name}, на прием к какому врачу вы хотели бы записаться?',
                         reply_markup=await kb.employees())


@router.message(F.text == 'Записаться')
async def appoint(message: Message, state: FSMContext) -> None:
    await state.set_state(Rec.doctor)
    await message.answer(
        'На прием к какому врачу вы хотели бы записаться?', reply_markup=await kb.employees())


@router.message((F.text == 'Мои записи') | (F.text == 'Отмена'))
async def client_appointments(message: Message, state: FSMContext) -> None:
    name = await database.get_name(message.chat.id, message.from_user.full_name)

    if name is None:
        await message.answer('У вас нет записей', reply_markup=kb.main())
        return

    appointments = await database.get_appointments(name, 'client')
    active = []
    for appointment in appointments:
        if appointment.date >= datetime.datetime.now().date():
            active.append(appointment)

    if active:
        answer = ''
        for appointment in active:
            answer += f'{appointment.doctor} {appointment.date} {appointment.time}\n'
        await message.answer(answer, reply_markup=kb.main())
    else:
        await message.answer('У вас нет записей', reply_markup=kb.main())


@router.message(Rec.date)
async def select_time(message: Message, state: FSMContext) -> None:
    await state.update_data(date=message.text)
    await state.set_state(Rec.time)
    await message.answer('Выберите время:', reply_markup=kb.time())


@router.message(Rec.time)
async def select_name(message: Message, state: FSMContext) -> None:
    await state.update_data(time=message.text)
    await state.set_state(Rec.client)
    await message.answer('Введите имя:', reply_markup=await kb.name(message.chat.id, message.from_user.full_name))


@router.message(Rec.client)
async def finish(message: Message, state: FSMContext) -> None:
    await state.update_data(client=message.text)
    data = await state.get_data()

    try:
        res = await database.create_appointment(data['client'],
                                                data['doctor'],
                                                datetime.datetime.strptime(data['date'], '%Y-%m-%d').date(),
                                                datetime.datetime.strptime(data['time'], '%H:%M').time())
        if res:
            await message.answer(f'Вы успешно записались к {data["doctor"]} {data["date"]} в {data["time"]}',
                                 reply_markup=kb.main())
            await database.set_name(message.chat.id, data['client'])
        else:
            await message.answer(f'Не удалось записаться. Попробуйте снова', reply_markup=kb.main())
    except ValueError:
        await message.answer(f'Не удалось записаться. Попробуйте снова', reply_markup=kb.main())


@router.callback_query(F.data, Rec.doctor)
async def doc_callback_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(doctor=callback.data)
    await callback.answer('Вы выбрали врача')
    await state.set_state(Rec.date)
    await callback.message.answer('Выберите дату:', reply_markup=kb.date())
