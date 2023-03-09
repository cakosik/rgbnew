from main import *

bot = Bot(token=cfg.BOT_TOKEN, disable_web_page_preview=True)
dp = Dispatcher(bot)


async def chats_handler(message):
   status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
   status_block = str(status_block[0])

   if status_block == 'on':
      return


   user_id = message.from_user.id
   user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
   user_name = str(user_name[0])

   user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
   user_status = str(user_status[0])

   if user_status in ['Owner', 'Helper_Admin', 'Admin']:
      chats = cursor.execute(f'SELECT * from chats')
      list_chat = []
      num = 0

      for chat in chats:
         
         num += 1

         list_chat.append(f'📎 <b>NAME: {chat[1]} | 🔎 ID:</b> <code>{chat[0]}</code> <b>| 📅 DATA:</b> <code>{chat[2]}</code>')
      
      list = '\n'.join(list_chat)

      await message.reply(list, parse_mode='html')
   else:
      return await message.reply('❗️ Данная команда доступна от прав администратора <b>ADMIN</b>', parse_mode='html')




async def register_chat_handler(message):
   status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
   status_block = str(status_block[0])

   if status_block == 'on':
      return

   user_id = message.from_user.id
   user_name = message.from_user.get_mention(as_html=True)

   chat_id = message.chat.id
   group_name = message.chat.full_name
   cursor.execute(f"SELECT chat_id FROM chats WHERE chat_id = '{chat_id}'")

   if user_id == chat_id:
      return await message.reply('❗️ Нельзя регистрировать ЛС бота, в <b>качестве чата</b>', parse_mode='html')

   if cursor.fetchone() is None:
      text_register_chat = f'''
💭 <code>{user_name}</code> , вы <b>успешно зарегистрировали</b> чат <code>{group_name}</code> 
      '''
      time_register = f'{datetime.now()}'
      photo_new_chat = open('newchat.jpg', 'rb')
      cursor.execute("INSERT INTO chats VALUES(?, ?, ?);", (chat_id, group_name, time_register[:19]))
      connect.commit()

      await bot.send_photo(message.chat.id, photo_new_chat, text_register_chat, parse_mode='html')
   else:
      return await message.reply(f'❗️ <code>{group_name}</code> <b>уже зарегистрирован</b>', parse_mode='html')

