from aiogram import types, Router, F
from aiogram.filters import Command, StateFilter

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from hw_02.keyboards import get_feedback_keyboard, get_grade_keyboard
from hw_02.model import FeedbackModel

import csv


router = Router()
feedbacks = []


class FeedbackStates(StatesGroup):
    general_impression = State()
    grading = State()
    commenting = State()


def add_new_feedback(data):
    feedback = FeedbackModel(data["impression"], data["grade"], data["comment"])

    feedbacks.append(feedback)


@router.message(StateFilter(None), Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    await message.answer("Привет! Этот бот создан для сбора обратной связи. "
                         "Чтобы оставить сообщение, необходимо ввести команду /feedback"
                         " или нажать на кнопку «Оставить отзыв» ниже",
                         reply_markup=get_feedback_keyboard())


@router.message(StateFilter(None), Command("show"))
async def show_handler(message: types.Message, state: FSMContext):
    if len(feedbacks) == 0:
        await message.answer("Пока нет отзывов")
        return

    for feedback in feedbacks:
        await message.answer(feedback.get_stats)


@router.message(StateFilter(None), Command("feedback"))
async def feedback_handler(message: types.Message, state: FSMContext):
    await message.answer("Опишите свои впечатления")

    await state.set_state(FeedbackStates.general_impression)


@router.message(StateFilter(None), F.text == "Оставить отзыв")
async def feedback_handler(message: types.Message, state: FSMContext):
    await message.answer("Опишите свои впечатления")

    await state.set_state(FeedbackStates.general_impression)


@router.message(StateFilter(FeedbackStates.general_impression), F.text)
async def impression_handler(message: types.Message, state: FSMContext):
    await state.update_data(impression=message.text)

    await message.answer("Оцените по шкале от 1 до 5", reply_markup=get_grade_keyboard())

    await state.set_state(FeedbackStates.grading)


@router.callback_query(StateFilter(FeedbackStates.grading),
                       lambda callback: callback.data in [str(i) for i in range(1, 6, 1)])
async def grade_handler(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(grade=callback.data)

    message = callback.message
    await message.delete_reply_markup()

    await message.answer("Оставьте комментарий")

    await state.set_state(FeedbackStates.commenting)


@router.message(StateFilter(FeedbackStates.commenting), F.text)
async def comment_handler(message: types.Message, state: FSMContext):
    await message.answer("Спасибо за отзыв!")
    await state.update_data(comment=message.text)

    user_data = await state.get_data()
    add_new_feedback(user_data)

    await state.clear()


# @router.message(StateFilter(None), Command("save"))
# async def save_handler(message: types.Message, state: FSMContext):
#     with open("feedbacks.csv", "w", newline="") as csvfile:
#         writer = csv.writer(csvfile, quotechar='|', quoting=csv.QUOTE_MINIMAL)
#         for feedback in feedbacks:
#             writer.writerow(str(feedback))
#
#     await message.answer_document(open("feedbacks.csv", "rb"))


@router.message(StateFilter(FeedbackStates.general_impression, FeedbackStates.commenting))
async def error_handler(message: types.Message, state: FSMContext):
    await message.answer("Нужно ввести текст")


@router.message(StateFilter(FeedbackStates.grading))
async def error_grade_handler(message: types.Message, state: FSMContext):
    await message.answer("Выберете оценку из предложенных")
