from collections import OrderedDict
from skpy import SkypeEventLoop, SkypeChatMemberEvent, SkypeMessageEvent


class EventManager(SkypeEventLoop):
    def __init__(self, user, pwd, member_event=None, chat_event=None):
        super(EventManager, self).__init__(user, pwd)
        self.member_event = member_event
        self.chat_event = chat_event

    def onEvent(self, event):
        if isinstance(event, SkypeChatMemberEvent):
            if self.member_event is not None:
                self.member_event(self, event.users, event.chat)

        elif isinstance(event, SkypeMessageEvent):
            if self.chat_event is not None:
                self.chat_event(self, event.msg)


class Server:
    def __init__(self):
        self.rooms = OrderedDict()
        self.skype = None

    def login(self, usr, pwd, member_event=None, chat_event=None):
        self.skype = EventManager(usr, pwd, member_event, chat_event)

    def create_room(self, title):
        if title not in self.rooms.keys():
            room = self.skype.chats.create()
            room.setOpen(True)
            room.setTopic(title)
            self.rooms[title] = room
            return True
        else:
            return False
