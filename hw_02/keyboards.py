from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def get_feedback_keyboard():
    kb_builder = ReplyKeyboardBuilder()
    kb_builder.button(text="Оставить отзыв")

    kb_markup = kb_builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True)

    return kb_markup


def get_grade_keyboard():
    kb_builder = InlineKeyboardBuilder()

    for i in range(1, 6, 1):
        kb_builder.button(text=str(i), callback_data=str(i))

    return kb_builder.as_markup()


