from transitions.extensions import GraphMachine
from random import randint
from utils import send_text_message
from utils import send_menu

finalnum=0
highest=100
lowest=1
guess=0
class TocMachine(GraphMachine):
    global count
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        
    def is_going_to_menu(self, event):
        text = event.message.text
        return text.lower() == "menu"

    def is_going_to_game(self, event):
        text = event.message.text
        return text == "game"  
    
    def is_going_to_guess(self, event):
        return True

    def is_going_to_hit(self, event):
        global finalnum
        global guess
        text = event.message.text
        guess = int(text) #把字串轉換成整數
        return guess==finalnum

    def guess_again(self, event):
        global finalnum
        global guess
        global highest
        global lowest
        text = event.message.text
        guess = int(text) #把字串轉換成整數
        if(guess>lowest and guess<highest):
            if(guess>finalnum):
                highest=guess
            else:
                lowest=guess
            return guess!=finalnum
        else:
            return False
    
    def on_enter_guess(self, event):
        global highest
        global lowest
        print("I'm entering guess")
        reply_token = event.reply_token
        send_text_message(reply_token,'密碼介於'+str(lowest) + ' - ' + str(highest) + ':')

    def on_exit_menu(self, event):
        print("Leaving guess")

    def on_enter_hit(self, event):
        global highest
        global lowest
        global guess
        print("I'm entering hit")
        reply_token = event.reply_token
        send_text_message(reply_token,"you got it!")
        highest=100
        lowest=1
        guess=0
        self.go_back()

    def on_exit_hit(self):
        print("Leaving hit")

    def on_enter_menu(self, event):
        print("I'm entering menu")
        reply_token = event.reply_token
        send_menu(reply_token)

    def on_exit_menu(self, event):
        print("Leaving menu")

    def on_enter_game(self, event):
        print("I'm entering game")
        global finalnum
        finalnum=randint(1,100)
        reply_token = event.reply_token
        send_text_message(reply_token, "GAME START" + str(finalnum)+'\n'+"輸入任意鍵開始遊戲:")

    def on_exit_game(self, event):
        print("Leaving game")

    def on_enter_guess(self, event):
        print("I'm entering guess")
        reply_token = event.reply_token
        send_text_message(reply_token, '密碼介於'+str(lowest) + ' - ' + str(highest) + ':')

    def on_exit_guess(self, event):
        print("Leaving guess")