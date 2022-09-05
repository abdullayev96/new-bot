from telegram import ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup
import re
from menu import main_menu, send_my_info


def get_first_name(update, context):
    message = update.message.text
    context.user_data['first_name'] = message
    if context.user_data.get("edit_state"):
        context.user_data["edit_state"] = False
        context.user_data["state"] = 7
        send_my_info(update, context)

    else:
        context.user_data['state'] = 2
        update.message.reply_text(
            text=f"Enter Last Name!",
            reply_markup=ReplyKeyboardRemove()
        )


def get_last_name(update, context):
    message = update.message.text
    context.user_data['last_name'] = message
    if context.user_data.get("edit_state"):
        context.user_data["edit_state"] = False
        context.user_data["state"] = 7
        send_my_info(update, context)

    else:
        context.user_data['state'] = 3
        update.message.reply_text(
            text=f"Bugungi kundi kiriting!",
            reply_markup=ReplyKeyboardRemove()
        )


def get_day(update, context):
    message = update.message.text
    if re.search('^[0-9]+$', message):
        context.user_data['day'] = message
        if context.user_data.get("edit_state"):
            context.user_data["edit_state"] = False
            context.user_data["state"] = 7
            send_my_info(update, context)

        else:
            context.user_data['state'] = 4
            buttons = [
                [KeyboardButton(text="Male"), KeyboardButton(text="Female")]
            ]
            update.message.reply_text(
                text=f"Choose Your Gender!",
                reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
            )
    else:
        update.message.reply_text(
            text=f"Please Enter True Value!!!",
        )


def get_gender(update, context):
    message = update.message.text
    if re.search('^(Male|Female)$', message):
        context.user_data['gender'] = message
        if context.user_data.get("edit_state"):
            context.user_data["edit_state"] = False
            context.user_data["state"] = 7
            send_my_info(update, context)

        else:
            context.user_data['state'] = 5
            buttons = [
                [KeyboardButton(text="Share", request_contact=True)]
            ]
            update.message.reply_text(
                text=f"Share Your Contact Or Send It",
                reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
            )
    else:
        update.message.reply_text(
            text=f"Iltimos to'\g'ri kiriting!!!",
        )


def get_text_contact(update, context):
    message = update.message.text
    context.user_data["contact"] = message
    context.user_data['state'] = 7

    if context.user_data.get("edit_state"):
        context.user_data["edit_state"] = False
        send_my_info(update, context)

    else:
        context.user_data['state'] = 6
        buttons = [
            [KeyboardButton(text="Share", request_location=True)]
        ]
        location = update.message.location
        update.message.reply_location(
            buttons, resize_keyboard=True, one_time_keyboard=True,latitude=location.latitude, longitude=location.longutide
        )  ## bu locatsiya uchun

def get_text_location(update, context):
    user=update.message.from_user
    message = update.message.text
    context.user_data["location"] = message
    context.user_data['state'] = 7

    if context.user_data.get("edit_state"):
        context.user_data["edit_state"] = False
        send_my_info(update, context)
    else:
        main_menu(update, context, user.id)

