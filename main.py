import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.types.user import User
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, PhotoSize, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards.user_keyboards import builder, back
from states.states import CatalogStates

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("httpx")
logger.setLevel(logging.WARNING)

# Объект бота
bot = Bot(token="7783836620:AAEKekan25gE2N6UOw3_xMWaHDVUSEh_Gc0")
# Диспетчер
dp = Dispatcher()

router = Router()

user_cart = {}

user = User

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("WAGNER — ТВОЙ ВЫСОКОТЕХНОЛОГИЧНЫЙ ПОМОЩНИК В МИРЕ ОКРАСКИ! 🚀\n\n"
                        "«Не просто красим — создаём совершенство!»",

                         reply_markup=builder.as_markup())

@dp.callback_query(F.data == "home")
async def handle_home(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text="WAGNER — ТВОЙ ВЫСОКОТЕХНОЛОГИЧНЫЙ ПОМОЩНИК В МИРЕ ОКРАСКИ! 🚀\n\n"
             "«Не просто красим — создаём совершенство!»",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

@dp.callback_query(F.data == "catalog")
async def handle_catalog(callback: types.CallbackQuery, state: FSMContext):
    try:
        # 1. Подтверждаем получение callback
        await callback.answer()

        # 2. Сбрасываем предыдущее состояние (если было)
        await state.clear()

        # 3. Создаем интерактивную клавиатуру каталога
        builder = InlineKeyboardBuilder()

        # Основные категории (3 кнопки в ряд)
        builder.row(
            types.InlineKeyboardButton(
                text="🔧 Профессиональное оборудование",
                callback_data="catalog:pro"
            ),
            types.InlineKeyboardButton(
                text="🏠 Бытовые решения",
                callback_data="catalog:home"
            ),
            types.InlineKeyboardButton(
                text="🏭 Промышленные системы",
                callback_data="catalog:industrial"
            ),
            width=1  # По 1 кнопке в строке
        )

        # Дополнительные действия
        builder.row(
            types.InlineKeyboardButton(
                text="🔍 Поиск по каталогу",
                switch_inline_query_current_chat=""
            ),
            types.InlineKeyboardButton(
                text="Назад",
                callback_data="home"
            )
        )

        # 4. Отправляем сообщение с меню
        await callback.message.edit_text(
            text="<b>🏗 Каталог оборудования Wagner</b>\n\n"
                 "Выберите категорию оборудования:",
            reply_markup=builder.as_markup(),
            parse_mode="HTML"
        )

        # 5. Записываем состояние просмотра каталога
        await state.set_state(CatalogStates.viewing_catalog)
        await state.update_data(last_message_id=callback.message.message_id)

    except Exception as e:
        logger.error(f"Catalog error: {e}")
        await callback.message.answer("⚠️ Ошибка загрузки каталога. Попробуйте позже.")


@dp.callback_query(F.data == "about")
async def handle_about(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.answer()

        await state.clear()

        await callback.message.edit_text(
            text="Кто мы? \n\nВ области промышленных решений мы предлагаем технологически совершенное оборудование и системы для нанесения жидких покрытий, порошковых покрытий и красок на различные поверхности. Профессионалы используют наши надежные и высокоэффективные аппараты, оснащенные самыми современными технологиями. Для любителей и мастеров компания Wagner производит широкий ассортимент удобной и многофункциональной продукции бытового сегмента для успешной реализации любых проектов. Мы устанавливаем новые стандартны в области обработки поверхностей. Благодаря инновационным и эффективным технологическим решениям, наша продукция является по настоящему полезной для клиентов.",
            reply_markup=back.as_markup(),
            parse_mode="HTML",
        )

    except Exception as e:
        logger.error(f"Catalog error: {e}")
        await callback.message.answer("⚠️ Ошибка загрузки страницы. Попробуйте позже.")


@dp.callback_query(F.data == "cart")
async def handle_cart(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text="В разработке",
        reply_markup=back.as_markup(),
        parse_mode="HTML",
    )




# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())