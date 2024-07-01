from aiogram import types, F
from aiogram.dispatcher.router import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.methods.send_message import SendMessage
from aiogram import Bot

from bot.handlers.states import UserFormState
from utils.settings import Settings
from bot.keyboards.reply_keyboards import get_main_keyboard
from bot.keyboards.inline_keyboards import get_check_data_keyboard, get_no_vin_keyboard
from bot.helpers.get_text_data import get_text_from_data
from bot.helpers import checkers

import bot.answers.request as ANSWERS
import logging

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
    if checkers.check_phone_number(msg.text):
        await state.update_data(PHONE_NUMBER=msg.text)
        await state.set_state(UserFormState.VIN)
        await msg.answer(text=ANSWERS.GET_VIN_TEXT, reply_markup=get_no_vin_keyboard())
    else:
        await msg.answer(text=ANSWERS.WRONG_NUMBER_TEXT)


@command_router.message(UserFormState.VIN)
async def get_vin(msg: types.Message, state: FSMContext):
    """Gets vin of car

    Args:
        msg (types.Messgae): object of message
        state (FSMContext): object of state
    """
    await bot.edit_message_reply_markup(
        chat_id=msg.from_user.id, message_id=msg.message_id-1, reply_markup=None
    )
    if len(msg.text) == 17:
        await state.update_data(VIN=msg.text)
        await state.set_state(UserFormState.PROBLEM)
        await msg.answer(text=ANSWERS.GET_PROBLEM_TEXT)
    else:
        await msg.answer(text=ANSWERS.WRONG_VIN_TEXT)


@command_router.message(UserFormState.PROBLEM)
async def get_problem(msg: types.Message, state: FSMContext):
    """Gets problem of user

    Args:
        msg (types.Messgae): object of message
        state (FSMContext): object of state
    """
    global bot
    await state.update_data(PROBLEM=msg.text)
    await check_data(msg, state)


async def check_data(msg: types.Message, state: FSMContext):
    """Generates messages about checkig information

    Args:
        msg (types.Message): object of message
        state (FSMContext): object od state
    """
    await msg.answer(text=ANSWERS.CHECK_TEXT)
    user_data = await state.get_data()
    answer = get_text_from_data(user_data)
    await msg.answer(text=answer, reply_markup=get_check_data_keyboard())
    await state.set_state(UserFormState.CHECK)


@command_router.callback_query(F.data == "checks_passed")
async def finish_request(data: types.CallbackQuery, state: FSMContext):
    """Finishing checks and send data to admin

    Args:
        state (FSMContext): object of state
    """
    logging.info("Checks for some user have been passed.")
    await bot.send_message(chat_id=data.from_user.id, text=ANSWERS.END_FORM_TEXT)
    await data.answer()
    await bot.edit_message_reply_markup(
        chat_id=data.from_user.id, message_id=data.message.message_id, reply_markup=None
    )

    await bot(
        SendMessage(
            chat_id=Settings.get_admin_id(),
            text=ANSWERS.RESEND_REQUEST,
        )
    )
    user_data = await state.get_data()

    answer = get_text_from_data(user_data, data)
    await bot(
        SendMessage(
            chat_id=Settings.get_admin_id(),
            text=answer,
        )
    )


@command_router.callback_query(F.data == "change_name")
async def change_name(data: types.CallbackQuery, state: FSMContext):
    """Function for change name of user

    Args:
        data (types.CallbackQuery): _description_
        state (FSMContext): _description_
    """
    await bot.edit_message_reply_markup(
        chat_id=data.from_user.id, message_id=data.message.message_id, reply_markup=None
    )
    await bot.send_message(chat_id=data.from_user.id, text=ANSWERS.GET_FIO_TEXT)
    await state.set_state(UserFormState.CHANGE_FIO)


@command_router.message(UserFormState.CHANGE_FIO)
async def save_changed_name(msg: types.Message, state: FSMContext):
    """Function for reading name that said user for change

    Args:
        msg (types.Message): object of message
        state (FSMContext): object of state
    """
    await state.update_data(FIO=msg.text)
    await check_data(msg, state)
    await state.set_state(UserFormState.CHECK)


@command_router.callback_query(F.data == "change_phone_number")
async def change_phone_number(data: types.CallbackQuery, state: FSMContext):
    """Begins changing of number

    Args:
        data (types.CallbackQuery): object of data
        state (FSMContext): object of state
    """
    await bot.edit_message_reply_markup(
        chat_id=data.from_user.id, message_id=data.message.message_id
    )
    await bot.send_message(
        chat_id=data.from_user.id, text=ANSWERS.GET_PHONE_NUMBER_TEXT
    )
    await state.set_state(UserFormState.CHANGE_PHONE_NUMBER)


@command_router.message(UserFormState.CHANGE_PHONE_NUMBER)
async def save_changed_number(msg: types.Message, state: FSMContext):
    """Saves changed phone number to state

    Args:
        data (types.CallbackQuery): object of message
        state (FSMContext): object of state
    """
    if checkers.check_phone_number(msg.text):
        await state.update_data(PHONE_NUMBER=msg.text)
        await check_data(msg, state)
    else:
        await msg.answer(text=ANSWERS.WRONG_NUMBER_TEXT)


@command_router.callback_query(F.data == "change_vin")
async def change_vin(data: types.CallbackQuery, state: FSMContext):
    """Begins changing of vin

    Args:
        data (types.CallbackQuery): object of data
        state (FSMContext): object of state
    """
    await bot.edit_message_reply_markup(
        chat_id=data.from_user.id, message_id=data.message.message_id
    )
    await bot.send_message(chat_id=data.from_user.id, text=ANSWERS.GET_VIN_TEXT, reply_markup=get_no_vin_keyboard(True))
    await state.set_state(UserFormState.CHANGE_VIN)


@command_router.message(UserFormState.CHANGE_VIN)
async def save_changed_vin(msg: types.Message, state: FSMContext):
    """Saves changed vin to state

    Args:
        data (types.CallbackQuery): object of message
        state (FSMContext): object of state
    """
    if len(msg.text) == 17:
        await state.update_data(VIN=msg.text)
        await check_data(msg, state)
    else:
        await msg.answer(text=ANSWERS.WRONG_VIN_TEXT)


@command_router.callback_query(F.data == "change_text")
async def change_text(data: types.CallbackQuery, state: FSMContext):
    """Function for change request

    Args:
        data (types.CallbackQuery): _description_
        state (FSMContext): _description_
    """
    await bot.edit_message_reply_markup(
        chat_id=data.from_user.id, message_id=data.message.message_id, reply_markup=None
    )
    await bot.send_message(chat_id=data.from_user.id, text=ANSWERS.GET_PROBLEM_TEXT)
    await state.set_state(UserFormState.CHANGE_PROBLEM)


@command_router.message(UserFormState.CHANGE_PROBLEM)
async def save_changed_problem(msg: types.Message, state: FSMContext):
    """Function for reading problm that said user for change

    Args:
        msg (types.Message): object of message
        state (FSMContext): object of state
    """
    await state.update_data(PROBLEM=msg.text)
    await check_data(msg, state)


@command_router.callback_query(F.data.in_(['no_vin', 'edit_no_vin']))
async def no_vin(data: types.CallbackQuery, state: FSMContext):
    """Works if auto has no vin

    Args:
        data (types.CallbackQuery): _description_
        state (FSMContext): _description_
    """
    await bot.edit_message_reply_markup(chat_id = data.from_user.id, message_id = data.message.message_id, reply_markup=None)
    await state.update_data(VIN = "отсутствует")
    await bot.edit_message_text(chat_id=data.from_user.id, message_id = data.message.message_id, text = ANSWERS.GET_NAME_OF_AUTO_TEXT)
    await data.answer()
    if data.data =='no_vin':
        await state.set_state(UserFormState.AUTO)
    else:
        logging.info("Reply markup in edit mode is working")
        await state.set_state(UserFormState.EDIT_AUTO)
    

@command_router.message(UserFormState.AUTO)
async def save_auto_name(msg: types.Message, state: FSMContext):
    await state.update_data(AUTO = msg.text)
    await state.set_state(UserFormState.PROBLEM)
    await msg.answer(text=ANSWERS.GET_PROBLEM_TEXT)
    
@command_router.message(UserFormState.EDIT_AUTO)
async def save_auto_name(msg: types.Message, state: FSMContext):
    await state.update_data(AUTO = msg.text)
    await check_data(msg, state)