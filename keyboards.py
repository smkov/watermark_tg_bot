from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

main_menu = ReplyKeyboardMarkup(
    [
        ['⚙️ Настроить водяной знак']
    ],
    resize_keyboard=False  # Make the keyboard smaller
)

mark_menu = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                "Создать",
                callback_data="create"
            )
        ]
    ])

settings_menu = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                "Светлый фон",
                callback_data='w_bg'
            ),
            InlineKeyboardButton(
                "Темный фон",
                callback_data='d_bg'
            )
        ],
[
            InlineKeyboardButton(
                "Редактировать",
                callback_data='edit'
            ),
            InlineKeyboardButton(
                "Канал",
                callback_data='channel'
            )
        ],
[
            InlineKeyboardButton(
                "Прозрачность",
                callback_data='opacity'
            ),
            InlineKeyboardButton(
                "Поворот",
                callback_data='rotate'
            )
        ],
[
            InlineKeyboardButton(
                "Расположение",
                callback_data='offset'
            ),
            InlineKeyboardButton(
                "Ширина",
                callback_data='width'
            )
        ],
[
            InlineKeyboardButton(
                "Сохранить",
                callback_data='Save'
            ),
            InlineKeyboardButton(
                "Назад",
                callback_data='Back'
            )
        ]
    ],
)