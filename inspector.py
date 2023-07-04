from config import dp, db, admins, bot, permitions, banSteps, sendMessage
from textsConfig import *
from utils import addToStatistics, is_admin, formatMsg, formatLog, replaceModerationText
from aiogram import types
import time
import logging
import os, os.path

if os.path.getsize("logs/logs.log") >= 52428800:
    filesCount = len([name for name in os.listdir('logs') if os.path.isfile(name)])
    os.rename('logs/logs.log', f'logs/logsOld{filesCount}.log')

logging.basicConfig(level=logging.INFO, filename="logs/logs.log", format="%(asctime)s | %(message)s")

@dp.message_handler(content_types=['audio', 'photo', 'voice', 'video', 'document', 'text', 'location', 'contact', 'sticker', 'poll'])
async def moderate(message: types.Message):
    user_id = message.from_user.id

    async def punish(reason):
        await bot.delete_message(message.chat.id, message.message_id)
        punishment = db.get_punishment(reason)
        timeToPunishment = 0
        if punishment == "ban":
            user_info = db.get_user_info(user_id)
            user_bans_count = user_info[1]
            timeToPunishment = banSteps[user_bans_count] if (user_bans_count < len(banSteps)) else (banSteps[-1])
            if timeToPunishment == 0:
                if sendMessage == True:
                    await message.answer(formatMsg(reason, timeToPunishment, message))
                logging.info(formatLog(reason, timeToPunishment, message))
            else:
                days, hours, minutes = timeToPunishment.split(':')
                untilDate = time.time() + (float(days) * 86400) + (float(hours) * 3600) + (float(minutes) * 60)

                await bot.restrict_chat_member(message.chat.id, user_id, permissions=permitions, until_date=untilDate)

                if sendMessage == True:
                    await message.answer(formatMsg(reason, timeToPunishment, message))
                logging.info(formatLog(reason, timeToPunishment, message))
            db.ban_user(user_id, user_info)
        addToStatistics(reason, timeToPunishment, message, punishment)
    
    if (str(message.chat.id), ) in db.get_chats():
        if user_id not in admins and not await is_admin(message):
            if (message.content_type, ) in db.get_permitions("restricted"):
                await punish("contentType")
            elif replaceModerationText(message.text):
                await punish("banWord")
        else:
            if "/unban" in message.text:
                user_id = message.text.split(" ")[1]
                await bot.promote_chat_member(message.chat.id, user_id)
                await message.answer(f"User has been unbaned")