from flask import Flask, jsonify
from flask_cors import CORS
from telegram import Bot 

import nsdb

app = Flask(__name__)
CORS(app)

# get all users
@app.route('/feedback')
def get_all_feedback():
    feedback_list = nsdb.display_feedback()
    if len(feedback_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "feedback": feedback_list
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There is no one in the feedback database."
        }
    ), 404

# get all users
@app.route('/alerts')
def get_all_alerts():
    alert_list = nsdb.display_alert()
    if len(alert_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "alert": alert_list
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There is no one in the feedback database."
        }
    ), 404

# get all users
@app.route('/users')
def get_all_users():
    user_list = nsdb.query_user_table()
    if len(user_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "users": user_list
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There is no one in the user database."
        }
    ), 404

@app.route('/pcinterview')
def get_all_pcinterview():
    pcinterview_list = nsdb.display_pcinterview()
    if len(pcinterview_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "pcinterview": pcinterview_list
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There is no one in the PC Interview database."
        }
    ), 404

telegramToken=""
if telegramToken == "":
    raise RuntimeError(
        f"the telegramToken was redacted. To test the code, please create your own Telegram bot as per README.md"
    )

async def requestPCInterview(userid):  
    bot = Bot(telegramToken)   
    async with bot:   
        await bot.send_message(text="hello", chat_id=userid)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

