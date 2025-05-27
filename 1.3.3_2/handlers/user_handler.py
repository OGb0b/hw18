from ftplib import all_errors

from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from data import notes
from keyboard.inline_kb import start_keyboard_inline, kb
from states.state_bot import NoteStates
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

router = Router()

# Старт бота (сброс состояния)
@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await state.clear()  # Сброс всех состояний
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
    note_text = message.text
    notes.append(note_text)
    # Здесь можно сохранить заметку (например, в словарь или БД)
    # await state.update_data(last_note=note_text)  # Сохраняем временно в FSM, нужно сохранить в бд
    await message.answer(f"Заметка сохранена:\n\n{note_text}")
    await state.set_state(NoteStates.Start)  # Возврат в начальное состояние
    await message.answer("Выберите действие:", reply_markup=start_keyboard_inline)


@router.callback_query(F.data == 'show', NoteStates.Start)
async def show_notes(cb: CallbackQuery, state: FSMContext):
    await cb.answer()

    # Здесь должен быть код для получения заметок из БД/хранилища
    if not notes:
        await cb.message.answer("📭 У вас пока нет заметок.")
    else:
        await cb.message.answer(
            "📋 Ваши заметки:\n\n" + "\n".join(f"• {note}" for note in notes)
        )

    await cb.message.answer("Выберите действие:", reply_markup=start_keyboard_inline)


@router.callback_query(F.data == 'delete', NoteStates.Start)
async def select_notes_to_delete(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    if not notes:
        await callback.message.answer("📭 У вас пока нет заметок.")
        return

    buttons = []
    for index, note in enumerate(notes):
        note_preview = ' '.join(note.split()[:3])
        if len(note.split()) > 3:
            note_preview += " ..."

        buttons.append(
            InlineKeyboardButton(
                text=f"{index + 1}. {note_preview}",
                callback_data=f"delete_note_{index}"  # Сохраняем индекс в формате "delete_note_0"
            )
        )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons[i:i + 2] for i in range(0, len(buttons), 2)])
    await state.set_state(NoteStates.DeleteNote)
    await callback.message.answer(
        "Выберите заметку для удаления:",
        reply_markup=keyboard
    )


@router.callback_query(NoteStates.DeleteNote)
async def confirm_note_deletion(callback: CallbackQuery, state: FSMContext):
    try:
        # Извлекаем индекс из callback_data (формат "delete_note_0")
        note_index = int(callback.data.split('_')[-1])

        if 0 <= note_index < len(notes):
            deleted_note = notes.pop(note_index)  # Удаляем выбранную заметку
            await callback.message.answer(f"🗑 Заметка удалена:\n{deleted_note}")
        else:
            await callback.message.answer("⚠ Ошибка: заметка не найдена")

    except (ValueError, IndexError):
        await callback.message.answer("⚠ Ошибка при обработке запроса")

    # Всегда возвращаемся в начальное состояние после одного удаления
    await state.set_state(NoteStates.Start)
    await callback.answer()
    await callback.message.answer(
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