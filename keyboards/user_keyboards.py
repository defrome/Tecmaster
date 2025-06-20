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
