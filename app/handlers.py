#TODO Тот кто рабоает с базой данных обрати внимания на функции: test, look_at_material, на все функции, где в названии есть look_at_material и get_result

import app.keyboards as kb
import logging

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery 
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.filters.callback_data import CallbackData

router = Router()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('logs.log', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


@router.message(CommandStart())
async def test(message: Message):
    '''
    Хенлер стартового сообщения
    '''
    try:
        if message.from_user.id in 'СЮДА ПОДАТЬ СПИСОК ID ЖЮРИ':
            await message.answer('Вы авторизовались как жюри', reply_markup=kb.jury_initial_keyboard)

        else:
            await message.answer('Добро пожаловать. На данный момент доступны следующие функции:', reply_markup=kb.player_initial_keyboard)
    except:
        logger.error('Ошиюка при отправке ответа на стартовое сообщение')


@router.callback_query(F.data == 'look_at_material')
async def look_at_material_first(callback: CallbackQuery):
    '''
    Хендлер нажатия на кнопку "Просмотр материала команд и его оценка"
    '''
    try:
        await callback.answer('Вы выбрали посмотреть материал команды')
        await callback.message.answer('Выберите команду, чей материал вы хотите посмотреть', reply_markup=await kb.generate_keyboard('СЮДА ПОДАТЬ СПИСОК НАЗВАНИЙ КОМАНД', 'look_at_material'))

    except Exception as e:
        logger.error(f'Произошла ошибка при просмотре материала: {e}. Функция - look_at_material_first')


class Look_at_material(StatesGroup):
    mark = State()


@router.callback_query(F.data.split('-')[0] == 'look_at_material')
async def look_at_material_second(callback: CallbackQuery, state: FSMContext):
    '''
    Хендлер для вывода материалов после вывода всех доступных команд
    '''
    try:
        await callback.answer()
        await callback.message.answer('На данный момент доступны следующие материалы: {"СЮДА НУЖНО ПОДАТЬ ВСЕ ДОСТУПНЫЕ МАТЕРИАЛЫ. НАЗВАНИЕ КОМАНДЫ ХРАНИТСЯ В ПЕРЕМЕННОЙ callback.data.split("-")[1]"}')
        await callback.message.answer(f'Введите оценку команде {callback.data.split('-')[1]}')

        await state.update_data(name=callback.data.split('-')[1])
        await state.set_state(Look_at_material.mark)

    except Exception as e:
        logger.error(f'Произошла ошибка при выводе выбранной команды: {e}. Функция - look_at_material_second')


@router.message(Look_at_material.mark)
async def look_at_material_third(message: Message, state: FSMContext):
    try:
        await state.update_data(mark=message.text)
        data = await state.get_data()

        "ПЕРЕМЕННАЯ data - словарь.  оценка находится по ключу mark, а название команды по ключу name"
        message.answer('Оценка команде успешно поставлена!')

    except Exception as e:
        logger.error(f'Произошла ошибка при записи оценки для команды: {e} Функция - look_at_material_third')
    
    finally:
        state.clear()


@router.callback_query(F.data == 'get_result')
async def get_result_first(callback: CallbackQuery):
    '''
    Хендлер нажатия на кнопку "Подведение результатов"
    '''
    try:
        await callback.answer('Вы выбрали подведение результатов')
        await callback.message.answer('Выберите команду, чьи оценки вы хотите посмотреть', reply_markup=await kb.generate_keyboard('СЮДА ПОДАТЬ СПИСОК НАЗВАНИЙ КОМАНД', 'get_result'))

    except Exception as e:
        logger.error(f'Произошла ошибка при подведении результатов: {e}. Функция - get_result_first')


@router.callback_query(F.data.split('-')[0] == 'get_result')
async def get_result_second(callback: CallbackQuery):
    '''
    Хендлер для отправки пользователю статистики
    '''
    try:
        await callback.answer()
        await callback.message.answer('Статистика следующая: {СЮДА ВПИСАТЬ ФУНКЦИЮ ВЫВОДА СТАТИСТИКИ О КОМАНДЕ. НАЗВАНИЕ КОМАНДЫ ХРАНИТСЯ В ПЕРЕМЕННОЙ callback.data.split("-")[1]}')

    except Exception as e:
        logger.error(f'Произошла ошибка при отправки статистики: {e}. Функция - get_result_second')