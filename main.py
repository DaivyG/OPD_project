import asyncio

from aiogram import Bot, Dispatcher
from app.handlers import router


bot = Bot(token='')
dp = Dispatcher()

async def main():
    '''
    Функция для начала работы бота
    '''
    try:
        dp.include_router(router)
        await dp.start_polling(bot)

    except Exception as e:
        print(f'Произошла ошибка при попытке начать работу бота: {e}')

if __name__ == '__main__':
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        print('Бот завершил работу')
