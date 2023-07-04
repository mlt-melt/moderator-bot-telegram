from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database import DB

admins = []                                                 # list of admins' IDs
db = DB('db.db')                                            # database name
bot = Bot(token='', parse_mode='html')                      # bot's token

permitions = {"can_send_messages": False,
              "can_send_audios": False,
              "can_send_documents": False,
              "can_send_photos": False,
              "can_send_videos": False,
              "can_send_video_notes": False,
              "can_send_voice_notes": False,
              "can_send_polls": False,
              "can_send_other_messages": False,
              "can_add_web_page_previews": False,
              "can_change_info": False,
              "can_invite_users": False,
              "can_pin_messages": False,
              "can_manage_topics": False,
              }                                             # what will be user permited after violation

banSteps = [0, "0:0:10", "0:1:0", "1:0:0", "7:0:0"]          # ban steps in format "days:hours:minutes", last step will be repeated indefinitely
                                                            # to ban permanently set value more then 365 days; to make warning set 0 value

sendMessage = True                                          # will bot send message in chat about user's violation (you can set this messages in textConfig.py)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)