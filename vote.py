import asyncio
from config import Config as C
from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardMarkup
from pyrogram.types import InlineKeyboardButton
from pyrogram.types import InlineKeyboardMarkup
from pyrogram.types import CallbackQuery
from pyrogram import enums
from pyrogram.errors import BadRequest
from pyrogram import enums
import pyromod
import pymongo
import random
gh = ['❤️','🤍','🤎','🧡','❤️‍🔥','💛','💚','💙','💜','🖤']
client = pymongo.MongoClient("mongodb+srv://miladinline:milad64523@cluster0.g7r1i.mongodb.net/?retryWrites=true&w=majority")
db = client["votes"]
post_col = db["eid"]
voted_users = db["voted"]
from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup,
                            InlineKeyboardButton)
admin= [5361491365,905339885]
logs = -1001547777717
import os
app = Client("bot", C.API_ID, C.API_HASH, C.TOKEN)
@app.on_message(filters.command(["start"]))
async def start(bot, message):
  loop = asyncio.get_event_loop()
  if message.from_user.id in admin:
    await message.reply(f'''🟢 ربات آنلاین است 
🔅 ادمین گرامی به پنل ربات نظرسنجی خوش آمدید ''',reply_markup=ReplyKeyboardMarkup(
                [
                    
                    ['ثبت پست جدید ➕']
                    
                ],
                resize_keyboard=True))
  
@app.on_message(filters.command(['free']))
async def free(b,m):
    for i in post_col.find():
        post_col.delete_one(i)
    for i in voted_users.find():
        voted_users.delete_one(i)    
    voted_users.delete_many({})
    post_col.delete_many({})



@app.on_message(filters.text )
async def new_post(bot,message):
    
    if message.text=="ثبت پست جدید ➕" and message.from_user.id in admin :
        
        answer = await message.chat.ask('''❗️ ادمین گرامی لطفا محتوای مورد نظر خود را برای همرسانی در چنل ارسال کنید .''', parse_mode=enums.ParseMode.MARKDOWN)
        documents = post_col.find()
        post_count = 0
        for i in documents:
            post_count+=1
        
        post_number = post_count+1
        new_post = {"_id":post_number , "likes" : 0}
        post_col.insert_one(new_post)

        await app.copy_message(logs, message.chat.id, answer.id,reply_markup=InlineKeyboardMarkup(
                [
                    [  # First row
                        InlineKeyboardButton(  # Generates a callback query when pressed
                            "❤️ 0 ",
                            callback_data=str(post_number)
                        )
                    ],
                    
                ]
            ))

        await answer.request.edit_text('''✅ ادمین گرامی محتوای  شما با موفقیت در چنل " **خبرگزاری علوم و تحقیقات تهران** " پست شد ''')
    else:
        pass    
        



@app.on_callback_query()
async def answer(client, q):

        try:
           member = await app.get_chat_member(logs, q.from_user.id)
           if member:
            # creating user ux
            document = voted_users.find()
            #    for i in document:
            #      print(i)
            user_id = q.from_user.id
            if  not voted_users.find_one({'_id':user_id}):
                    await q.answer('''ضمن تشکر از  از شما برای شرکت در نظرسنجی 
✅ نظرسنجی شما با موفقیت ثبت شد ''', show_alert=True)
                    
                    voted_users.insert_one({'_id':user_id,'voted_posts':''})
                    
                    
                    the_post = q.data
                    user_profile= voted_users.find_one({'_id':user_id})    
                    
                    new_voting = {'$set':{'voted_posts': user_profile['voted_posts']+'.'+str(q.data)}}
                    voted_users.update_one(user_profile,new_voting)
                    
                    result = post_col.find_one({"_id":int(q.data)})
                    
                    new_likes = {'$set': {'likes': result["likes"]+1}}
                    post_col.update_one(result, new_likes)
                    
                    
                    await q.edit_message_reply_markup(InlineKeyboardMarkup([[InlineKeyboardButton(f"{random.choice(gh)} {result['likes']+1} ", callback_data=str(result['_id']))]]))
                    await asyncio.sleep(2.5)

            elif   voted_users.find_one({'_id':user_id})  :

                user_profile= voted_users.find_one({'_id':user_id})
                if q.data in user_profile['voted_posts'].split('.'):
                    await q.answer('''⚠️ اخطار :
کاربر گرامی شما قبلا به این پست رای داده اید . ''',show_alert=True)
                else:  
                        await q.answer('''ضمن تشکر از  از شما برای شرکت در نظرسنجی 
✅ نظرسنجی شما با موفقیت ثبت شد ''', show_alert=True)
                        the_post = q.data
                        
                        
                        new_voting = {'$set':{'voted_posts': user_profile['voted_posts']+'.'+str(q.data)}}
                        voted_users.update_one(user_profile,new_voting)
                        
                        result = post_col.find_one({"_id":int(q.data)})
                        
                        new_likes = {'$set': {'likes': result["likes"]+1}}
                        post_col.update_one(result, new_likes)
                       
                        
                        await q.edit_message_reply_markup(InlineKeyboardMarkup([[InlineKeyboardButton(f"{random.choice(gh)} {result['likes']+1} ", callback_data=str(result['_id']))]]))
                        await asyncio.sleep(2.5)
        except:
            await q.answer('''⚠️ اخطار :
برای شرکت در نظرسنجی باید در کانال " خبرگزاری علوم و تحقیقات تهران " جوین شوید , در غیر اینصورت نمیتوانید در نظرسنجی شرکت کنید . ''',show_alert=True)
            


        
    
        
             





if __name__ == '__main__':
    print('[BOT] im running ')
    app.run()  