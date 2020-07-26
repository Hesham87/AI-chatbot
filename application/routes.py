from application import app
from flask import render_template, request

@app.route("/")
def index():
    return render_template("chatPage.html")
# @app.route("/get")
# def get_bot_response():
#     userText = request.args.get('msg')
#     return str(Bot.reply('localuser', userText))