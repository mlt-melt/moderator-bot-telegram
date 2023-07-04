from config import dp, db, admins, bot
from textsConfig import *
from utils import dateToStr, secondsToDateStr
from aiogram import types
import time
from aiogram.dispatcher import FSMContext
from states import *

@dp.message_handler(commands='admin')
async def adminCmd(message: types.Message):
    if message.from_user.id in admins:
        mkp = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Banwords settings', callback_data='banwords')
        btn2 = types.InlineKeyboardButton('Manage content types', callback_data='contentType')
        btn3 = types.InlineKeyboardButton('Set punishment', callback_data='measure')
        btn4 = types.InlineKeyboardButton('Moderated chats', callback_data='setChats')
        btn5 = types.InlineKeyboardButton('Get statistics', callback_data='getStat')
        btn6 = types.InlineKeyboardButton('Get logs', callback_data='getLogs')
        mkp.add(btn1).add(btn2).add(btn3).add(btn4).add(btn5).add(btn6)
        await message.answer("You are in admin panel", reply_markup=mkp)

@dp.callback_query_handler(text='admin')
async def adminCall(call: types.CallbackQuery):
    if call.from_user.id in admins:
        await call.message.delete()
        mkp = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Banwords settings', callback_data='banwords')
        btn2 = types.InlineKeyboardButton('Manage content types', callback_data='contentType')
        btn3 = types.InlineKeyboardButton('Set punishment', callback_data='measure')
        btn4 = types.InlineKeyboardButton('Moderated chats', callback_data='setChats')
        btn5 = types.InlineKeyboardButton('Get statistics', callback_data='getStat')
        btn6 = types.InlineKeyboardButton('Get logs', callback_data='getLogs')
        mkp.add(btn1).add(btn2).add(btn3).add(btn4).add(btn5).add(btn6)
        await call.message.answer("You are in admin panel", reply_markup=mkp)


@dp.callback_query_handler(text='banwords')
async def banwordsCall(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("All banwords:")
    msg = ""
    for i in db.get_banwords():
        if len(msg) + len(f'{i}\n') >= 4096:
            await call.message.answer(msg)
            msg = ""
        msg += f'{i}\n'
    if len(msg) > 0:
        await call.message.answer(msg)

    mkp = types.InlineKeyboardMarkup()
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Add new banwords', callback_data='addBanwords')
    btn2 = types.InlineKeyboardButton('Delete banword', callback_data='delBanwords')
    btn3 = types.InlineKeyboardButton('Back to admin panel', callback_data='admin')
    mkp.add(btn1).add(btn2).add(btn3)
    await call.message.answer("Choose action", reply_markup=mkp)


@dp.callback_query_handler(text='cancel', state=AddBanwordsList.Text)
@dp.callback_query_handler(text='cancel', state=DelBanword.Text)
async def cancelToBanwordsCall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    try:
        await state.finish()
    except:
        pass
    await call.message.delete()
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Add new banwords', callback_data='addBanwords')
    btn2 = types.InlineKeyboardButton('Delete banword', callback_data='delBanwords')
    btn3 = types.InlineKeyboardButton('Back to admin panel', callback_data='admin')
    mkp.add(btn1).add(btn2).add(btn3)
    await call.message.answer("Choose action", reply_markup=mkp)


@dp.callback_query_handler(text='addBanwords')
async def addBanwordsListCall(call: types.CallbackQuery):
    await call.message.delete()
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Cancel', callback_data='cancel')
    mkp.add(btn1)
    await AddBanwordsList.Text.set()
    await call.message.answer("Send list with new banwords (each word must be on new line)", reply_markup=mkp)

@dp.message_handler(state=AddBanwordsList.Text)
async def addBanwordsListGo(message: types.Message, state: FSMContext):
    await state.finish()
    for i in message.text.split("\n"):
        db.add_banword(i.lower())
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Return', callback_data='admin')
    mkp.add(btn1)
    await message.answer("Banwords added. You can return to admin panel", reply_markup=mkp)


@dp.callback_query_handler(text='delBanwords')
async def delBanwordsCall(call: types.CallbackQuery):
    await call.message.delete()
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Cancel', callback_data='cancel')
    mkp.add(btn1)
    await DelBanword.Text.set()
    await call.message.answer("Send list with words you want to delete from banwords (each word must be on new line)", reply_markup=mkp)

@dp.message_handler(state=DelBanword.Text)
async def delBanwordsGo(message: types.Message, state: FSMContext):
    await state.finish()
    for i in message.text.split("\n"):
        db.del_banword(i)
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Return', callback_data='admin')
    mkp.add(btn1)
    await message.answer("Banwords deleted. You can return to admin panel", reply_markup=mkp)


@dp.callback_query_handler(text='contentType')
async def contentTypesCall(call: types.CallbackQuery):
    await call.message.delete()
    mkp = types.InlineKeyboardMarkup()
    for i in db.get_content_types():
        if i[1] == "allow":
            mkp.add(types.InlineKeyboardButton(f'✅ {i[0]} ✅', callback_data=f'restricted_{i[0]}'))
        else:
            mkp.add(types.InlineKeyboardButton(f'❌ {i[0]} ❌', callback_data=f'allow_{i[0]}'))
    mkp.add(types.InlineKeyboardButton('< Return >', callback_data='admin'))
    await call.message.answer("Choose which type of content will be allowed and which fordbidden", reply_markup=mkp)

@dp.callback_query_handler(text_contains='restricted_')
@dp.callback_query_handler(text_contains='allow_')
async def changePermitionCall(call: types.CallbackQuery):
    contentType = call.data.split('_')[1]
    db.change_permition(contentType, call.data.split('_')[0])
    mkp = types.InlineKeyboardMarkup()
    for i in db.get_content_types():
        if i[1] == "allow":
            mkp.add(types.InlineKeyboardButton(f'✅ {i[0]} ✅', callback_data=f'restricted_{i[0]}'))
        else:
            mkp.add(types.InlineKeyboardButton(f'❌ {i[0]} ❌', callback_data=f'allow_{i[0]}'))
    mkp.add(types.InlineKeyboardButton('< Return >', callback_data='admin'))
    await call.message.edit_reply_markup(reply_markup=mkp)


@dp.callback_query_handler(text='measure')
async def setPunishMeasureCall(call: types.CallbackQuery):
    await call.message.delete()
    mkp = types.InlineKeyboardMarkup()
    for i in ["contentType", "banWord"]:
        if db.get_punishment(i) == "delete":
            mkp.add(types.InlineKeyboardButton(f'Fordbidden {"content" if i == "contentType" else "word"} - delete msg ❎', callback_data=f'changeToBan_{i}'))
        else:
            mkp.add(types.InlineKeyboardButton(f'Fordbidden {"content" if i == "contentType" else "word"} - delete msg and ban 🚫', callback_data=f'changeToDel_{i}'))
    mkp.add(types.InlineKeyboardButton('< Return >', callback_data='admin'))
    await call.message.answer("Set the punishment", reply_markup=mkp)

@dp.callback_query_handler(text_contains='changeToBan_')
@dp.callback_query_handler(text_contains='changeToDel_')
async def changePunishMeasureCall(call: types.CallbackQuery):
    reason = call.data.split('_')[1]
    if call.data.split('_')[0] == "changeToBan":
        db.change_punishment(reason, "ban")
    else:
        db.change_punishment(reason, "delete")
    mkp = types.InlineKeyboardMarkup()
    for i in ["contentType", "banWord"]:
        if db.get_punishment(i) == "delete":
            mkp.add(types.InlineKeyboardButton(f'Fordbidden {"content" if i == "contentType" else "word"} - delete msg ❎', callback_data=f'changeToBan_{i}'))
        else:
            mkp.add(types.InlineKeyboardButton(f'Fordbidden {"content" if i == "contentType" else "word"} - delete msg and ban 🚫', callback_data=f'changeToDel_{i}'))
    mkp.add(types.InlineKeyboardButton('< Return >', callback_data='admin'))
    await call.message.edit_reply_markup(reply_markup=mkp)


@dp.callback_query_handler(text='setChats')
async def setChatsCall(call: types.CallbackQuery):
    await call.message.delete()
    chats = ""
    try:
        for i in db.get_chats():
            chats += f"{i[0]}\n"
    except:
        chats = "*There are no moderated chats*"
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Add new chat', callback_data='addChat')
    btn2 = types.InlineKeyboardButton('Delete chat', callback_data='delChat')
    btn3 = types.InlineKeyboardButton('Return', callback_data='admin')
    mkp.add(btn1).add(btn2).add(btn3)
    await call.message.answer(f"All moderated chats now:\n\n{chats}\n\n", reply_markup=mkp)


@dp.callback_query_handler(text='cancel', state=AddChat.Text)
@dp.callback_query_handler(text='cancel', state=DelChat.Text)
async def cancelChatsCall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    try:
        await state.finish()
    except:
        pass
    chats = ""
    try:
        for i in db.get_chats():
            chats += f"{i[0]}\n"
    except:
        chats = "*There are no moderated chats*"
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Add new chat', callback_data='addChat')
    btn2 = types.InlineKeyboardButton('Delete chat', callback_data='delChat')
    btn3 = types.InlineKeyboardButton('Return', callback_data='admin')
    mkp.add(btn1).add(btn2).add(btn3)
    await call.message.answer(f"All moderated chats now:\n\n{chats}\n\n", reply_markup=mkp)


@dp.callback_query_handler(text='addChat')
async def addChatCall(call: types.CallbackQuery):
    await call.message.delete()
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Cancel', callback_data='cancel')
    mkp.add(btn1)
    await AddChat.Text.set()
    await call.message.answer('To add new chat do this steps:\n1)Add this bot to your group\n2)Give to bot all admin rights\n3)Send to your chat command "<code>/id</code>"\n4)Bot will send chat id. Copy it and send there (bot\'s direct messages)', reply_markup=mkp)

@dp.message_handler(state=AddChat.Text)
async def addChatGo(message: types.Message, state: FSMContext):
    await state.finish()
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Return', callback_data='admin')
    mkp.add(btn1)
    try:
        msg = await bot.send_message(int(message.text), "Test message to checking rights...")
        db.add_chat(message.text)
        await message.answer("Chat successfully added. You can return to admin panel", reply_markup=mkp)
        await bot.delete_message(int(message.text), msg.message_id)
    except:
        await message.answer("Adding failed. Repeat all steps later. You can return to admin panel", reply_markup=mkp)


@dp.callback_query_handler(text='delChat')
async def delChatCall(call: types.CallbackQuery):
    await call.message.delete()
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Cancel', callback_data='cancel')
    mkp.add(btn1)
    await DelChat.Text.set()
    await call.message.answer("Send chat id to delete from moderated chats", reply_markup=mkp)

@dp.message_handler(state=DelChat.Text)
async def delChatGo(message: types.Message, state: FSMContext):
    await state.finish()
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Return', callback_data='admin')
    mkp.add(btn1)
    try:
        await bot.leave_chat(message.text)
        await message.answer("Chat deleted. You can return to admin panel", reply_markup=mkp)
    except:
        await message.answer("There is some problems with deleting chat. Try again later. You can return to admin panel", reply_markup=mkp)
    finally:
        db.del_chat(message.text)


@dp.callback_query_handler(text='getLogs')
async def getLogsCall(call: types.CallbackQuery):
    await call.message.answer('Last log file will be send below. Older logs you can find at <b>"logs"</b> folder')
    await call.message.reply_document(open('logs/logs.log', 'rb'))


@dp.callback_query_handler(text='getStat')
async def getStatCall(call: types.CallbackQuery):
    await call.message.delete()
    
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Return', callback_data='admin')
    mkp.add(btn1)

    statistic = db.get_stat()
    bansDurationInPercents = ""
    allDurations = set(statistic['banTimes'])
    durationsAndCount = {}
    allCount = 0
    for i in allDurations:
        durationsAndCount[i] = statistic['banTimes'].count(i)
        allCount += statistic['banTimes'].count(i)
    for i in allDurations:
        bansDurationInPercents += f"            {dateToStr(i) if i!=0 and i!='0' else 'Warning'} ≈ {int((durationsAndCount[i]/allCount) * 100)}%\n"
    

    await call.message.answer(f"Statistics:\n\n\
Total Violations count: <b>{len(statistic['violations'])}</b> \n\
In <b>{len(set(statistic['chats']))}</b> chats \n\
Among them \n\
            For banwords: <b>{len(statistic['forBanWord'])}</b> \n\
            For restricted content type: <b>{len(statistic['forContentType'])}</b> \n\
And \n\
            Delete msg and ban user: <b>{len(statistic['bans'])}</b> times \n\
            Just delete msg: <b>{len(statistic['deletes'])}</b> times \n\n\
Last violation: \n\
            ≈ <b>{secondsToDateStr(time.time() - float(statistic['lastViolations'][0]))}</b>ago \n\
            For: <b>{dateToStr(statistic['lastViolations'][1])}</b> \n\n\
Bans' duration statistics: \n\
{bansDurationInPercents} \n\
Messages after violation sent: <b>{len(statistic['messagesSent'])}</b> \n\n\
Violations in timeline: \n\
            For the last day: <b>{len(statistic['violationsLastDay'])}</b> \n\
            For the last week: <b>{len(statistic['violationsLastWeek'])}</b> \n\
            For the last month: <b>{len(statistic['violationsLastMonth'])}</b> \n\
            For the last year: <b>{len(statistic['violationsLastYear'])}</b>", reply_markup=mkp)