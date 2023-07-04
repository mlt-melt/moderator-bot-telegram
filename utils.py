import time
from config import db, bot, sendMessage
from aiogram import types
from textsConfig import *
import re

async def is_admin(message):
    userStatus = await bot.get_chat_member(message.chat.id, message.from_user.id)
    return userStatus["status"] in ['administrator', 'creator']

def dateToStr(date):
    # date in format "days:hours:minutes"
    days, hours, minutes = date.split(':')
    result = ''
    if days != "0":
        result += f'{days} days '
    if hours != "0":
        result += f'{hours} hours '
    if minutes != "0":
        result += f'{minutes} minutes '
    return result

def secondsToDateStr(seconds):
    # time in seconds 
    result = ''
    days, hours, minutes = [0, 0, 0]

    if seconds > 86400:
        days = seconds // 86400
        result += f'{days}:'
    else:
        result += f'0:'

    if seconds > 3600:
        hours = (seconds - (days * 86400)) // 3600
        result += f'{hours}:'
    else:
        result += f'0:'
    
    if seconds > 60:
        minutes = (seconds - ((days * 86400) + (hours * 3600))) // 60
        result += f'{minutes}'
    else:
        result += f'0'
    
    if result != "0:0:0":
        return dateToStr(result)
    else:
        return f"{seconds} seconds "


def formatMsg(reason, timeToPunishment, message: types.Message):
    if timeToPunishment != 0:
        if reason == "contentType":
            return banContentText.replace("{contentType}", f"<b>{message.content_type}</b>").replace("{username}", f"<b>{message.from_user.mention}</b>").replace("{banTime}", dateToStr(timeToPunishment))
        else:
            return banWordText.replace("{username}", f"<b>{message.from_user.mention}</b>").replace("{banTime}", dateToStr(timeToPunishment))
    else:
        if reason == "contentType":
            return warningContentText.replace("{contentType}", f"<b>{message.content_type}</b>").replace("{username}", f"<b>{message.from_user.mention}</b>")
        else:
            return warningWordText.replace("{username}", f"<b>{message.from_user.mention}</b>")

def formatLog(reason, timeToPunishment, message: types.Message):
    if timeToPunishment != 0:
        if reason == "contentType":
            return f'chat {message.chat.id} | User {message.from_user.id} ({message.from_user.mention}) has been banned for {dateToStr(timeToPunishment)}. Reason - {message.content_type} sent'
        else:
            return f'chat {message.chat.id} | User {message.from_user.id} ({message.from_user.mention}) has been banned for {dateToStr(timeToPunishment)}. Reason - banword sent ({message.text})'
    else:
        if reason == "contentType":
            return f'chat {message.chat.id} | User {message.from_user.id} has been warned. Reason - {message.content_type} sent'
        else:
            return f'chat {message.chat.id} | User {message.from_user.id} has been warned. Reason - banword sent ({message.text})'


def addToStatistics(reason, timeToPunishment, message: types.Message, punishment):
    user_id = message.from_user.id
    chat_id = message.chat.id
    if reason == "contentType":
        reasonExplanation = message.content_type
    else:
        reasonExplanation = message.text
    violationDate = time.time()
    if punishment == "ban":
        wasMessageSent = sendMessage
    else:
        wasMessageSent = False

    db.add_to_stat(user_id, chat_id, reason, reasonExplanation, punishment, timeToPunishment, violationDate, wasMessageSent)


def replaceModerationText(text):
    banwords = db.get_banwords()
    newText = text.lower().replace(" ", "")
    if bool(re.search('(?:{})'.format('|'.join(banwords)), newText, flags=re.I)):
        return True
    
    replaceList = [(" ", ""), ("sh", "ш"), ("ch", "ч"), ('ⓒⓗ', 'ч'), ('ⓢⓗ', 'ш'), ("s", "с"), ("c", "с"), ("$", "с"), ("@", "а"),
                   ("3", "э"), ("e", "е"), ("r", "р"), ("t", "т"), ("u", "у"), ("o", "о"), ("p", "р"), ("a", "а"),
                   ("d", "д"), ("f", "ф"), ("g", "г"), ("h", "х"), ("j", "дж"), ("l", "л"), ("v", "в"), ("b", "б"),
                   ("n", "п"), ("m", "м"), ("x", "х"), ('ⓐ', 'а'), ("k", "к"), ("4", "ч"), ("z", "з"), ("3", "з"),
                   ('ⓑ', 'б'), ('ⓥ', 'в'), ('ⓖ', 'г'), ('ⓓ', 'д'), ('ⓔ', 'е'), ('ⓙ', 'ж'), ('ⓩ', 'з'), ('ⓘ', 'и'),
                   ('ⓨ', 'й'), ('ⓚ', 'к'), ('ⓛ', 'л'), ('ⓜ', 'м'), ('ⓝ', 'н'), ('ⓞ', 'о'), ('ⓟ', 'п'), ('ⓡ', 'р'),
                   ('ⓢ', 'с'), ('ⓣ', 'т'), ('ⓤ', 'у'), ('ⓕ', 'ф'), ('ⓗ', 'х'), ('【', ''), ('】', ''), ('ᚣ', 'а'),
                   ('ƃ', 'б'), ('ᛒ', 'в'), ('ᛚ', 'г'), ('ᚦ', 'д'), ('ᛊ', 'е'), ('ᛊ', 'ё'), ('ᛯ', 'ж'), ('℥', 'з'), ('ᛋ', 'и'),
                   ('ᛋ', 'й'), ('ᛕ', 'к'), ('ᚳ', 'л'), ('ᛖ', 'м'), ('ᚺ', 'н'), ('ᛟ', 'о'), ('ᚢ', 'п'), ('ᚹ', 'р'), ('ᛈ', 'с'),
                   ('ᛠ', 'т'), ('ᚴ', 'у'), ('ᛄ', 'ф'), ('ᚷ', 'х'), ('ᛪ', 'ц'), ('ᚶ', 'ч'), ('Ⱎ', 'ш'), ('Ⱎ', 'щ'), ('ᛧ', 'ъ'),
                   ('ᛧ', 'ы'), ('Ⱃ', 'ь'), ('Ⱃ', 'э'), ('ᛆ', 'ю'), ('Ⱃ', 'я')]
    newText = text.lower()
    for i in replaceList:
        newText = newText.replace(i[0], i[1])
    if bool(re.search('(?:{})'.format('|'.join(banwords)), newText, flags=re.I)):
        return True
    
    replaceList = [(" ", ""), ("с", "c"), ("$", "s"), ("@", "a"), ("к", "k"), ("4", "ch"), ("з", "z"), ("е", "e"), ("ч", "ch"),
                   ("р", "r"), ("т", "t"), ("у", "u"), ("о", "o"), ("р", "r"), ("а", "a"), ("д", "d"), ("ф", "f"),
                   ("г", "g"), ("х", "x"), ("л", "l"), ("в", "v"), ("б", "b"), ("п", "n"), ("м", "m"), ("ш", "sh"),
                   ('ⓐ', 'a'), ('ⓑ', 'b'), ('ⓒ', 'c'), ('ⓓ', 'd'), ('ⓔ', 'e'), ('ⓕ', 'f'), ('ⓖ', 'g'), ('ⓗ', 'h'),
                   ('ⓘ', 'i'), ('ⓙ', 'j'), ('ⓚ', 'k'), ('ⓛ', 'l'), ('ⓜ', 'm'), ('ⓝ', 'n'), ('ⓞ', 'o'), ('ⓟ', 'p'),
                   ('ⓠ', 'q'), ('ⓡ', 'r'), ('ⓢ', 's'), ('ⓣ', 't'), ('ⓤ', 'u'), ('ⓥ', 'v'), ('ⓦ', 'w'), ('ⓧ', 'x'),
                   ('ⓨ', 'y'), ('ⓩ', 'z'), ('₳', 'a'), ('฿', 'b'), ('₵', 'c'), ('Đ', 'd'), ('Ɇ', 'e'), ('₣', 'f'),
                   ('₲', 'g'), ('Ⱨ', 'h'), ('ł', 'i'), ('J', 'j'), ('₭', 'k'), ('Ⱡ', 'l'), ('₥', 'm'), ('₦', 'n'), ('Ø', 'o'),
                   ('₱', 'p'), ('Q', 'q'), ('Ɽ', 'r'), ('₴', 's'), ('₮', 't'), ('Ʉ', 'u'), ('V', 'v'), ('₩', 'w'), ('Ӿ', 'x'),
                   ('Ɏ', 'y'), ('Ⱬ', 'z'), ('𝕒', 'a'), ('𝕓', 'b'), ('𝕔', 'c'), ('𝕕', 'd'), ('𝕖', 'e'), ('𝕗', 'f'), ('𝕘', 'g'),
                   ('𝕙', 'h'), ('𝕚', 'i'), ('𝕛', 'j'), ('𝕜', 'k'), ('𝕝', 'l'), ('𝕞', 'm'), ('𝕟', 'n'), ('𝕠', 'o'), ('𝕡', 'p'),
                   ('𝕢', 'q'), ('𝕣', 'r'), ('𝕤', 's'), ('𝕥', 't'), ('𝕦', 'u'), ('𝕧', 'v'), ('𝕨', 'w'), ('𝕩', 'x'), ('𝕪', 'y'),
                   ('𝕫', 'z'), ('【', ''), ('】', ''), ('🅐', 'a'), ('🅑', 'b'), ('🅒', 'c'), ('🅓', 'd'), ('🅔', 'e'), ('🅕', 'f'),
                   ('🅖', 'g'), ('🅗', 'h'), ('🅘', 'i'), ('🅙', 'j'), ('🅚', 'k'), ('🅛', 'l'), ('🅜', 'm'), ('🅝', 'n'), ('🅞', 'o'),
                   ('🅟', 'p'), ('🅠', 'q'), ('🅡', 'r'), ('🅢', 's'), ('🅣', 't'), ('🅤', 'u'), ('🅥', 'v'), ('🅦', 'w'), ('🅧', 'x'),
                   ('🅨', 'y'), ('🅩', 'z'), ('🄰', 'a'), ('🄱', 'b'), ('🄲', 'c'), ('🄳', 'd'), ('🄴', 'e'), ('🄵', 'f'), ('🄶', 'g'),
                   ('🄷', 'h'), ('🄸', 'i'), ('🄹', 'j'), ('🄺', 'k'), ('🄻', 'l'), ('🄼', 'm'), ('🄽', 'n'), ('🄾', 'o'), ('🄿', 'p'),
                   ('🅀', 'q'), ('🅁', 'r'), ('🅂', 's'), ('🅃', 't'), ('🅄', 'u'), ('🅅', 'v'), ('🅆', 'w'), ('🅇', 'x'), ('🅈', 'y'),
                   ('🅉', 'z'), ('𝓪', 'a'), ('𝓫', 'b'), ('𝓬', 'c'), ('𝓭', 'd'), ('𝓮', 'e'), ('𝓯', 'f'), ('𝓰', 'g'), ('𝓱', 'h'),
                   ('𝓲', 'i'), ('𝓳', 'j'), ('𝓴', 'k'), ('𝓵', 'l'), ('𝓶', 'm'), ('𝓷', 'n'), ('𝓸', 'o'), ('𝓹', 'p'), ('𝓺', 'q'),
                   ('𝓻', 'r'), ('𝓼', 's'), ('𝓽', 't'), ('𝓾', 'u'), ('𝓿', 'v'), ('𝔀', 'w'), ('𝔁', 'x'), ('𝔂', 'y'), ('𝔃', 'z')]
    newText = text.lower()
    for i in replaceList:
        newText = newText.replace(i[0], i[1])
    if bool(re.search('(?:{})'.format('|'.join(banwords)), newText, flags=re.I)):
        return True
    
    return False