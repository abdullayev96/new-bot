from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, ConversationHandler
from telegram import (
    InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, ChatAction
)
import re
import register
from menu import main_menu, send_my_info


states = {
    "first_name": 1,
    "last_name": 2,
    "day": 3,
    "gender": 4,
    "contact": 5,
    "location":6,
    "inline": 7
}


def start_handler(update, context):
    user = update.message.from_user
    update.message.reply_chat_action(action=ChatAction.TYPING)
    if context.user_data.get("first_name"):
        main_menu(update, context, user.id)
    else:
        context.user_data['state'] = 1
        update.message.reply_text(
            text=f"Enter First Name",
            reply_markup=ReplyKeyboardRemove()

        )


def message_handler(update, context):
    message = update.message.text
    state = context.user_data.get("state", 0)

    if state == 1:
        register.get_first_name(update, context)

    elif state == 2:
        register.get_last_name(update, context)

    elif state == 3:
        register.get_day(update, context)

    elif state == 4:
        register.get_gender(update, context)

    elif state == 5:
        register.get_text_contact(update, context)

    elif state == 6:
        register.get_text_location(update, context)

    elif state == 7:
        if message == "Manager":
            pass
        elif message == "My Info":
            send_my_info(update, context)
        elif message == "Mechanic":
            pass
        elif message == "Worker":
            pass
        elif message == "Organizations":
            pass

def contact_handler(update, context):
    state = context.user_data.get("state", 0)
    user = update.message.from_user
    if state == 5:
        context.user_data["contact"] = update.message.contact.phone_number
        context.user_data['state'] = 7
        main_menu(update, context, user.id)

def location_handler(update, context):
    print(update.message.location)
    state = context.user_data.get("state", 0)
    user = update.message.from_user
    if state == 6:
        context.user_data["contact"] =update.message.location
        context.user_data['state'] = 7
        main_menu(update, context, user.id)



def inline_handler(update, context):

    query = update.callback_query

    if query.data == "edit_data":
        buttons = [
            [
                InlineKeyboardButton(text="First Name", callback_data="edit_first_name"),
                InlineKeyboardButton(text="Last Name", callback_data="edit_last_name"),
            ],
            [
                InlineKeyboardButton(text="Age", callback_data="edit_age"),
                InlineKeyboardButton(text="Gender", callback_data="edit_gender"),
            ],
            [
                InlineKeyboardButton(text="Contact", callback_data="edit_contact"),
                InlineKeyboardButton(text="Location", callback_data="edit_location")
            ],

        ]
        query.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif query.data == "edit_first_name":
        query.message.edit_text("Enter First Name!")
        context.user_data['edit_state'] = True
        context.user_data['state'] = 1

    elif query.data == "edit_last_name":
        query.message.edit_text("Enter Last Name!")
        context.user_data['edit_state'] = True
        context.user_data['state'] = 2

    elif query.data == "edit_age":
        query.message.edit_text("Enter Age!")
        context.user_data['edit_state'] = True
        context.user_data['state'] = 3

    elif query.data == "edit_gender":
        buttons = [
            [KeyboardButton(text="Male"), KeyboardButton(text="Female")]
        ]
        context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
        query.message.reply_text(text="Choose Your Gender!", reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True))
        context.user_data['edit_state'] = True
        context.user_data['state'] = 4

    elif query.data == "edit_contact":
        buttons = [
            [KeyboardButton(text="Share", request_contact=True)]
        ]
        context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
        query.message.reply_text("Share Your Contact Or Send It!", reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True))
        context.user_data['edit_state'] = True
        context.user_data['state'] = 5

    elif query.data == "edit_location":
        buttons = [
            [KeyboardButton(text="Share", request_location=True)]
        ]
        context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
        query.message.reply_text("Share Your Location Or Send It!",reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True,one_time_keyboard=True))
        context.user_data['edit_state'] = True
        context.user_data['state'] = 6


    elif query.data == "main_menu":
        context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
        main_menu(update, context, query.message.chat_id)


def main():
    updater = Updater("1828443311:AAFC_9GaPz03an-SZrGpaBWsaONDmJt9xzM")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_handler))
    dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
    dispatcher.add_handler(MessageHandler(Filters.contact, contact_handler))
    dispatcher.add_handler(MessageHandler(Filters.location, location_handler))

    dispatcher.add_handler(CallbackQueryHandler(inline_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
