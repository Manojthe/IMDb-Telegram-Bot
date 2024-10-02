# membership.py

import telebot
from info import CHANNEL_1, CHANNEL_2  # Import the channel variables

def is_user_member(bot, chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Error checking membership: {e}")
        return False

def check_membership(bot, message):
    user_id = message.from_user.id

    # Check membership in both channels using user_id
    is_member_channel_1 = is_user_member(bot, CHANNEL_1, user_id)
    is_member_channel_2 = is_user_member(bot, CHANNEL_2, user_id)

    if is_member_channel_1 and is_member_channel_2:
        return None  # User is a member of both channels
    else:
        missing_channels = []
        if not is_member_channel_1:
            missing_channels.append(CHANNEL_1)
        if not is_member_channel_2:
            missing_channels.append(CHANNEL_2)

        return missing_channels
