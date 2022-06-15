# referenced from https://www.codementor.io/@karandeepbatra/part-1-how-to-create-a-telegram-bot-in-python-in-under-10-minutes-19yfdv4wrq

# Import nsdb to handle database functions
import nsdb

# Other library imports
import logging
import os
from datetime import datetime, timezone
import pytz
from functools import wraps

# Telegram imports
from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

import os
from google.cloud import dialogflow
from google.api_core.exceptions import InvalidArgument
from uuid import uuid4
from datetime import datetime

from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from telegram.constants import ChatAction
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram import Bot
import asyncio

from functools import wraps


# DialogFlow imports
from google.cloud import dialogflow
from google.api_core.exceptions import InvalidArgument



# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'private_key.json'

DIALOGFLOW_PROJECT_ID = 'code-exp-bqsp'
DIALOGFLOW_LANGUAGE_CODE = 'en'
SESSION_ID = 'me'
session_client = dialogflow.SessionsClient()
session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
telegramToken=""
if telegramToken == "":
    raise RuntimeError(
        f"the telegramToken was redacted. To test the code, please create your own Telegram bot as per README.md"
    )


# Session variables
PDPA, GENDER, ORD = range(3)
FEEDBACK, FEEDBACK_COLLECT = range(2)
Q1ANS, Q1LOG, Q2ANS, Q2LOG, Q3ANS, Q3LOG, Q4ANS, Q4LOG, Q5ANS, Q5LOG, Q6ANS, Q6LOG = range(12)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        async def command_func(update, context, *args, **kwargs):
            if update.message == None:
                return
            await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return await func(update, context,  *args, **kwargs)
        return command_func
    
    return decorator


'''Configure profile and obtain details'''

@send_action(ChatAction.TYPING) 
async def start(update, context):
    """Send a message when the command /start is issued."""
    reply_keyboard = [["Yes","No"]]
    await context.bot.send_message(chat_id=update.message.from_user.id, text="Hi buddy, glad to meet you!")
    await context.bot.send_message(chat_id=update.message.from_user.id, text="😄")
    await update.message.reply_text(
        "To be able to help you better, I will be asking for and remembering your name, gender and ORD date. Your feedback and responses to PC Interview questions will be shared with your commanders.\n\n"
        "Do you acknowledge?",
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Yes or No?"
        ),
    )
    
    return PDPA

@send_action(ChatAction.TYPING)
async def pdpa(update, context):
    """Asks for elaboration if ans=yes. Otherwise, ask q2"""
    if update.message.text == "Yes":
        reply_keyboard = [["Boy", "Girl", "Other"]]

        await update.message.reply_text(
            "I would love to know you better. Just two questions.\n\n"
            "Firstly, are you a boy or a girl?",
            reply_markup = ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder="Boy or Girl?"
            ),
        )
        return GENDER
    elif update.message.text == "No":
        reply_keyboard = [["Yes", "No"]]
        await update.message.reply_text(
            "Unfortunately, we can only have a meaningful chat if you are fine with me asking for and remembering your name, gender and ORD date. I also need to be able to share your feedback and responses to PC Interview questions with your commanders.\n\n"
            "Do you acknowledge?",
            reply_markup = ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder="Yes or No?"
            ),
        )
        return PDPA
    else:
        reply_keyboard = [["Yes", "No"]]
        await update.message.reply_text(
            "Please reply Yes or No.",
            reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Yes or No?"
            ),
        )
        return PDPA

@send_action(ChatAction.TYPING)     
async def gender(update, context):
    """Stores the selected gender and asks for ORD date."""
    #user = update.message.from_user
    #logger.info("Gender of %s: %s", user.first_name, update.message.text)
    userid = update.message.from_user.id
    gender = update.message.text
    
    # Write to database
    nsdb.add_user_gender(userid, gender)
    last_name = update.message.from_user.last_name
    if last_name is None: last_name = ''
    nsdb.add_user_name(userid, update.message.from_user.first_name +" "+ last_name)

    await update.message.reply_text(
        "I see! When are you going to ORD? "
        "Send following the format dd/mm/yy",
        reply_markup=ReplyKeyboardRemove(),
    )

    return ORD

@send_action(ChatAction.TYPING) 
async def getORD(update, context):
    """Stores the ORD date and ends the conversation."""
    user = update.message.from_user
    try:
        date = datetime.strptime(update.message.text, '%d/%m/%y')
    except ValueError:
        await update.message.reply_text(
            "That doesn't seem like the right format! Please try again in the format dd/mm/yy",
            reply_markup=ReplyKeyboardRemove(),
        )
        return ORD
        
    #logger.info("ORD Date of %s: %s", user.first_name, date)
    userid = update.message.from_user.id
    
    # Write to database
    nsdb.add_user_ord(userid, date.strftime("%d%m%y"))

    context.user_data["ORD"] = update.message.text
    await update.message.reply_text(
        "Thanks! Now I feel like we got closer! Feel free to chat with me about NS. I'll be your listening ear 👂",
        reply_markup=ReplyKeyboardRemove(),
    )

    return ConversationHandler.END

@send_action(ChatAction.TYPING)     
async def cancel(update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! You can tell me about it again by sending /start", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

'''Configure profile and obtain details'''


'''PC interview'''

@send_action(ChatAction.TYPING) 
async def pcinterview_start(update, context):
    """Send a message when the command /pcinterview is issued."""
    userid = update.message.from_user.id
    message = update.message.text
    date = update.message.date
    date = date.replace(tzinfo=timezone.utc).astimezone(pytz.timezone('Asia/Singapore'))
    needToDo=nsdb.update_pc_interview(userid, date.strftime("%d%m%y %H%M"), "ongoing")
    if not needToDo:
        nsdb.add_pcinterview(userid, date.strftime("%d%m%y %H%M"), "ongoing")
    #print(str(nsdb.query_pcinterview_table()))
    reply_keyboard = [["Yes", "No"]]

    await update.message.reply_text(
        "Do you face any financial problems? (e.g. your family member lost their job / you owe someone money / you are in need of cash now)",
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Yes or No?"
        ),
    )
    
    return Q1ANS
    
@send_action(ChatAction.TYPING) 
async def q1ans(update, context):
    """Asks for elaboration if ans=yes. Otherwise, ask q2"""
    if update.message.text == "Yes":
        userid = update.message.from_user.id
        date = update.message.date
        date = date.replace(tzinfo=timezone.utc).astimezone(pytz.timezone('Asia/Singapore'))
        nsdb.update_pc_interview(userid, date.strftime("%d%m%y %H%M"), "failed")
        #print(str(nsdb.query_pcinterview_table()))
        await update.message.reply_text(
            "Could you elaborate on the issue you are facing? I would like to understand it better.",
            reply_markup=ReplyKeyboardRemove(),
        )
        return Q1LOG
    elif update.message.text == "No":
        reply_keyboard = [["Yes", "No"]]
        await update.message.reply_text(
            "Do you face any problems with family? (e.g. you have fallen out with a family member / your family is being harassed)",
            reply_markup = ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder="Yes or No?"
            ),
        )
        return Q2ANS
    else:
        reply_keyboard = [["Yes", "No"]]
        await update.message.reply_text(
            "Please reply Yes or No.",
            reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Yes or No?"
            ),
        )
        return Q1ANS

@send_action(ChatAction.TYPING) 
async def q1log(update, context):
    """Stores response and asks q2."""
    userid = update.message.from_user.id
    message = update.message.text
    date = update.message.date
    date = date.replace(tzinfo=timezone.utc).astimezone(pytz.timezone('Asia/Singapore'))
    nsdb.add_alert(userid, date.strftime("%d%m%y %H%M"), 'financial', message)
    #print(str(nsdb.query_alert_table()))
    reply_keyboard = [["Yes", "No"]]

    await update.message.reply_text(
        "Do you face any problems with family? (e.g. you have fallen out with a family member / your family is being harassed)",
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Yes or No?"
        ),
    )

    return Q2ANS

@send_action(ChatAction.TYPING) 
async def q2ans(update, context):
    """Asks for elaboration if ans=yes. Otherwise, ask q3"""
    if update.message.text == "Yes":
        userid = update.message.from_user.id
        date = update.message.date
        date = date.replace(tzinfo=timezone.utc).astimezone(pytz.timezone('Asia/Singapore'))
        nsdb.update_pc_interview(userid, date.strftime("%d%m%y %H%M"), "failed")
        #print(str(nsdb.query_pcinterview_table()))
        await update.message.reply_text(
            "Could you elaborate on the issue you are facing? I would like to understand it better.",
            reply_markup=ReplyKeyboardRemove(),
        )
        return Q2LOG
    elif update.message.text == "No":
        reply_keyboard = [["Yes", "No"]]
        await update.message.reply_text(
            "Do you face any problems with relationships? (e.g. you and your partner are arguing about something / you recently broke up)",
            reply_markup = ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder="Yes or No?"
            ),
        )
        return Q3ANS
    else:
        reply_keyboard = [["Yes", "No"]]
        await update.message.reply_text(
            "Please reply Yes or No.",
            reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Yes or No?"
            ),
        )
        return Q2ANS

@send_action(ChatAction.TYPING) 
async def q2log(update, context):
    """Stores response and asks q3."""
    userid = update.message.from_user.id
    message = update.message.text
    date = update.message.date
    date = date.replace(tzinfo=timezone.utc).astimezone(pytz.timezone('Asia/Singapore'))
    nsdb.add_alert(userid, date.strftime("%d%m%y %H%M"), 'family', message)
    reply_keyboard = [["Yes", "No"]]

    await update.message.reply_text(
        "Do you face any problems with relationships? (e.g. you and your partner are arguing about something / you recently broke up)",
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Yes or No?"
        ),
    )

    return Q3ANS

@send_action(ChatAction.TYPING) 
async def q3ans(update, context):
    """Asks for elaboration if ans=yes. Otherwise, ask q4"""
    if update.message.text == "Yes":
        userid = update.message.from_user.id
        date = update.message.date
        date = date.replace(tzinfo=timezone.utc).astimezone(pytz.timezone('Asia/Singapore'))
        nsdb.update_pc_interview(userid, date.strftime("%d%m%y %H%M"), "failed")
        #print(str(nsdb.query_pcinterview_table()))
        await update.message.reply_text(
            "Could you elaborate on the issue you are facing? I would like to understand it better.",
            reply_markup=ReplyKeyboardRemove(),
        )
        return Q3LOG
    elif update.message.text == "No":
        reply_keyboard = [["Yes", "No"]]
        await update.message.reply_text(
            "Do you face any problems with drug / inhalant / alcohol abuse? (e.g. you find yourself needing a drink often / you smoke too many packs a day / your friend got you to try drugs)",
            reply_markup = ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder="Yes or No?"
            ),
        )
        return Q4ANS
    else:
        reply_keyboard = [["Yes", "No"]]
        await update.message.reply_text(
            "Please reply Yes or No.",
            reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Yes or No?"
            ),
        )
        return Q3ANS

@send_action(ChatAction.TYPING) 
async def q3log(update, context):
    """Stores response and asks q4."""
    userid = update.message.from_user.id
    message = update.message.text
    date = update.message.date
    date = date.replace(tzinfo=timezone.utc).astimezone(pytz.timezone('Asia/Singapore'))
    nsdb.add_alert(userid, date.strftime("%d%m%y %H%M"), 'relationship', message)
    reply_keyboard = [["Yes", "No"]]

    await update.message.reply_text(
        "Do you face any problems with drug/inhalant/alcohol abuse? (e.g. you find yourself needing a drink often / you smoke too many packs a day / your friend got you to try drugs)",
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Yes or No?"
        ),
    )

    return Q4ANS

@send_action(ChatAction.TYPING) 
async def q4ans(update, context):
    """Asks for elaboration if ans=yes. Otherwise, ask q5"""
    if update.message.text == "Yes":
        userid = update.message.from_user.id
        date = update.message.date
        date = date.replace(tzinfo=timezone.utc).astimezone(pytz.timezone('Asia/Singapore'))
        nsdb.update_pc_interview(userid, date.strftime("%d%m%y %H%M"), "failed")
        #print(str(nsdb.query_pcinterview_table()))
        await update.message.reply_text(
            "Could you elaborate on the issue you are facing? I would like to understand it better.",
            reply_markup=ReplyKeyboardRemove(),
        )
        return Q4LOG
    elif update.message.text == "No":
        reply_keyboard = [["Yes", "No"]]
        await update.message.reply_text(
            "Have you had self harm/suicidal thoughts? (e.g. you think life is meaningless / your life is too hard and you are thinking of suicide)",
            reply_markup = ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder="Yes or No?"
            ),
        )
        return Q5ANS
    else:
        reply_keyboard = [["Yes", "No"]]
        await update.message.reply_text(
            "Please reply Yes or No.",
            reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Yes or No?"
            ),
        )
        return Q4ANS

@send_action(ChatAction.TYPING) 
async def q4log(update, context):
    """Stores response and asks q5."""
    userid = update.message.from_user.id
    message = update.message.text
    date = update.message.date
    date = date.replace(tzinfo=timezone.utc).astimezone(pytz.timezone('Asia/Singapore'))
    nsdb.add_alert(userid, date.strftime("%d%m%y %H%M"), 'alcohol/drug/inhalant', message)
    reply_keyboard = [["Yes", "No"]]

    await update.message.reply_text(
        "Have you had self harm/suicidal thoughts? (e.g. you think life is meaningless / your life is too hard and you are thinking of suicide)",
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Yes or No?"
        ),
    )

    return Q5ANS

@send_action(ChatAction.TYPING) 
async def q5ans(update, context):
    """Asks for elaboration if ans=yes. Otherwise, ask q6"""
    if update.message.text == "Yes":
        userid = update.message.from_user.id
        date = update.message.date
        date = date.replace(tzinfo=timezone.utc).astimezone(pytz.timezone('Asia/Singapore'))
        nsdb.update_pc_interview(userid, date.strftime("%d%m%y %H%M"), "failed")
        #print(str(nsdb.query_pcinterview_table()))
        await update.message.reply_text(
            "Could you elaborate on the issue you are facing? I would like to understand it better.",
            reply_markup=ReplyKeyboardRemove(),
        )
        return Q5LOG
    elif update.message.text == "No":
        reply_keyboard = [["Yes", "No"]]
        await update.message.reply_text(
            "Do you have any upcoming counselling appointments? (e.g. you will be meeting the unit para-counsellor / you have an appointment at IMH, a private counsellor or psychologist)",
            reply_markup = ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder="Yes or No?"
            ),
        )
        return Q6ANS
    else:
        reply_keyboard = [["Yes", "No"]]
        await update.message.reply_text(
            "Please reply Yes or No.",
            reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Yes or No?"
            ),
        )
        return Q5ANS

@send_action(ChatAction.TYPING) 
async def q5log(update, context):
    """Stores response and asks q6."""
    userid = update.message.from_user.id
    message = update.message.text
    date = update.message.date
    date = date.replace(tzinfo=timezone.utc).astimezone(pytz.timezone('Asia/Singapore'))
    nsdb.add_alert(userid, date.strftime("%d%m%y %H%M"), 'suicide', message)
    reply_keyboard = [["Yes", "No"]]

    await update.message.reply_text(
        "Do you have any upcoming counselling appointments? (e.g. you will be meeting the unit para-counsellor / you have an appointment at IMH, a private counsellor or psychologist)",
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Yes or No?"
        ),
    )

    return Q6ANS

@send_action(ChatAction.TYPING) 
async def q6ans(update, context):
    """Asks for elaboration if ans=yes. Otherwise, end"""
    if update.message.text == "Yes":
        userid = update.message.from_user.id
        date = update.message.date
        date = date.replace(tzinfo=timezone.utc).astimezone(pytz.timezone('Asia/Singapore'))
        nsdb.update_pc_interview(userid, date.strftime("%d%m%y %H%M"), "failed")
        #print(str(nsdb.query_pcinterview_table()))
        await update.message.reply_text(
            "Could you tell me more about your upcoming counselling appointments? I would like to understand it better.",
            reply_markup=ReplyKeyboardRemove(),
        )
        return Q6LOG
    elif update.message.text == "No":
        userid = update.message.from_user.id
        date = update.message.date
        date = date.replace(tzinfo=timezone.utc).astimezone(pytz.timezone('Asia/Singapore'))
        nsdb.update_pc_interview(userid, date.strftime("%d%m%y %H%M"), "completed")
        reply_keyboard = [["Yes", "No"]]
        await update.message.reply_text(
            "That's the end of the PC interview! Thanks for your time.",
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END
    else:
        reply_keyboard = [["Yes", "No"]]
        await update.message.reply_text(
            "Please reply Yes or No.",
            reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Yes or No?"
            ),
        )
        return Q6ANS

@send_action(ChatAction.TYPING) 
async def q6log(update, context):
    """Stores response and ends."""
    userid = update.message.from_user.id
    message = update.message.text
    date = update.message.date
    date = date.replace(tzinfo=timezone.utc).astimezone(pytz.timezone('Asia/Singapore'))
    nsdb.add_alert(userid, date.strftime("%d%m%y %H%M"), 'counselling', message)

    await update.message.reply_text(
            "That's the end of the PC interview! Thanks for your time.",
            reply_markup=ReplyKeyboardRemove(),
        )

    return ConversationHandler.END

'''PC interview'''
    
'''Feedback'''

@send_action(ChatAction.TYPING) 
async def feedback_start(update, context):
    """Send a message when the command /feedback is issued."""
    reply_keyboard = [["Yes", "No"]]

    await update.message.reply_text(
            "Would you like to submit feedback?",
            reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Yes or No?"
            ),
        )
    
    return FEEDBACK
    
@send_action(ChatAction.TYPING) 
async def feedback(update, context):
    """Asks for elaboration."""
    if update.message.text == "Yes":
        await update.message.reply_text(
            "What is your feedback?",
            reply_markup=ReplyKeyboardRemove(),
        )
        return FEEDBACK_COLLECT    
    elif update.message.text == "No":
        await update.message.reply_text(
            "Alright, have a nice day.",
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END
    else:
        reply_keyboard = [["Yes", "No"]]
        await update.message.reply_text(
            "Please reply Yes or No.",
            reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Yes or No?"
            ),
        )
        return FEEDBACK

@send_action(ChatAction.TYPING) 
async def feedback_collect(update, context):
    """Stores response and ends."""
    userid = update.message.from_user.id
    message = update.message.text
    date = update.message.date
    
    # Format datetime for writing to database
    date = date.replace(tzinfo=timezone.utc).astimezone(pytz.timezone('Asia/Singapore'))

    # Write to database
    nsdb.add_feedback(userid, date.strftime("%d%m%y %H%M"), message)

    await update.message.reply_text(
        "Your feedback has been received!",
        reply_markup=ReplyKeyboardRemove(),
    )

    return ConversationHandler.END
    
'''Feedback'''

    
'''Commands'''    

@send_action(ChatAction.TYPING)
async def help(update, context):
    """Send a message when the command /help is issued."""
    await update.message.reply_text("You can send me these commands:\n/pcinterview - commence PC interiew\n/feedback - provide feedback")

'''Commands end'''


@send_action(ChatAction.TYPING)
async def chat(update, context):
    """Echo the user message."""
    DIALOGFLOW_PROJECT_ID = 'code-exp-bqsp'
    DIALOGFLOW_LANGUAGE_CODE = 'en'
    SESSION_ID = update.message.from_user.id
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    
    text_input = dialogflow.TextInput(text=update.message.text, language_code=DIALOGFLOW_LANGUAGE_CODE)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    
    userid = update.message.from_user.id 
    date = update.message.date
    date = date.replace(tzinfo=timezone.utc).astimezone(pytz.timezone('Asia/Singapore'))
    message = update.message.text   
    if response.query_result.fulfillment_text == "Do your superiors know?" or response.query_result.fulfillment_text == "Do your superiors know about this?":
        message = update.message.text
        context.user_data['alert'] = update.message.text
    if response.query_result.fulfillment_text == "{ALERT: violence}":
        # Write to database
        nsdb.add_alert(userid, date.strftime("%d%m%y %H%M"), 'violence', message)
        await update.message.reply_text("Take some deep breathes. I am arranging for someone to assist you 😇.") 
    
    elif response.query_result.fulfillment_text == "{ALERT: financial}":
        # Write to database
        nsdb.add_alert(userid, date.strftime("%d%m%y %H%M"), 'financial', context.user_data.get('alert', 'Not found'))
        await update.message.reply_text("I have flagged out this issue to your superiors. In the meantime, you can also contact MINDEF Shared Services – Personnel Services Centre at 6373-1140 or 6373-1155 for financial support.")
    
    elif response.query_result.fulfillment_text == "{ALERT: camp}":
        # Write to database
        nsdb.add_alert(userid, date.strftime("%d%m%y %H%M"), 'camp', context.user_data.get('alert', 'Not found'))
        await update.message.reply_text("I have flagged out this issue to your superiors. Be cool and try your best to avoid conflict in the meantime. If the problem persists and escalates, please do let your superiors know again. It would be easier for them to handle this issue directly.")
    
    elif response.query_result.fulfillment_text == "{ALERT: relationship}":
        # Write to database
        nsdb.add_alert(userid, date.strftime("%d%m%y %H%M"), 'relationship', context.user_data.get('alert', 'Not found'))
        await update.message.reply_text("I have flagged out this issue to your superiors. You could also contact certified para counsellors in your unit, as well as the SAF hotline.")
        
    elif response.query_result.fulfillment_text == "{ALERT: substance}":
        # Write to database
        nsdb.add_alert(userid, date.strftime("%d%m%y %H%M"), 'substance', context.user_data.get('alert', 'Not found'))
        await update.message.reply_text("I have flagged out this issue to your superiors. I can imagine how hard it is for you to suffer in silence. Please do reach out to the respective institutions for help.")
        bot = Bot(telegramToken) 
        async with bot: 
            await bot.send_message(text='The National Addictions Management Service (NAMS) provides treatment for a broad range of addictions, including addiction to drugs, alcohol, gambling, gaming and others. \n\nFor enquiries: 6389 2000\nFor appointment: 6389 2200\nEmail: nams@imh.com.sg', chat_id=update.message.from_user.id)
            
    else:
        await update.message.reply_text(response.query_result.fulfillment_text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    application = Application.builder().token(telegramToken).build()

    # on different commands - answer in Telegram
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            PDPA: [MessageHandler(filters.TEXT, pdpa)],
            GENDER: [MessageHandler(filters.Regex("^(Boy|Girl|Other)$"), gender)],
            ORD: [MessageHandler(filters.TEXT, getORD)],
            },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    #pc interview
    pc_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("pcinterview", pcinterview_start)],
        states={
            Q1ANS: [MessageHandler(filters.TEXT, q1ans)],
            Q1LOG: [MessageHandler(filters.TEXT, q1log)],
            Q2ANS: [MessageHandler(filters.TEXT, q2ans)],
            Q2LOG: [MessageHandler(filters.TEXT, q2log)],
            Q3ANS: [MessageHandler(filters.TEXT, q3ans)],
            Q3LOG: [MessageHandler(filters.TEXT, q3log)],
            Q4ANS: [MessageHandler(filters.TEXT, q4ans)],
            Q4LOG: [MessageHandler(filters.TEXT, q4log)],
            Q5ANS: [MessageHandler(filters.TEXT, q5ans)],
            Q5LOG: [MessageHandler(filters.TEXT, q5log)],
            Q6ANS: [MessageHandler(filters.TEXT, q6ans)],
            Q6LOG: [MessageHandler(filters.TEXT, q6log)],
            },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    #feedback
    feedback_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("feedback", feedback_start)],
        states={
            FEEDBACK: [MessageHandler(filters.TEXT, feedback)],
            FEEDBACK_COLLECT: [MessageHandler(filters.TEXT, feedback_collect)],
            },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.add_handler(pc_conv_handler)
    application.add_handler(feedback_conv_handler)
    application.add_handler(CommandHandler("help", help))
    # on noncommand i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT, chat))
    # log all errors
    application.add_error_handler(error)

    # Start the Bot
    application.run_polling()


if __name__ == '__main__':
    main()