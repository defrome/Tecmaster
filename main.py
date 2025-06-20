import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
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

# Глобальная переменная для хранения ID последнего сообщения
last_message_id = None

cart = {}

products_list = [
            {"id": "1", "description": "Test"},
            {"id": "2", "description": "Test"},
            {"id": "3", "description": "Test"}
        ]

async def delete_previous_message(chat_id: int):
    global last_message_id
    if last_message_id:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=last_message_id)
        except Exception as e:
            logger.warning(f"Не удалось удалить сообщение: {e}")
        last_message_id = None

async def show_main_menu(message_or_callback, state: FSMContext):
    global last_message_id
    try:
        if isinstance(message_or_callback, types.CallbackQuery):
            await message_or_callback.answer()
            chat_id = message_or_callback.message.chat.id
            reply_method = message_or_callback.message.answer_photo
        else:
            chat_id = message_or_callback.chat.id
            reply_method = message_or_callback.answer_photo

        await state.clear()
        await delete_previous_message(chat_id)

        caption = (
            "   <b>TECMASTER</b> – символ передовых технологий в области механизированной окраски\n\n"
            "🔹 <i>Профессиональные решения</i> для любых задач\n"
            "🔹 <i>Доступные инструменты</i> для частных мастеров\n"
            "🔹 <i>Инновационные подходы</i> в нанесении покрытий\n\n"
            "Выберите интересующий раздел:"
        )

        msg = await reply_method(
            photo='AgACAgIAAxkBAANmaFRviIs0dpywgA9Fq9gY9yS6CNsAAgL6MRuMHKBKSVown6eez1wBAAMCAAN5AAM2BA',
            caption=caption,
            reply_markup=builder.as_markup(),
            parse_mode="HTML"
        )
        last_message_id = msg.message_id

    except Exception as e:
        logger.error(f"Main menu error: {e}")
        error_msg = "⚠️ Произошла ошибка. Пожалуйста, попробуйте позже."
        if isinstance(message_or_callback, types.CallbackQuery):
            await message_or_callback.message.answer(error_msg, reply_markup=builder.as_markup())
        else:
            await message_or_callback.answer(error_msg)

# Обработчики

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    # Создаем fake callback объект для передачи в handle_home
    class FakeCallback:
        def __init__(self, message):
            self.message = message
            self.data = "home"
            self.from_user = message.from_user

        async def answer(self):
            pass

    await handle_home(FakeCallback(message), state)


@dp.callback_query(F.data == "home")
async def handle_home(callback: types.CallbackQuery, state: FSMContext):
    global last_message_id
    try:
        await callback.answer()
        await state.clear()
        await delete_previous_message(callback.message.chat.id)

        caption = (
            "   <b>TECMASTER</b> – символ передовых технологий в области механизированной окраски\n\n"
            "🔹 <i>Профессиональные решения</i> для любых задач\n"
            "🔹 <i>Доступные инструменты</i> для частных мастеров\n"
            "🔹 <i>Инновационные подходы</i> в нанесении покрытий\n\n"
            "Выберите интересующий раздел:"
        )

        msg = await callback.message.answer_photo(
            photo='AgACAgIAAxkBAANmaFRviIs0dpywgA9Fq9gY9yS6CNsAAgL6MRuMHKBKSVown6eez1wBAAMCAAN5AAM2BA',
            caption=caption,
            reply_markup=builder.as_markup(),
            parse_mode="HTML"
        )
        last_message_id = msg.message_id

    except Exception as e:
        logger.error(f"Home error: {e}")
        await callback.message.answer(
            "⚠️ Произошла ошибка при загрузке главного меню. Пожалуйста, попробуйте позже.",
            reply_markup=builder.as_markup()
        )


@dp.callback_query(F.data == "catalog")
async def handle_catalog(callback: types.CallbackQuery, state: FSMContext):
    global last_message_id
    try:
        await callback.answer()
        await state.clear()
        await delete_previous_message(callback.message.chat.id)

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

        msg = await callback.message.answer(
            text="<b>🏗 Каталог оборудования Wagner</b>\n\n"
                 "Выберите категорию оборудования:",
            reply_markup=builder.as_markup(),
            parse_mode="HTML"
        )
        last_message_id = msg.message_id

        await state.set_state(CatalogStates.viewing_catalog)

    except Exception as e:
        logger.error(f"Catalog error: {e}")
        await callback.message.answer("⚠️ Ошибка загрузки каталога. Попробуйте позже.")


pro_products = [
    {
        "id": "pro1",
        "name": "Профессиональный окрасочный аппарат X500",
        "price": 125000,
        "description": "Мощный аппарат для профессионального использования"
    },
    {
        "id": "pro2",
        "name": "Промышленный распылитель W850",
        "price": 189000,
        "description": "Высокопроизводительный распылитель для промышленных работ"
    },
    {
        "id": "pro3",
        "name": "Компрессорная станция PRO-3000",
        "price": 235000,
        "description": "Профессиональная компрессорная станция"
    }
]

home_products = [
    {
        "id": "1",
        "name": "Домашний окрасочный аппарат X500",
        "price": 125000,
        "description": "Мощный аппарат для профессионального использования"
    },
    {
        "id": "2",
        "name": "Промышленный распылитель W850",
        "price": 189000,
        "description": "Высокопроизводительный распылитель для промышленных работ"
    },
    {
        "id": "3",
        "name": "Компрессорная станция PRO-3000",
        "price": 235000,
        "description": "Профессиональная компрессорная станция"
    }
]


@dp.callback_query(F.data == 'catalog:pro')
async def get_home_catalog(callback: types.CallbackQuery, state: FSMContext):
    global last_message_id
    try:
        await callback.answer()
        await state.clear()
        await delete_previous_message(callback.message.chat.id)

        builder = InlineKeyboardBuilder()

        # Используем глобальный список продуктов
        for product in pro_products:
            builder.row(
                InlineKeyboardButton(
                    text=f"{product['name']} - {product['price']}₽",
                    callback_data=f"pro_product:{product['id']}"
                ),
                width=1
            )

        builder.row(
            InlineKeyboardButton(
                text="↩️ Назад в каталог",
                callback_data="catalog"
            ),
            InlineKeyboardButton(
                text="🏠 На главную",
                callback_data="home"
            ),
            width=2
        )

        msg = await callback.message.answer(
            text="<b>🔧 Профессиональное оборудование</b>\n\n"
                 "Выберите товар из категории:",
            reply_markup=builder.as_markup(),
            parse_mode="HTML"
        )
        last_message_id = msg.message_id

        await state.set_state(CatalogStates.viewing_pro_category)
        await state.update_data(category="pro", products=pro_products)

    except Exception as e:
        logger.error(f"Home catalog error: {e}", exc_info=True)
        await callback.message.answer(
            "⚠️ Произошла ошибка при загрузке каталога",
            reply_markup=back.as_markup()
        )

@dp.callback_query(F.data == 'catalog:home')
async def get_home_catalog(callback: types.CallbackQuery, state: FSMContext):
    global last_message_id
    try:
        await callback.answer()
        await state.clear()
        await delete_previous_message(callback.message.chat.id)

        builder = InlineKeyboardBuilder()

        # Используем глобальный список продуктов
        for product in home_products:
            builder.row(
                InlineKeyboardButton(
                    text=f"{product['name']} - {product['price']}₽",
                    callback_data=f"home_product:{product['id']}"
                ),
                width=1
            )

        builder.row(
            InlineKeyboardButton(
                text="↩️ Назад в каталог",
                callback_data="catalog"
            ),
            InlineKeyboardButton(
                text="🏠 На главную",
                callback_data="home"
            ),
            width=2
        )

        msg = await callback.message.answer(
            text="<b>🔧 Профессиональное оборудование</b>\n\n"
                 "Выберите товар из категории:",
            reply_markup=builder.as_markup(),
            parse_mode="HTML"
        )
        last_message_id = msg.message_id

        await state.set_state(CatalogStates.viewing_pro_category)
        await state.update_data(category="home", products=home_products)

    except Exception as e:
        logger.error(f"Home catalog error: {e}", exc_info=True)
        await callback.message.answer(
            "⚠️ Произошла ошибка при загрузке домашнего каталога",
            reply_markup=back.as_markup()
        )


@dp.callback_query(F.data.startswith('pro_product:'))
async def handle_product(callback: types.CallbackQuery, state: FSMContext):
    global last_message_id
    try:
        await callback.answer()
        await state.clear()
        await delete_previous_message(callback.message.chat.id)

        product_id = callback.data.split(':')[1]
        product = next((p for p in pro_products if p['id'] == product_id), None)

        if not product:
            await callback.message.answer("Товар не найден")
            return

        builder = InlineKeyboardBuilder()


        builder.row(
            InlineKeyboardButton(
                text='🛒 Добавить в корзину',
                callback_data=f"add_to_cart:{product['id']}"
            ),
            width=1
        )

        builder.row(
            InlineKeyboardButton(
                text="↩️ Назад в каталог",
                callback_data="catalog:pro"  # Возврат в нужный каталог
            ),
            InlineKeyboardButton(
                text="🏠 На главную",
                callback_data="home"
            ),
            width=2
        )

        product_info = (
            f"<b>{product['name']}</b>\n\n"
            f"💵 Цена: {product['price']}₽\n"
            f"📦 Артикул: {product['id']}\n\n"
            f" Характеристики: {product['description']}\n\n"
        )

        msg = await callback.message.answer(
            text=product_info,
            reply_markup=builder.as_markup(),
            parse_mode="HTML"
        )
        last_message_id = msg.message_id

        await state.set_state(CatalogStates.viewing_item)
        await state.update_data(current_product=product)

    except Exception as e:
        logger.error(f"Product error: {e}", exc_info=True)
        await callback.message.answer(
            "⚠️ Произошла ошибка при загрузке товара",
            reply_markup=back.as_markup()
        )


@dp.callback_query(F.data.startswith('home_product:'))
async def handle_product(callback: types.CallbackQuery, state: FSMContext):
    global last_message_id
    try:
        await callback.answer()
        await state.clear()
        await delete_previous_message(callback.message.chat.id)

        product_id = callback.data.split(':')[1]
        product = next((p for p in home_products if p['id'] == product_id), None)

        if not product:
            await callback.message.answer("Товар не найден")
            return

        builder = InlineKeyboardBuilder()


        builder.row(
            InlineKeyboardButton(
                text='🛒 Добавить в корзину',
                callback_data=f"add_to_cart:{product['id']}"
            ),
            width=1
        )

        builder.row(
            InlineKeyboardButton(
                text="↩️ Назад в каталог",
                callback_data="catalog:home"  # Возврат в нужный каталог
            ),
            InlineKeyboardButton(
                text="🏠 На главную",
                callback_data="home"
            ),
            width=2
        )

        product_info = (
            f"<b>{product['name']}</b>\n\n"
            f"💵 Цена: {product['price']}₽\n"
            f"📦 Артикул: {product['id']}\n\n"
            f" Характеристики: {product['description']}\n\n"
        )

        msg = await callback.message.answer(
            text=product_info,
            reply_markup=builder.as_markup(),
            parse_mode="HTML"
        )
        last_message_id = msg.message_id

        await state.set_state(CatalogStates.viewing_item)
        await state.update_data(current_product=product)

    except Exception as e:
        logger.error(f"Product error: {e}", exc_info=True)
        await callback.message.answer(
            "⚠️ Произошла ошибка при загрузке товара",
            reply_markup=back.as_markup()
        )



@dp.callback_query(F.data == "about")
async def handle_about(callback: types.CallbackQuery, state: FSMContext):
    global last_message_id
    try:
        await callback.answer()
        await state.clear()
        await delete_previous_message(callback.message.chat.id)

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

        msg = await callback.message.answer(
            text=about_text,
            reply_markup=back.as_markup(),
            parse_mode="HTML"
        )
        last_message_id = msg.message_id

    except Exception as e:
        logger.error(f"About error: {e}")
        await callback.message.answer("⚠️ Ошибка загрузки страницы. Попробуйте позже.")


@dp.callback_query(F.data == "cart")
async def handle_cart(callback: types.CallbackQuery, state: FSMContext):
    global last_message_id
    try:
        await callback.answer()
        await state.clear()
        await delete_previous_message(callback.message.chat.id)

        msg = await callback.message.answer(
            text="🛒 Ваша корзина пуста\n\n"
                 "Добавьте товары из каталога!",
            reply_markup=back.as_markup(),
            parse_mode="HTML"
        )
        last_message_id = msg.message_id

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


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())