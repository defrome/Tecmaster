import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards.user_keyboards import builder

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("httpx")
logger.setLevel(logging.WARNING)

# Объект бота
bot = Bot(token="7783836620:AAEKekan25gE2N6UOw3_xMWaHDVUSEh_Gc0")
# Диспетчер
dp = Dispatcher()

router = Router()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Компания WAGNER является мировым лидером в области распыления и окрашивания поверхностей. Наша миссия: мы окрашиваем, защищаем и делаем поверхности более функциональными.",
                         reply_markup=builder.as_markup())

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())