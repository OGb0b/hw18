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
    user_notes = note.get(str(user_id), [])
    notes_text = [
        f"• {list(note_data.values())[0]}"
        for note_data in user_notes
    ]
    await cb.message.answer(
        "📋 Ваши заметки:\n\n" + "\n".join(notes_text) if notes_text else "📭 У вас пока нет заметок."
    )
    await cb.message.answer("Выберите действие:", reply_markup=start_keyboard_inline)


@router.callback_query(F.data == 'delete', NoteStates.Start)
async def select_notes_to_delete(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    user_id = str(cb.from_user.id)
    note = load_data()
    user_notes = note.get(user_id, [])

    if not user_notes:
        await cb.message.answer("📭 У вас пока нет заметок.")
        return

    buttons = []
    for index, note_data in enumerate(user_notes):
        note_text = list(note_data.values())[0]
        words = note_text.split()
        preview = ' '.join(words[:3]) + ("..." if len(words) > 3 else "")


        buttons.append(
            InlineKeyboardButton(
                text=f"{index + 1}. {preview}",
                callback_data=f"delete_note_{index}"  # Индекс для удаления
            )
        )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons[i:i + 2] for i in range(0, len(buttons), 2)])
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
            save_data(note)
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

