from aiogram import types, F
from aiogram.dispatcher.router import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.methods.send_message import SendMessage
from aiogram import Bot

from bot.handlers.states import UserFormState
from utils.settings import Settings
from bot.keyboards.reply_keyboards import get_main_keyboard
from bot.keyboards.inline_keyboards import get_copy_keyboard

import bot.answers.request as ANSWERS


command_router = Router()
bot: Bot


def regsier_bot(b: Bot):
    global bot
    bot = b


@command_router.message(Command(commands=["start"]))
async def start(msg: types.Message) -> None:
    """Answers to \start

    Args:
        msg (types.Message): object of message
        state (FSMContext): object of state
    """

    await msg.answer(text=ANSWERS.HELLO_TEXT, reply_markup=get_main_keyboard())


@command_router.message(F.text == "Сделать заказ")
async def begin_request(msg: types.Message, state: FSMContext):
    """Begins a making of request

    Args:
        msg (types.Message): object of message
        state (FSMContext): object of state
    """
    await msg.answer(text=ANSWERS.GET_FIO_TEXT)
    await state.set_state(UserFormState.FIO)


@command_router.message(UserFormState.FIO)
async def get_name(msg: types.Message, state: FSMContext):
    """Gets FIO of user

    Args:
        msg (types.Message): object of message
        state (FSMContext): object of state
    """
    await msg.answer(text=ANSWERS.GET_PHONE_NUMBER_TEXT)
    await state.update_data(FIO=msg.text)
    await state.set_state(UserFormState.PHONE_NUMBER)


@command_router.message(UserFormState.PHONE_NUMBER)
async def get_number(msg: types.Message, state: FSMContext):
    """Gets phone number of user

    Args:
        msg (types.Message): object of message
        state (FSMContext): object of state
    """
    await msg.answer(text=ANSWERS.GET_VIN_TEXT)
    await state.update_data(PHONE_NUMBER=msg.text)
    await state.set_state(UserFormState.VIN)


@command_router.message(UserFormState.VIN)
async def get_vin(msg: types.Message, state: FSMContext):
    """Gets vin of car

    Args:
        msg (types.Messgae): object of message
        state (FSMContext): object of state
    """

    await msg.answer(text=ANSWERS.GET_PROBLEM_TEXT)
    await state.update_data(VIN=msg.text)
    await state.set_state(UserFormState.PROBLEM)


@command_router.message(UserFormState.PROBLEM)
async def get_problem(msg: types.Message, state: FSMContext):
    """Gets problem of user

    Args:
        msg (types.Messgae): object of message
        state (FSMContext): object of state
    """
    global bot
    await msg.answer(text=ANSWERS.END_FORM_TEXT)
    await state.update_data(PROBLEM=msg.text)
    await bot(
        SendMessage(
            chat_id=Settings.get_admin_id(),
            text=ANSWERS.RESEND_REQUEST,
        )
    )
    user_data = await state.get_data()
    await state.clear()
    answer = f"""ФИО: {user_data['FIO']}
tg: @{msg.from_user.username}
Номер телефона: {user_data['PHONE_NUMBER']}\n
VIN: {user_data['VIN']}
Заявка: {user_data['PROBLEM']}
"""
    await bot.send_message(chat_id=Settings.get_admin_id(), text=f"{answer}")


# TODO сделать проверку формата номера и вина
# TODO добавить кнопку для заказа
