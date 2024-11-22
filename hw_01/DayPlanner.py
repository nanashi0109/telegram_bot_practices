import asyncio
from datetime import *
from resources.config import TOKEN_HW_1_1

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command, CommandObject

bot = Bot(token=TOKEN_HW_1_1)
dispatcher = Dispatcher()

commands_list = {"/start": "печатает на экран описание, указанное сверху.",
                 "/add_task <время> <описание>": "добавляет задачу (например, /add_task 14:00 Купить продукты).",
                 "/show_tasks": "показывает список задач на день в виде чек-листа.",
                 "/remove_task <время>": "удаляет задачу по времени (например, /remove_task 14:00).",
                 "/clear_tasks": "очищает весь план дня."}


users_tasks = {}


def add_user_at_tasks(user_id: int) -> None:
    if user_id not in users_tasks.keys():
        users_tasks[user_id] = {}


@dispatcher.message(Command("start"))
async def start_handler(message: types.Message) -> None:
    add_user_at_tasks(message.chat.id)
    await message.answer("Бот помогает пользователю составить план дня, добавляя задачи с указанием времени и пометками о приоритете")


@dispatcher.message(Command("help"))
async def help_handler(message: types.Message):
    commands = get_commands_string()

    await message.answer(commands)


def get_commands_string() -> str:
    commands = ""
    for key in commands_list:
        commands += f"{key} - {commands_list[key]}\n"

    return commands


@dispatcher.message(Command("add_task"))
async def add_task_handler(message: types.Message, command: CommandObject):
    add_user_at_tasks(message.chat.id)

    error_message = "Неверные аргументы для команды. Для подробной информации воспользуйся командой /help"

    if command.args is None:
        await message.answer(error_message)
        return
    command = command.args.split(" ", 1)
    if len(command) < 2:
        await message.answer(error_message)
        return
    try:
        task_time, task_text = datetime.strptime(command[0], "%H:%M").time(), command[1]
    except ValueError:
        await message.answer(error_message)
        return

    users_tasks[message.chat.id][str(task_time)] = task_text
    await message.answer(f"Задача '{task_text}' на {task_time} обавлена")


@dispatcher.message(Command("show_tasks"))
async def show_tasks_handler(message: types.Message):
    add_user_at_tasks(message.chat.id)

    tasks = users_tasks[message.chat.id]
    if len(tasks) == 0:
        await message.answer("У вас нет задач")
        return
    tasks_times = list(tasks.keys())
    tasks_times = snail_sorting(tasks_times, key=lambda x: str(x), order_by=lambda x, y: x > y)

    tasks_string = "Ваши задачи:\n"
    for i in tasks_times:
        tasks_string += f"{i}: {tasks[i]}\n"

    await message.answer(tasks_string)


def snail_sorting(collection: list, key: lambda x: str(x), order_by: lambda x, y: x > y):
    array = collection.copy()

    length_array = len(array)
    if length_array == 0:
        return array

    if length_array == 1:
        return array

    for i in range(0, length_array-1, 1):
        for j in range(0, length_array-i-1, 1):
            if order_by(key(array[j]), key(array[j+1])):
                array[j], array[j+1] = array[j+1], array[j]

    return array


@dispatcher.message(Command("remove_task"))
async def remove_task_handler(message: types.Message, command: CommandObject):
    error_message = "Неверные аргументы для команды. Для подробной информации воспользуйся командой /help"

    if command.args is None:
        await message.answer(error_message)
        return

    try:
        task_time = datetime.strptime(command.args, "%H:%M").time()
        task_time = str(task_time)
    except ValueError:
        await message.answer(error_message)
        return

    tasks = users_tasks[message.chat.id]
    if task_time in tasks.keys():
        await message.answer(f"Задача {tasks[task_time]}  удалена")
        del tasks[task_time]
    else:
        await message.answer("Нет задач на это время")


@dispatcher.message(Command("clear_tasks"))
async def clear_tasks_handler(message: types.Message):
    try:
        del users_tasks[message.chat.id]
        add_user_at_tasks(message.chat.id)
        await message.answer("Задачи очищены")
    except KeyError:
        await message.answer("У вас нет задач")


@dispatcher.message(F.text)
async def other_text_hanler(message: types.Message):
    await message.answer("Неверная команда.\n Для просмотра списка комманд воспользуйся /help")


async def main():
    await dispatcher.start_polling(bot)

asyncio.run(main())
