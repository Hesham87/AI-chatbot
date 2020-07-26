import utilities
from application import app
from rivescript import RiveScript
from application import routes
from flask import render_template,request

Bot = RiveScript()
Bot.load_directory("./brain")
Bot.sort_replies()

@app.route("/")
def creatPage():
    routes.index

@app.route("/get")
def get_bot_response():
    userText = request.args['msg']
    if userText=='v':
        userText = utilities.audio()
        print(userText)
        bot_reply = str(Bot.reply('localuser', userText))
        audio_bot = ""
        i = 0
        while i < len(bot_reply):
            if bot_reply[i] == "<" and bot_reply[i + 1] == "b" and bot_reply[i + 2] == "r" and bot_reply[i + 3] == ">":
                i = i + 3
            else:
                audio_bot += bot_reply[i]
            i += 1

        utilities.speak(audio_bot)

        reply = "-++"+userText+"++-"+bot_reply
        if utilities.current_user != None:
            utilities.add_chat("+ " + userText + "<br>" + "- " + bot_reply)
        return reply
    else:
        bot_reply=str(Bot.reply('localuser', userText))
        audio_bot=""
        i = 0
        while i < len(bot_reply):
            if bot_reply[i] == "<" and bot_reply[i + 1] == "b" and bot_reply[i + 2] == "r" and bot_reply[i + 3] == ">":
                i = i+3
            else:
                audio_bot += bot_reply[i]
            i += 1
        utilities.speak(audio_bot)
        if utilities.current_user != None:
            utilities.add_chat("+ " + userText + "<br>" + "- " + bot_reply)
        return bot_reply

if __name__ == "__main__":
    app.run()
