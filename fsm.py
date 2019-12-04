from transitions.extensions import GraphMachine

from utils import send_text_message


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_start1(self, event):
        text = event.message.text
        return text.lower() == "go to start1"

    def is_going_to_start2(self, event):
        text = event.message.text
        return text.lower() == "go to start2"

    def on_enter_start1(self, event):
        print("I'm entering start1")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger start1")
        self.go_back()

    def on_exit_start1(self):
        print("Leaving start1")

    def on_enter_start2(self, event):
        print("I'm entering start2")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger start2")
        self.go_back()

    def on_exit_start2(self):
        print("Leaving start2")
