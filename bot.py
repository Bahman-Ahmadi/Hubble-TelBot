''' there is a telegram bot for finding hubble photo in some day as birthday '''
from csv import reader
from rich import print
from models import JSON, NewUser
from jdatetime import datetime
from pyrogram import Client, filters, types
from threading import Thread

def get_image(month: str, day: int) -> str:
    ''' gets image of a birthdate and info of that' '''
    base = "https://imagine.gsfc.nasa.gov/hst_bday/images/"
    rows = list(map(lambda i: i, reader(open('data.csv'))))
    data = [i for i in list(map(lambda i: i if i[0].split()[:2] == [
                            month, str(int(day))] else None, rows)) if i != None][0]
    data[1] = base + data[1]
    return data


def isJoin(bot, user_id: int, channels: list[(str, str)]) -> bool:
    try:
        for channel in channels:
            bot.get_chat_member(channel[1], user_id).status
        return True
    except:
        return False


months = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']

channels = [('کانال اسپانسر', 'rubikalib'),
            ('کانال اطلاع‌رسانی', 'bots_notifs')]

bot = Client('BirthHub', api_id=ID,
             api_hash=HASH)


@bot.on_message(filters.text)
def pv_text_handler(client, msg: types.Message):
    text = msg.text
    referral = text.split()[1] if text.startswith(
        '/start') and ' ' in text else None
    user = NewUser(msg.from_user.id)
    if user['quota'] > 0:
        if not isJoin(bot, msg.from_user.id, channels):
            msg.reply(
                'سلام و درود عزیز دل! 🫡❤️\nمیخوای بدونی توی روز تولدت فضا چه شکلی بوده؟\nپس بزن بریم!!\nفقط قبلش لطفا توی کانال های زیر عضو شو و بعدش دکمهٔ (عضو شدم) رو بزن در آخر کار.',
                quote=True,
                reply_markup=types.InlineKeyboardMarkup([
                    [types.InlineKeyboardButton(
                        name, url="https://t.me/"+username) for name, username in channels],
                    [types.InlineKeyboardButton(
                        'عضو شدم ✅', url=f'https://t.me/{bot.get_me().username}?start{"="+referral if referral is not None else ""}')]
                ])
            )
        else:
            if text.startswith("/start"):
                # print(referral, msg.from_user.id, JSON("users").GET(referral).get('referrals'), )
                if referral is not None and referral != msg.from_user.id and not msg.from_user.id in JSON("users").GET(referral).get('referrals'):
                    JSON("users").PUT(referral, 'referrals', msg.from_user.id)
                    JSON("users").PUT(referral, 'quota', +1)
                    bot.send_message(
                        referral, f'کاربر گرامی! یک کاربر جدید از طریق لینک دعوت شما به کاربران ربات افزوده شد.\nبا عضویت ({msg.from_user.first_name}) یک اعتبار جدید دریافت کردید 💯\n[×] اعتبار شما: {JSON("users").GET(referral).get("quota")}')

                msg.reply(
                    f'سلاااام {msg.from_user.first_name}{" " + (msg.from_user.last_name or "")} عزیز! 👋👽\nمن رباتی هستم که میتونه بهت بگه فضا توی روز تولد تو یا کسی که دوستش داری چه شکلی بوده ✨😎\nعکس ها مستقیما از تلسکوپ فضایی هابل و ناسا گرفته میشه پس بزن که بریم!!\n**توی کدوم ماه بدنیا اومدی؟؟** 🌚',
                    quote=True,
                    reply_markup=types.InlineKeyboardMarkup([
                        [types.InlineKeyboardButton(j, callback_data=f"month_{datetime.j_months_fa.index(j) + 1}") for j in i[::-1]] for i in [datetime.j_months_fa[:3], datetime.j_months_fa[3:6], datetime.j_months_fa[6:9], datetime.j_months_fa[9:]]
                    ])
                )
    else:
        msg.reply(
            f'کاربر گرامی، سقف اعتبار شما برای استفاده از ربات به پایان رسیده\nبرای افزایش اعتبار خود، دوستانتان را از طریق لینک زیر دعوت کنید؛ هرفردی که از طریق لینک شما به کاربران ربات اضافه شود، یک اعتبار جدید برای شما خواهد بود.\n\n**لینک دعوت شما:**\nhttps://t.me/{bot.get_me().username}?start={msg.from_user.id}',
            quote=True
        )


@bot.on_callback_query()
def callback_query_handler(client, query: types.CallbackQuery):
    data = query.data
    if data.startswith('month'):
        month = int(data.split("_")[1])
        query.edit_message_text(
            f'خب پس {datetime.j_months_fa[month-1]} ماهی عزیز؛ چندمِ {datetime.j_months_fa[month-1]} به دنیا اومدی؟ 🌝')
        query.edit_message_reply_markup(types.InlineKeyboardMarkup([
            [types.InlineKeyboardButton(j, callback_data=f"day_{j}&month_{month}") for j in i[::-1]] for i in [range(1, 7), range(7, 13), range(13, 19), range(19, 25), range(25, 32 if month < 7 else 30 if month == 12 else 31)]
        ]))

    elif data.startswith('day'):
        # MAIN TASK
        query.edit_message_text('یه کوچولو صبر کن 🤌')
        day, month = [int(i.split("_")[1]) for i in data.split('&')]
        gdate = datetime(1300, month, day).togregorian()
        result = get_image(months[gdate.month - 1], gdate.day)
        quota = JSON("users").GET(query.from_user.id).get('quota') - 1
        bot.delete_messages(query.from_user.id, query.message.id)
        bot.send_photo(query.from_user.id, result[1], caption=f"🔭✨ **{result[2]}**\n{result[3]}\n\n[×] اعتبار شما: {quota}\n\n**دوستت میدونه فضا توی روز تولدش چه شکلی بوده؟**\n🔭🤖 @{bot.get_me().username}", reply_markup=types.InlineKeyboardMarkup([
            # [types.InlineKeyboardButton("Share With Friends", switch_inline_query_current_chat="wow")],
            [types.InlineKeyboardButton("اطلاعات بیشتر", url=result[4])]
        ]))
        JSON("users").PUT(query.from_user.id, 'quota', -1)


if __name__ == "__main__":
    bot.run()