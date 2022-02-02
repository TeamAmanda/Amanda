import datetime
import platform
import time
from platform import python_version

import requests
import telegram
from psutil import cpu_percent, virtual_memory, disk_usage, boot_time
from spamwatch import __version__ as __sw__
from telegram import ParseMode, Update
from telegram.ext import CommandHandler, Filters, CallbackContext

from Amanda import dispatcher, OWNER_ID
from Amanda.modules.helper_funcs.alternate import typing_action
from Amanda.modules.helper_funcs.filters import CustomFilters


@typing_action
def get_bot_ip(update, _):
    """Sends the bot's IP address, so as to be able to ssh in if necessary.
    OWNER ONLY.
    """
    res = requests.get("http://ipinfo.io/ip")
    update.message.reply_text(res.text)


@typing_action
def system_status(update: Update, context: CallbackContext):
    uptime = datetime.datetime.fromtimestamp(boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    status = "<b>======[ 𝚂𝚈𝚂𝚃𝙴𝙼 𝚂𝚃𝙰𝚃𝙸𝚂𝚃𝙸𝙲𝚂 ]======</b>\n\n"
    status += "<b>📍 𝚂𝚢𝚜𝚝𝚎𝚖 𝚞𝚙𝚝𝚒𝚖𝚎 :</b> <code>" + str(uptime) + "</code>\n\n"

    uname = platform.uname()
    status += "<b>┍</b>\n"
    status += "<b>    ◤ 𝚂𝚢𝚜𝚝𝚎𝚖 :</b> <code>" + str(uname.system) + "</code>\n"
    status += "<b>    ◤ 𝚁𝚎𝚕𝚎𝚊𝚜𝚎 :</b> <code>" + str(uname.release) + "</code>\n"
    status += "<b>    ◤ 𝙼𝚊𝚌𝚑𝚒𝚗𝚎 :</b> <code>" + str(uname.machine) + "</code>\n"
    status += "<b>    ◤ 𝙿𝚛𝚘𝚌𝚎𝚜𝚜𝚘𝚛 :</b> <code>" + str(uname.processor) + "</code>\n"
    status += "<b>    ◤ 𝙽𝚘𝚍𝚎 𝚗𝚊𝚖𝚎 :</b> <code>" + str(uname.node) + "</code>\n"
    status += "<b>    ◤ 𝚅𝚎𝚛𝚜𝚒𝚘𝚗 :</b> <code>" + str(uname.version) + "</code>\n\n"

    mem = virtual_memory()
    cpu = cpu_percent()
    disk = disk_usage("/")
    status += "<b>    ◤ 𝙲𝙿𝚄 𝚞𝚜𝚊𝚐𝚎 :</b> <code>" + str(cpu) + " %</code>\n"
    status += "<b>    ◤ 𝚁𝚊𝚖 𝚞𝚜𝚊𝚐𝚎 :</b> <code>" + str(mem[2]) + " %</code>\n"
    status += "<b>    ◤ 𝚂𝚝𝚘𝚛𝚊𝚐𝚎 𝚞𝚜𝚎𝚍 :</b> <code>" + str(disk[3]) + " %</code>\n\n"
    status += "<b>    ◤ 𝙿𝚢𝚝𝚑𝚘𝚗 𝚟𝚎𝚛𝚜𝚒𝚘𝚗 :</b> <code>" + python_version() + "</code>\n"
    status += (
        "<b>    ◤ 𝙻𝚒𝚋𝚛𝚊𝚛𝚢 𝚟𝚎𝚛𝚜𝚒𝚘𝚗 :</b> <code>"
        + str(telegram.__version__)
        + "</code>\n"
    )
    status += "<b>    ◤ 𝚂𝚙𝚊𝚖𝚠𝚊𝚝𝚌𝚑 𝙰𝙿𝙸 :</b> <code>" + str(__sw__) + "</code>\n"
    status += "<b>┖</b>\n"
    context.bot.sendMessage(update.effective_chat.id, status, parse_mode=ParseMode.HTML)


IP_HANDLER = CommandHandler(
    "ip", get_bot_ip, filters=Filters.chat(OWNER_ID), run_async=True
)
SYS_STATUS_HANDLER = CommandHandler(
    "sysinfo", system_status, filters=CustomFilters.dev_filter, run_async=True
)

dispatcher.add_handler(IP_HANDLER)
dispatcher.add_handler(SYS_STATUS_HANDLER)
