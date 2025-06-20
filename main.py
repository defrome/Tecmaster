import asyncio
import logging
from typing import Dict, List

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.handlers import message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dataclasses import dataclass
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.user_keyboards import builder, back
from states.states import CatalogStates, CartStates

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token="7783836620:AAEKekan25gE2N6UOw3_xMWaHDVUSEh_Gc0")
dp = Dispatcher()

@dataclass
class CartItem:
    product_id: int
    name: str
    price: float
    quantity: int

user_carts: Dict[int, List[CartItem]] = {}


# Обработчики
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    try:
        caption = (
            "   <b>TECMASTER</b> – символ передовых технологий в области механизированной окраски\n\n"
            "🔹 <i>Профессиональные решения</i> для любых задач\n"
            "🔹 <i>Доступные инструменты</i> для частных мастеров\n"
            "🔹 <i>Инновационные подходы</i> в нанесении покрытий\n\n"
            "Выберите интересующий раздел:"
        )

        await message.answer_photo(
            photo='AgACAgIAAxkBAANmaFRviIs0dpywgA9Fq9gY9yS6CNsAAgL6MRuMHKBKSVown6eez1wBAAMCAAN5AAM2BA',
            caption=caption,
            reply_markup=builder.as_markup(),
            parse_mode="HTML"
        )

        await message.answer(
            "💡 <b>Новым клиентам скидка 10% по промокоду:</b> <code>WELCOME10</code>",
            parse_mode="HTML"
        )

    except Exception as e:
        logger.error(f"Start command error: {e}")
        await message.answer("⚠️ Произошла ошибка. Пожалуйста, попробуйте позже.")


@dp.callback_query(F.data == "home")
async def handle_home(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.answer()  # Подтверждаем получение callback

        # Очищаем состояние
        await state.clear()

        caption = (
            "   <b>TECMASTER</b> – символ передовых технологий в области механизированной окраски\n\n"
            "🔹 <i>Профессиональные решения</i> для любых задач\n"
            "🔹 <i>Доступные инструменты</i> для частных мастеров\n"
            "🔹 <i>Инновационные подходы</i> в нанесении покрытий\n\n"
            "Выберите интересующий раздел:"
        )

        await callback.message.answer_photo(
            photo='AgACAgIAAxkBAANmaFRviIs0dpywgA9Fq9gY9yS6CNsAAgL6MRuMHKBKSVown6eez1wBAAMCAAN5AAM2BA',
            caption=caption,
            reply_markup=builder.as_markup(),
            parse_mode="HTML"
        )


    except Exception as e:
        logger.error(f"Home error: {e}")
        await callback.message.answer(
            "⚠️ Произошла ошибка при загрузке главного меню. Пожалуйста, попробуйте позже.",
            reply_markup=builder.as_markup()
        )


@dp.callback_query(F.data == "catalog")
async def handle_catalog(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        await state.clear()

        builder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardButton(
                text="🔧 Профессиональное оборудование",
                callback_data="catalog:pro"
            ),
            width=1
        )
        builder.row(
            InlineKeyboardButton(
                text="🏠 Бытовые решения",
                callback_data="catalog:home"
            ),
            width=1
        )
        builder.row(
            InlineKeyboardButton(
                text="🏭 Промышленные системы",
                callback_data="catalog:industrial"
            ),
            width=1
        )
        builder.row(
            InlineKeyboardButton(
                text="🔍 Поиск по каталогу",
                switch_inline_query_current_chat=""
            ),
            InlineKeyboardButton(
                text="↩️ Назад",
                callback_data="home"
            )
        )

        # Проверяем тип сообщения перед редактированием
        if callback.message.content_type == "text":
            await callback.message.edit_text(
                text="<b>🏗 Каталог оборудования Wagner</b>\n\n"
                     "Выберите категорию оборудования:",
                reply_markup=builder.as_markup(),
                parse_mode="HTML"
            )
        else:
            await callback.message.answer(
                text="<b>🏗 Каталог оборудования Wagner</b>\n\n"
                     "Выберите категорию оборудования:",
                reply_markup=builder.as_markup(),
                parse_mode="HTML"
            )

        await state.set_state(CatalogStates.viewing_catalog)

    except Exception as e:
        logger.error(f"Catalog error: {e}")
        await callback.message.answer("⚠️ Ошибка загрузки каталога. Попробуйте позже.")

async def add_to_cart(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()



@dp.callback_query(F.data == "about")
async def handle_about(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        await state.clear()

        about_text = (
            "Кто мы?\n\n"
            "В области промышленных решений мы предлагаем технологически совершенное оборудование "
            "и системы для нанесения жидких покрытий, порошковых покрытий и красок на различные поверхности. "
            "Профессионалы используют наши надежные и высокоэффективные аппараты, оснащенные самыми современными технологиями.\n\n"
            "Для любителей и мастеров компания Wagner производит широкий ассортимент удобной и многофункциональной "
            "продукции бытового сегмента для успешной реализации любых проектов.\n\n"
            "Мы устанавливаем новые стандартны в области обработки поверхностей. Благодаря инновационным и "
            "эффективным технологическим решениям, наша продукция является по настоящему полезной для клиентов."
        )

        if callback.message.content_type == "text":
            await callback.message.edit_text(
                text=about_text,
                reply_markup=back.as_markup(),
                parse_mode="HTML"
            )
        else:
            await callback.message.answer(
                text=about_text,
                reply_markup=back.as_markup(),
                parse_mode="HTML"
            )

    except Exception as e:
        logger.error(f"About error: {e}")
        await callback.message.answer("⚠️ Ошибка загрузки страницы. Попробуйте позже.")


@dp.callback_query(F.data == "cart")
async def handle_cart(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        await state.clear()
        if callback.message.content_type == "text":
            await callback.message.edit_text(
                text="🛒 Ваша корзина пуста\n\n"
                     "Добавьте товары из каталога!",
                reply_markup=back.as_markup(),
                parse_mode="HTML"
            )
        else:
            await callback.message.answer(
                text="🛒 Ваша корзина пуста\n\n"
                     "Добавьте товары из каталога!",
                reply_markup=back.as_markup(),
                parse_mode="HTML"
            )

        await state.set_state(CartStates.viewing_cart)


    except Exception as e:
        logger.error(f"Cart error: {e}")
        await callback.message.answer("⚠️ Ошибка загрузки корзины. Попробуйте позже.")


@dp.message(F.photo)
async def handle_photo(message: types.Message):
    try:
        file_id = message.photo[-1].file_id
        await message.answer(
            f"🖼 <b>Фото принято!</b>\n"
            f"🔑 <code>{file_id}</code> — твой file_id\n"
            f"Используй его для сохранения или пересылки!",
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Photo error: {e}")
        await message.answer("⚠️ Ошибка обработки фото. Попробуйте ещё раз.")

def get_cart_keyboard(cart_items: List[CartItem]):
    builder = InlineKeyboardBuilder()

    # Кнопки для каждого товара
    for item in cart_items:
        builder.row(
            InlineKeyboardButton(
                text=f"➖ {item.name}",
                callback_data=f"cart_decrease:{item.product_id}"
            ),
            InlineKeyboardButton(
                text=f"➕ {item.name}",
                callback_data=f"cart_increase:{item.product_id}"
            ),
            width=2
        )
        builder.row(
            InlineKeyboardButton(
                text=f"❌ Удалить {item.name}",
                callback_data=f"cart_remove:{item.product_id}"
            ),
            width=1
        )

    # Основные кнопки
    builder.row(
        InlineKeyboardButton(
            text="✅ Оформить заказ",
            callback_data="cart_checkout"
        ),
        width=1
    )
    builder.row(
        InlineKeyboardButton(
            text="↩️ Назад в каталог",
            callback_data="catalog"
        ),
        InlineKeyboardButton(
            text="🔄 Обновить корзину",
            callback_data="cart"
        ),
        width=2
    )

    return builder.as_markup()

def empty_cart_item(cart_items: List[CartItem]):
    builder = InlineKeyboardBuilder
    builder.row(
        InlineKeyboardButton(
            text='🛒 Перейти в каталог',
            callback_data='catalog'
        ),
        width=1
    )
    return builder.as_markup()

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())