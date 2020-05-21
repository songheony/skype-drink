import threading
from flask import Flask, render_template, request
from skpy import SkypeTextMsg
from server import Server


def parse_chat(html):
    command = None
    content = None
    if html.startswith("/all "):
        command = "all"
        content = html[5:]
    return command, content


def new_member(skype, users, chat):
    pass


def new_chat(skype, msg):
    if isinstance(msg, SkypeTextMsg) and msg.user.id != skype.userId:
        command, content = parse_chat(msg.html)
        if command == "all":
            message = f"{msg.user.name}: {content}"
            for room in skype.rooms:
                if room.id != msg.chat.id:
                    room.sendMsg(message, rich=True)


ID = "jpmansong@gmail.com"
sk = Server()

app = Flask(__name__)


@app.route('/')
def index():
    if sk.skype is None:
        return render_template('login.html')
    else:
        return render_template('index.html', rooms=sk.rooms)


@app.route('/', methods=['POST'])
def login():
    action = request.form['action_type']
    if action == "input_password":
        pwd = request.form['text-password']
        sk.login(ID, pwd, member_event=new_member, chat_event=new_chat)
        sk_thread = threading.Thread(target=sk.skype.loop)
        sk_thread.start()
        return render_template('index.html', rooms=sk.rooms)
    else:
        return "Invalid action"


@app.route('/admin')
def admin():
    return render_template('admin.html', rooms=sk.rooms)


@app.route('/admin', methods=['POST'])
def edit_room():
    action = request.form['action_type']
    if action == "add_room":
        title = request.form['text-add-room']
        sk.create_room(title)
    elif action == "delete_room":
        room_id = request.form['room_id']
        for title, room in sk.rooms.items():
            if room.id == room_id:
                room.leave()
                break
        sk.rooms.pop(title, None)
    elif action == "delete_all":
        for title, room in sk.rooms.items():
            room.leave()
        sk.rooms.clear()
    else:
        return "Invalid action"
    return render_template('admin.html', rooms=sk.rooms)


if __name__ == "__main__":
    app.run(debug=False)
