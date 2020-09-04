from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG
import subprocess

# class IrRemote(MycroftSkill):
#     def __init__(self):
#         MycroftSkill.__init__(self)

#     @intent_file_handler('remote.ir.intent')
#     def handle_remote_ir(self, message):
#         self.speak_dialog('remote.ir')


# def create_skill():
#     return IrRemote()







class IrRemote(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(IrRemote, self).__init__(name="IrRemote")
        
        # Initialize working variables used within the skill.
        self.count = 0
        self.key = ""
        self.device = ""
        self.action = ""

    # The "handle_xxxx_intent" function is triggered by Mycroft when the
    # skill's intent is matched.  The intent is defined by the IntentBuilder()
    # pieces, and is triggered when the user's utterance matches the pattern
    # defined by the keywords.  In this case, the match occurs when one word
    # is found from each of the files:
    #    vocab/en-us/Hello.voc
    #    vocab/en-us/World.voc
    # In this example that means it would match on utterances like:
    #   'Hello world'
    #   'Howdy you great big world'
    #   'Greetings planet earth'
    @intent_handler(IntentBuilder("").require("Hello").require("World"))
    def handle_hello_world_intent(self, message):
        # In this case, respond by simply speaking a canned response.
        # Mycroft will randomly speak one of the lines from the file
        #    dialogs/en-us/hello.world.dialog
        self.speak_dialog("hello.world")


    @intent_handler(IntentBuilder("").require("Count").require("Action"))
    def handle_count_intent(self, message):
        if message.data["Action"] == "up":
            self.count += 1
        else:  # assume "down"
            self.count -= 1
        self.speak_dialog("count.is.now", data={"count": self.count})


    @intent_handler(IntentBuilder("").require("Device").require("Command").require("Action"))
    def handle_remote_intent(self, message):
        self.device = "LG_AKB72915207"
        if message.data["Command"] in ("volume","audio","sound"): 
            self.action = message.data["Action"] 
            if self.action in ("up", "plus", "app"):
                self.key = "KEY_VOLUMEUP"
            elif self.action in ("down", "minus"):
                self.key = "KEY_VOLUMEDOWN"
            elif self.action == "mute":
                self.key = "KEY_MUTE"
            self.speak_dialog("action.volume", data={"action": self.action})

        if message.data["Command"] == "power":
            self.key = "KEY_POWER" 

        self.send_command()

    @intent_handler(IntentBuilder("").require("Command").require("Action"))
    def handle_remote_intent_2(self, message):
        self.device = "LG_AKB72915207"
        if message.data["Command"] == "volume": 
            self.action = message.data["Action"] 
            if self.action == "up":
                self.key = "KEY_VOLUMEUP"
            elif self.action == "down":
                self.key = "KEY_VOLUMEDOWN"
            elif self.action == "mute":
                self.key = "KEY_MUTE"
            self.speak_dialog("action.volume", data={"action": self.action})

        if message.data["Command"] == "power":
            self.key = "KEY_POWER" 
            
        self.send_command()


    def send_command(self):
        subprocess.run(["irsend", "SEND_ONCE", self.device, self.key])
        self.key = ""
        self.device = ""
        self.action = ""
        # irsend SEND_ONCE Samsung_00056A KEY_POWER
    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, there is no need to override it.  If you DO
    # need to implement stop, you should return True to indicate you handled
    # it.
    #
    # def stop(self):
    #    return False

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return IrRemote()

