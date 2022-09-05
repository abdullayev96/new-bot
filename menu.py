from telegram import (
    KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove,
    InlineKeyboardButton, InlineKeyboardMarkup
)


def main_menu(update, context, chat_id):
    buttons = [
        [
            KeyboardButton(text="Manager"), KeyboardButton(text="My Info"),
        ],
        [
            KeyboardButton(text="Mechanic"), KeyboardButton(text="Worker")
        ],
        [
            KeyboardButton(text="Organizations")
        ]
    ]
    context.bot.send_message(
        chat_id=chat_id,
        text="Main Menu",
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )


def send_my_info(update, context):
    data = context.user_data
    buttons = [
        [
            InlineKeyboardButton(text="Edit Data", callback_data="edit_data"),
        ],
        [
            InlineKeyboardButton(text="Main Menu", callback_data="main_menu"),
        ]
    ]
    msg = update.message.reply_text(
        text="🕓",
        reply_markup=ReplyKeyboardRemove(),
    )
    context.bot.delete_message(chat_id=update.message.chat_id, message_id=msg.message_id)
    update.message.reply_text(
        text=f"<b>First Name</b>: {data['first_name']}\n"
             f"<b>Last Name</b>:{data['last_name']}\n"
             f"<b>Age</b>: {data['day']}\n"
             f"<b>Gender</b>: {data['gender']}\n"
             f"<b>Phone Number</b>: {data['contact']}\n",
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="HTML"
    )