import tcod as libtcod
from enum import Enum
import textwrap


class Message:
    def __init__(self, text, color=libtcod.white):
        self.text = text
        self.color = color


class MessageLog:
    def __init__(self, x, width, height):
        self.messages = []
        self.verbosities = []
        self.x = x
        self.width = width
        self.height = height

    

    def add_message(self, message, verbosity=4):
        # Split the message if necessary, among multiple lines
        new_msg_lines = textwrap.wrap(message.text, self.width)

        for line in new_msg_lines:
            # If the buffer is full, remove the first line to make room for the new one
            if len(self.messages) == self.height:
                del self.messages[0]

            # Add the new line as a Message object, with the text and the color
            self.messages.append(Message(line, message.color))


class Verbosity(Enum):
    MAJOR = 1
    DIALOGUE = 2
    GENERAL = 3
    DEBUG = 4