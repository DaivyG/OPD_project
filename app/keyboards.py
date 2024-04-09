
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


jury_initial_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Просмотр материала команд и его оценка', callback_data='look_at_material_of_commands')],
    [InlineKeyboardButton(text='Подведение результатов', callback_data='get_result')]
], resize_keyboard=True)


player_initial_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Вступить в существующую группу')],
    [KeyboardButton(text='Создать новую группу')]
], resize_keyboard=True)

async def generate_keyboard(data, callback_prefix):
        '''
        Генерирует клавиатуру из названий команд в БД
        '''
        keyboard = InlineKeyboardBuilder()
        for name in data:
            keyboard.add(InlineKeyboardButton(text=name, callback_data=f'{callback_prefix}-{name}'))

        return keyboard.adjust(2).as_markup()