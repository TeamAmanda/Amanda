import logging
import time
from Amanda import OWNER_ID
from Amanda import pbot
from userbase import present_in_userbase, add_to_userbase, get_users

@pbot.on_message(filters.private & filters.command('broadcast') & filters.user(OWNER_ID) & filters.reply)
async def broadcast(client: pbot, message: Message):
       broadcast_msg = message.reply_to_message
       txt = await message.reply(text = 'Staring....')        
       user_ids = await get_users()
       success = 0
       deleted = 0
       blocked = 0     
       await txt.edit(text = 'Broadcasting message, Please wait', reply_markup = None)   
       for user_id in user_ids:
          try:
            broadcast_msg = await broadcast_msg.copy(
            chat_id =user_id ,
            reply_to_message_id = broadcast_msg.message_id
            )
            success += 1
            time.sleep(3)
          except FloodWait as e:
            await asyncio.sleep(e.x)
            success += 1
          except UserIsBlocked:
            blocked += 1
          except InputUserDeactivated:
            deleted += 1                       
       text = f"""<b>Broadcast Completed</b>    
Total users: {str(len(user_ids))}
Deleted accounts: {str(deleted)} """
       await message.reply(text=text)
       await message.delete()
