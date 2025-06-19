from aiogram.fsm.state import State, StatesGroup

# 1. Определяем состояния каталога
class CatalogStates(StatesGroup):
    viewing_catalog = State()  # Основное меню каталога
    browsing_category = State()  # Просмотр категории
    viewing_item = State()  # Детали товара
    in_search = State()  # Поиск по каталогу