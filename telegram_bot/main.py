from telegram_bot.config import TOKEN
import logging
import datetime
import markups
from aiogram import Bot, Dispatcher, executor, types
from telegram_bot.sqlighter import SQLighter
import post_parser
import asyncio

# log level
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Connecting database
db = SQLighter('db.db')

last_kronbars_post_id = 0
last_itmostudents_post_id = 0
last_itmocareer_post_id = 0

@dp.message_handler(commands=['help'])
async def get_help(message: types.Message):
    await message.answer("\\subscribe - to start getting the newest post \n"
                         "\\unsubscribe - to stop mail merge \n"
                         "\\set_news - to choose the news you are interested in\n"
                         "\\sign_up - to taste your personal web interface and see monitoribale news ")

@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if db.user_is_banned(message.from_user.id, datetime.datetime.now()):
        await message.answer("You can't be subscribed because you were banned. Wait for some time and try again")
    else:
        if (not db.subscriber_exists(message.from_user.id)):
            db.add_subscriber(message.from_user.id, datetime.datetime.now())
        else:
            db.update_subscription(message.from_user.id, datetime.datetime.now(), status=True)
        await message.answer(
            "You'd been subscribed successfully.\nMy congratulations!\n\nNow you can choose some news. Use command /set_news")
    await check()


@dp.message_handler(commands=['set_news'])
async def set_news(message: types.Message):
    if db.user_subscribed(message.from_user.id):
        await message.answer("Click on the news you are interested in", reply_markup=markups.choice)
    await message.answer("Subscribe at first")

@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if db.user_subscribed(message.from_user.id):
        if (not db.subscriber_exists(message.from_user.id)):
            db.add_subscriber(message.from_user.id, datetime.datetime.now(), False)
            await message.answer("You hadn't been subscribed!")
        else:
            db.update_subscription(message.from_user.id, datetime.datetime.now(), False)
            await message.answer("You'd been unsubscribed and made admin upset successfully.\nGoodbye!")
    await message.answer("Subscribe at first")


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        "Welcome, sir! You're talking with parser bot.\nI can send actual news from itmo to you. Just /subscribe and let's get it started!")


@dp.message_handler(commands=['sign_up'])
async def sign_up(message: types.Message):
    if db.user_subscribed(message.from_user.id):
        await message.answer(
            f"Hey, you are an advanced user! Follow http://127.0.0.1:5000/sign_up to check your news subscriptions. Remember your id = {message.from_user.id}")
    await message.answer("Subscribe at first")


@dp.callback_query_handler(text="sport")
async def kronbars(call: types.CallbackQuery):
    if '0' in db.check_news_subscription(call.from_user.id, "Kronbars"):
        db.update_news_subscription(call.from_user.id, "Kronbars", True)
        await call.message.answer("You'd been subscribed on Kronbars news successfully")
    else:
        db.update_news_subscription(call.from_user.id, "Kronbars", False)
        await call.message.answer("You'd been unsubscribed from Kronbars news successfully")


@dp.callback_query_handler(text="itmo")
async def itmostudents(call: types.CallbackQuery):
    if '0' in db.check_news_subscription(call.from_user.id, "ItmoStudents"):
        db.update_news_subscription(call.from_user.id, "ItmoStudents", True)
        await call.message.answer("You'd been subscribed on ItmoStudents news successfully")
    else:
        db.update_news_subscription(call.from_user.id, "ItmoStudents", False)
        await call.message.answer("You'd been unsubscribed from ItmoStudents news successfully")


@dp.callback_query_handler(text="career")
async def itmocareer(call: types.CallbackQuery):
    if '0' in db.check_news_subscription(call.from_user.id, "ItmoCareer"):
        db.update_news_subscription(call.from_user.id, "ItmoCareer", True)
        await call.message.answer("You'd been subscribed on ItmoCareer news successfully")
    else:
        db.update_news_subscription(call.from_user.id, "ItmoCareer", False)
        await call.message.answer("You'd been unsubscribed from ItmoCareer news successfully")


@dp.callback_query_handler(text="sub_all")
async def sub_all(call: types.CallbackQuery):
    db.update_news_subscription(call.from_user.id, "ItmoCareer", True)
    db.update_news_subscription(call.from_user.id, "ItmoStudents", True)
    db.update_news_subscription(call.from_user.id, "Kronbars", True)
    await call.message.answer("You'd been subscribed on all news")


@dp.callback_query_handler(text="unsub_all")
async def unsub_all(call: types.CallbackQuery):
    db.update_news_subscription(call.from_user.id, "ItmoCareer", False)
    db.update_news_subscription(call.from_user.id, "ItmoStudents", False)
    db.update_news_subscription(call.from_user.id, "Kronbars", False)
    await call.message.answer("You'd been unsubscribed from all news")


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(
        "Remind you I'm just a bot. Use commands to contact with me.\n\help - to check the list of commands")


# @dp.message_handler()
# async def echo(message: types.Message):
#     media = types.MediaGroup()
#     if "bars".lower() in message.text:
#         post_id, post_text, post_img_url = parser.parse_kronbars()
#         media.attach_photo(post_img_url, post_text)
#     elif "itmo".lower() in message.text:
#         post_id, post_text, post_img_url = parser.parse_itmostudents()
#         media.attach_photo(post_img_url, post_text)
#     elif "car".lower() in message.text:
#         post_id, post_text, post_img_url = parser.parse_career_news()
#         media.attach_photo(post_img_url, post_text)
#     await message.answer_media_group(media=media)

async def check():
    # await asyncio.sleep(60)
    while (True):
        global last_kronbars_post_id
        global last_itmocareer_post_id
        global last_itmostudents_post_id

        post_id, post_text, post_img_url = post_parser.parse_kronbars()
        if post_id != last_kronbars_post_id:
            last_kronbars_post_id = post_id - 1
            for i in db.get_all_subscribers("Kronbars"):
                media = types.MediaGroup()
                media.attach_photo(post_img_url, post_text)
                await bot.send_photo(i[0], post_img_url, post_text)

        await asyncio.sleep(5)

        post_id, post_text, post_img_url = post_parser.parse_itmostudents()
        if post_id != last_itmostudents_post_id:
            last_itmostudents_post_id = post_id - 1
            for i in db.get_all_subscribers("ItmoStudents"):
                media = types.MediaGroup()
                media.attach_photo(post_img_url, post_text)
                await bot.send_photo(i[0], post_img_url, post_text)

        await asyncio.sleep(5)

        post_id, post_text, post_img_url = post_parser.parse_career_news()
        if post_id != last_itmocareer_post_id:
            last_itmocareer_post_id = post_id
            for i in db.get_all_subscribers("ItmoCareer"):
                media = types.MediaGroup()
                media.attach_photo(post_img_url, post_text)
                await bot.send_photo(i[0], post_img_url, post_text)
        await asyncio.sleep(20)


# async def check(user_id):
#     # await asyncio.sleep(60)
#     while(True):
#         global last_kronbars_post_id
#         global  last_itmocareer_post_id
#         global last_itmostudents_post_id
#         if 1 in db.check_news_subscription(user_id, "Kronbars"):
#             post_id, post_text, post_img_url = post_parser.parse_kronbars()
#             media = types.MediaGroup()
#             media.attach_photo(post_img_url, post_text)
#             if post_id != last_kronbars_post_id:
#                 last_kronbars_post_id = post_id
#                 await bot.send_photo(user_id, post_img_url, post_text)
#
#             await asyncio.sleep(5)
#         if 1 in db.check_news_subscription(user_id, "ItmoCareer"):
#             post_id, post_text, post_img_url = post_parser.parse_career_news()
#             media = types.MediaGroup()
#             media.attach_photo(post_img_url, post_text)
#             if post_id != last_itmocareer_post_id:
#                 last_itmocareer_post_id = post_id
#                 await bot.send_photo(user_id, post_img_url, post_text)
#             await asyncio.sleep(5)
#         if 1 in db.check_news_subscription(user_id, "ItmoStudents"):
#             post_id, post_text, post_img_url = post_parser.parse_itmostudents()
#             media = types.MediaGroup()
#             media.attach_photo(post_img_url, post_text)
#             if post_id != last_itmostudents_post_id:
#                 last_itmostudents_post_id = post_id
#                 await bot.send_photo(user_id, post_img_url, post_text)
#             await asyncio.sleep(5)
#         await asyncio.sleep(20)


# run long-polling
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
