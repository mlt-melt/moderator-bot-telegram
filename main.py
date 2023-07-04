from config import dp
from aiogram.utils import executor
import start
import admin
import inspector

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)