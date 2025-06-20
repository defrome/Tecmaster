from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from main import CartItem

builder = InlineKeyboardBuilder()

# Основные кнопки (3 в ряд)
builder.row(
    InlineKeyboardButton(text="🔎 Каталог", callback_data="catalog"),
    InlineKeyboardButton(text="🛒 Корзина", callback_data="cart"),
    InlineKeyboardButton(text="ℹ️ О нас", callback_data="about"),
)

# Дополнительные кнопки (2 в ряд)
builder.row(
    InlineKeyboardButton(text="📞 Контакты", callback_data="contacts"),
    InlineKeyboardButton(text="🚀 Акции", callback_data="promo"),
)

# Кнопка с ссылкой (отдельный ряд)
builder.row(
    InlineKeyboardButton(text="🌐 Наш сайт", url="https://tecmaster.ru"),
)

back = InlineKeyboardBuilder()

back.row(
    InlineKeyboardButton(text='Назад', callback_data="home")
)


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