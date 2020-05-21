from collections import OrderedDict
from getpass import getpass
from skpy import SkypeEventLoop, SkypeChatMemberEvent, SkypeMessageEvent


class Server(SkypeEventLoop):
    def __init__(self, user, member_event=None, chat_event=None):
        super(Server, self).__init__(user, getpass())
        self.rooms = OrderedDict()
        self.member_event = member_event
        self.chat_event = chat_event

    def onEvent(self, event):
        if isinstance(event, SkypeChatMemberEvent):
            if self.member_event is not None:
                self.member_event(self, event.users, event.chat)

        elif isinstance(event, SkypeMessageEvent):
            if self.chat_event is not None:
                self.chat_event(self, event.msg)

    def create_room(self, title):
        if title not in self.rooms.keys():
            room = self.chats.create()
            room.setOpen(True)
            room.setTopic(title)
            self.rooms[title] = room
            return True
        else:
            return False
