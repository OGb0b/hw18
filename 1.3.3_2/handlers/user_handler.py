from aiogram import Router, F
from aiogram.dispatcher.middlewares import data
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from keyboard.inline_kb import start_keyboard_inline
from states.state_bot import NoteStates
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.note_data import  save_data, load_data
import datetime


router = Router()

@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Выберите действие:",
         reply_markup=start_keyboard_inline)
    await state.set_state(NoteStates.Start)


@router.callback_query(F.data == 'add', NoteStates.Start)
async def add_note_start(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await cb.message.answer("Введите текст заметки:")
    await state.set_state(NoteStates.AddNote)

@router.message(NoteStates.AddNote)
async def save_note(message: Message, state: FSMContext):
    user_id = message.from_user.id
    note_text = message.text
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    note = load_data()
    if str(user_id) in note:
        note[str(user_id)].append({current_time: note_text})
    else:
        note[user_id] = [{current_time: note_text}]
    save_data(note)
    await message.answer(f"Заметка сохранена:\n\n{note_text}")
    await state.set_state(NoteStates.Start)
    await message.answer("Выберите действие:", reply_markup=start_keyboard_inline)


@router.callback_query(F.data == 'show', NoteStates.Start)
async def show_notes(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    user_id = cb.from_user.id
    note = load_data()
    user_notes = note.get(str(user_id), [])  # Получаем список заметок или пустой список
    notes_text = [
        f"• {list(note_data.values())[0]}"  # Извлекаем текст заметки
        for note_data in user_notes
    ]
    await cb.message.answer(
        "📋 Ваши заметки:\n\n" + "\n".join(notes_text) if notes_text else "📭 У вас пока нет заметок."
    )
    await cb.message.answer("Выберите действие:", reply_markup=start_keyboard_inline)


@router.callback_query(F.data == 'delete', NoteStates.Start)
async def select_notes_to_delete(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    user_id = str(cb.from_user.id)  # Приводим к строке
    note = load_data()
    user_notes = note.get(user_id, [])  # Безопасное получение заметок

    if not user_notes:
        await cb.message.answer("📭 У вас пока нет заметок.")
        return

    # Создаем кнопки для каждой заметки
    buttons = []
    for index, note_data in enumerate(user_notes):
        # Извлекаем текст заметки (первое значение словаря {время: текст})
        note_text = list(note_data.values())[0]

        # Формируем превью (первые 3 слова + "...")
        words = note_text.split()
        preview = ' '.join(words[:3]) + ("..." if len(words) > 3 else "")

        # Добавляем кнопку
        buttons.append(
            InlineKeyboardButton(
                text=f"{index + 1}. {preview}",
                callback_data=f"delete_note_{index}"  # Индекс для удаления
            )
        )

    # Группируем кнопки по 2 в ряд
    keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons[i:i + 2] for i in range(0, len(buttons), 2)])

    # Отправляем сообщение с клавиатурой
    await state.set_state(NoteStates.DeleteNote)
    await cb.message.answer(
        "Выберите заметку для удаления:",
        reply_markup=keyboard
    )

@router.callback_query(NoteStates.DeleteNote)
async def confirm_note_deletion(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    note = load_data()
    user_id = cb.from_user.id
    user_notes = note[str(user_id)]
    try:
        note_index = int(cb.data.split('_')[-1])
        user_notes = note.get(str(user_id), [])
        if 0 <= note_index < len(user_notes):
            deleted_note = user_notes.pop(note_index)
            save_data(note)  # Сохраняем обновлённые данные
            await cb.message.answer(f"🗑 Заметка удалена:\n{list(deleted_note.values())[0]}")
        else:
            await cb.message.answer("⚠ Ошибка: заметка не найдена")
    except (ValueError, IndexError):
        await cb.message.answer("⚠ Ошибка при обработке запроса")

    await state.set_state(NoteStates.Start)
    await cb.answer()
    await cb.message.answer(
        "Выберите действие:",
        reply_markup=start_keyboard_inline)

#
# @router.callback_query(lambda cb: cb.data in ['add', 'show', 'delete'])
# async def callback(cb: CallbackQuery, state: FSMContext):
#     await cb.answer()
#     await cb.message.answer(f'Вы выбрали {cb.data}')
#

    # await state.update_data(main_course=cb.data)
    # print(f'Вы выбрали {choice}')
    # await cb.message.answer(f'Выберите напиток: ', reply_markup=kb)
    # print(await state.get_data())
    # await state.set_state(MenuState.drink_state)

# @router.callback_query(lambda cb: cb.data in ['juice', 'tea'], StateFilter('MenuState:drink_state'))
# async def get_drink(cb: CallbackQuery, state: FSMContext):
#     await cb.answer()
#     await cb.message.answer('Спасибо')
#     print(await state.get_data())
#     print(await state.get_state())
#     await state.clear()
#     await state.set_data({})
#     print(await state.get_data())
#     print(await state.get_state())

#
# @router.message(Command('test'))
# async def test_reply(m: Message):
#     await m.answer('Нажмите на кнопку', reply_markup=reply_kb.keyboard_reply)
#
# @router.message(Command('buy'))
# async def buy_func(m: Message, state: FSMContext):
#     await m.answer('Выберите основное блюдо: ', reply_markup=keyboard_inline)
#     # print(await state.get_state())
#     await state.set_state(MenuState.main_course_state)
#     # print(await state.get_state())
#     print(await state.get_data())
#