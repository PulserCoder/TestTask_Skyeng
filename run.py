from aiogram import executor
from setup_db import Base, engine




if __name__ == '__main__':
    from handlers import dp
    Base.metadata.create_all(bind=engine)
    executor.start_polling(dp, skip_updates=True)