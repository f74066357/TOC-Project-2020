from transitions.extensions import GraphMachine
from random import randint
from utils import send_text_message
from utils import send_menu
from utils import send_image
from utils import send_audio
finalnum=0
highest=100
lowest=1
guess=0
songnum=0
songlist=["點水","好不好","追光者"]
songurl=["https://k007.kiwi6.com/hotlink/iyoge2q5gp/mp3", #點水
        "https://k007.kiwi6.com/hotlink/msuiwqghhk/mp3", #好不好
        "https://hao.haolingsheng.com/ring/000/985/6da0d4255bd1d84d71a18ed859a7dac6.mp3" #追光者
        ]
class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        
    def is_going_to_menu(self, event):
        text = event.message.text
        return text.lower() == "menu"

    def is_going_to_game1(self, event):
        text = event.message.text
        return text == "game1"  

    def is_going_to_game2(self, event):
        text = event.message.text
        return text == "game2"
    
    def is_going_to_guess(self, event):
        return True

    def is_going_to_song(self, event):
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
        if(guess>=lowest and guess<=highest):
            if(guess>finalnum):
                highest=guess
            else:
                lowest=guess
            return guess!=finalnum
        else:
            return False

    def is_going_to_right(self, event):
        global songnum
        global songlist
        text = event.message.text
        return text==songlist[songnum]

    def is_going_to_wrong(self, event):
        global songnum
        global songlist
        text = event.message.text
        return text!=songlist[songnum]

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
        send_image(reply_token)
        #send_text_message(reply_token,"you got it!")
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

    def on_enter_game1(self, event):
        print("I'm entering game1")
        global finalnum
        finalnum=randint(1,100)
        reply_token = event.reply_token
        send_text_message(reply_token, "GAME START" + str(finalnum)+'\n'+"輸入任意鍵開始遊戲:")

    def on_exit_game1(self, event):
        print("Leaving game1")

    def on_enter_game2(self, event):
        global songnum
        global songlist
        print("I'm entering game2")
        reply_token = event.reply_token
        songnum=randint(0,2)
        send_text_message(reply_token, "GAME2 START"+"\n"+str(songnum)+songlist[songnum]+"輸入任意鍵開始遊戲:")

    def on_exit_game2(self, event):
        print("Leaving game2")

    def on_enter_guess(self, event):
        print("I'm entering guess")
        reply_token = event.reply_token
        send_text_message(reply_token, '密碼介於'+str(lowest) + ' - ' + str(highest) + ':')

    def on_exit_guess(self, event):
        print("Leaving guess")

    def on_enter_song(self, event):
        print("I'm entering song")
        global songnum
        global songurl
        reply_token = event.reply_token
        send_audio(reply_token,str(songurl[songnum]))

    def on_exit_song(self, event):
        print("Leaving song")

    def on_enter_right(self, event):
        print("I'm entering right")
        reply_token = event.reply_token
        send_text_message(reply_token,"you got it!")
        self.go_back()

    def on_exit_right(self):
        print("Leaving right")

    def on_enter_wrong(self, event):
        global songnum
        print("I'm entering right")
        reply_token = event.reply_token
        send_text_message(reply_token,"錯了 這是"+songlist[songnum])
        self.go_back()

    def on_exit_wrong(self):
        print("Leaving wrong")