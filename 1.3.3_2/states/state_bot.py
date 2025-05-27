from aiogram.fsm.state import State, StatesGroup

class NoteStates(StatesGroup):
    Start = State()
    AddNote = State()
    DeleteNote = State()