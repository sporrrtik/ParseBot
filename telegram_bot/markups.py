from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

choice = InlineKeyboardMarkup (
    inline_keyboard=[
        [
            InlineKeyboardButton(text = "Kronbars", callback_data="sport"),
            InlineKeyboardButton(text = "ItmoStudents", callback_data="itmo"),
            InlineKeyboardButton(text = "ItmoCareer", callback_data="career"),
        ],
        [
            InlineKeyboardButton(text = "Sub all", callback_data="sub_all"),
            InlineKeyboardButton(text = "Unsub all", callback_data="unsub_all")
        ]
    ]
)