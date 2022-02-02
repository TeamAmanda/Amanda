from telegram.ext import run_async

from Amanda import dispatcher
from Amanda.modules.disable import DisableAbleCommandHandler
from Amanda.modules.helper_funcs.alternate import send_message
from Amanda.modules.helper_funcs.chat_status import user_admin


@run_async
@user_admin
def send(update, context):
    args = update.effective_message.text.split(None, 1)
    creply = args[1]
    send_message(update.effective_message, creply)


ADD_CCHAT_HANDLER = DisableAbleCommandHandler("send", send)
dispatcher.add_handler(ADD_CCHAT_HANDLER)
__command_list__ = ["send"]
__handlers__ = [ADD_CCHAT_HANDLER]
