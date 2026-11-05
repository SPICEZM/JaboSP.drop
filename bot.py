import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import web

# Токен подтягивается из настроек Render (Environment Variables)
TOKEN = os.getenv("BOT_TOKEN", "ВСТАВЬ_ТОКЕН_ЕСЛИ_ТЕСТИРУЕШЬ_ЛОКАЛЬНО")

# Твой юзернейм в Telegram без собачки @ (для кнопки заказа)
MANAGER_USERNAME = "spaysikzm"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- КЛАВИАТУРЫ ---
def main_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📂 Каталог ботов и цены", callback_data="catalog")],
        [InlineKeyboardButton(text="💬 Связаться / Заказать", url=f"https://t.me/{MANAGER_USERNAME}")]
    ])

def catalog_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🤖 Бот-визитка / Портфолио — от 1 500 ₽", callback_data="item_card")],
        [InlineKeyboardButton(text="🛒 Магазин с автооплатой — от 4 000 ₽", callback_data="item_shop")],
        [InlineKeyboardButton(text="🎮 Игровой / Развлекательный бот — от 3 000 ₽", callback_data="item_game")],
        [InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="back_home")]
    ])

def back_to_catalog_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Заказать такого бота", url=f"https://t.me/{MANAGER_USERNAME}")],
        [InlineKeyboardButton(text="⬅️ Назад к каталогу", callback_data="catalog")]
    ])

# --- ОБРАБОТЧИКИ КОМАНД И КНОПОК ---
@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "👋 **Привет! Добро пожаловать в Магазин Ботов.**\n\n"
        "Я разрабатываю быстрых и удобных Telegram-ботов под ключ: от простых визиток до магазинов и игровых систем.\n\n"
        "Выбери нужный раздел ниже:",
        reply_markup=main_menu_kb(),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "catalog")
async def show_catalog(call: CallbackQuery):
    await call.message.edit_text(
        "📋 **Каталог услуг и прайс-лист:**\n\n"
        "Нажми на интересующий вариант, чтобы посмотреть подробности:",
        reply_markup=catalog_kb(),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "item_card")
async def item_card_info(call: CallbackQuery):
    await call.message.edit_text(
        "🤖 **Бот-визитка / Портфолио**\n"
        "💰 **Цена:** от 1 500 ₽\n"
        "⏱ **Сроки:** 1–2 дня\n\n"
        "Идеально для фрилансеров и авторов. Включает интерактивное меню, ответы на частые вопросы, прайс-лист и прямую связь с клиентом.",
        reply_markup=back_to_catalog_kb(),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "item_shop")
async def item_shop_info(call: CallbackQuery):
    await call.message.edit_text(
        "🛒 **Telegram-магазин с корзиной**\n"
        "💰 **Цена:** от 4 000 ₽\n"
        "⏱ **Сроки:** 3–5 дней\n\n"
        "Полноценный каталог товаров, админ-панель для добавления позиций, выдача цифровых товаров и подключение оплаты (СБП, карты, крипта).",
        reply_markup=back_to_catalog_kb(),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "item_game")
async def item_game_info(call: CallbackQuery):
    await call.message.edit_text(
        "🎮 **Игровой / Чат-бот**\n"
        "💰 **Цена:** от 3 000 ₽\n"
        "⏱ **Сроки:** от 2 дней\n\n"
        "Боты для бесед, мини-игры, генераторы контента, привязка к игровым серверам и нестандартная механика под твоё ТЗ.",
        reply_markup=back_to_catalog_kb(),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "back_home")
async def go_home(call: CallbackQuery):
    await call.message.edit_text(
        "👋 **Главное меню Магазина Ботов.**\n\n"
        "Выбери нужный раздел ниже:",
        reply_markup=main_menu_kb(),
        parse_mode="Markdown"
    )

# --- ВЕБ-СЕРВЕР ДЛЯ RENDER (ЧТОБЫ НЕ ПАДАЛ ПО ТАЙМАУТУ ПОРТА) ---
async def handle_ping(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

# --- ЗАПУСК ---
async def main():
    await start_web_server()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
