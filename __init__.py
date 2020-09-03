from mycroft import MycroftSkill, intent_file_handler


class IrRemote(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('remote.ir.intent')
    def handle_remote_ir(self, message):
        self.speak_dialog('remote.ir')


def create_skill():
    return IrRemote()

