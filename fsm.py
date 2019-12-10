from transitions.extensions import GraphMachine
from random import randint
from utils import send_text_message
from utils import send_menu
from utils import send_image
from utils import send_audio
from utils import push_message
from utils import display_name
finalnum=0
highest=100
lowest=1
guess=0
songnum=0
songlist=["點水","好不好","追光者","愛著愛著就永遠","我們不一樣","告白氣球","等你下課","句號","怪美的","浪費"]
songurl=[
        "https://k007.kiwi6.com/hotlink/iyoge2q5gp/mp3", #點水
        "https://k007.kiwi6.com/hotlink/msuiwqghhk/mp3", #好不好
        "https://k007.kiwi6.com/hotlink/5fuwirarug/mp3", #追光者
        "https://k007.kiwi6.com/hotlink/9lts8qybr4/mp3", #愛著愛著就永遠
        "https://k007.kiwi6.com/hotlink/39sbn7xkxf/mp3", #我們不一樣
        "https://k007.kiwi6.com/hotlink/8f4ofi1hnq/mp3", #告白氣球
        "https://k007.kiwi6.com/hotlink/nlh96ql89f/mp3", #等你下課
        "https://k007.kiwi6.com/hotlink/6ig3r3cwfd/mp3", #句號
        "https://k007.kiwi6.com/hotlink/j8cjy4o873/mp3", #怪美的
        "https://k007.kiwi6.com/hotlink/iibvj03ewe/mp3"  #浪費
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

    def is_going_to_addsong(self, event):
        text = event.message.text
        return text == "addsong"

    def is_going_to_addname(self, event):
        return True   
    
    def is_going_to_addurl(self, event):
        return True

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
        try:
            guess = int(text) #把字串轉換成整數
        except:
            return False
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
        text = event.message.text
        return text=="不猜了"

    def is_going_to_songagain(self, event):
        global songnum
        global songlist
        text = event.message.text
        return text!="不猜了"and text!=songlist[songnum]

    def on_enter_guess(self, event):
        global highest
        global lowest
        print("I'm entering guess")
        reply_token = event.reply_token
        send_text_message(reply_token,'密碼介於'+str(lowest) + ' - ' + str(highest) + ':')

    def on_exit_menu(self, event):
        print("Leaving guess")

    def on_enter_addsong(self, event):
        print("I'm entering addsong")
        reply_token = event.reply_token
        send_text_message(reply_token,'請遵守下列規則:\n1.輸入正確歌曲名稱,\n2.歌曲長度在1分鐘內\n3.歌曲url需為https開頭的mp3連結\nEX:https://www.sample-videos.com/audio/mp3/crowd-cheering.mp3\n\n請輸入歌曲名:')

    def on_exit_addsong(self, event):
        print("Leaving addsong")

    def on_enter_addname(self, event):
        print("I'm entering addname")
        text = event.message.text
        global songlist
        songlist.append(text)
        reply_token = event.reply_token
        send_text_message(reply_token,'請輸入歌曲連結')

    def on_exit_addname(self, event):
        print("Leaving addname")

    def on_enter_addurl(self, event):
        print("I'm entering addurl")
        text = event.message.text
        global songurl
        songurl.append(text)
        self.go_back()
        reply_token = event.reply_token
        send_text_message(reply_token,'添加歌曲成功\n目前歌曲:'+str(songlist))
        push_message(event,"再次輸入menu選取要的功能吧><")

    def on_exit_addurl(self):
        print("Leaving addurl")

    def on_enter_hit(self, event):
        global highest
        global lowest
        global guess
        print("I'm entering hit")
        reply_token = event.reply_token
        send_image(reply_token)
        username=display_name(event)
        push_message(event,username+" 引爆了炸彈!!")
        highest=100
        lowest=1
        guess=0
        push_message(event,"再次輸入menu選取要的功能吧><")
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
        username=display_name(event)
        send_text_message(reply_token, username+"發起了終極密碼的挑戰\n輸入任意鍵開始遊戲:")

    def on_exit_game1(self, event):
        print("Leaving game1")

    def on_enter_game2(self, event):
        global songnum
        global songlist
        print("I'm entering game2")
        reply_token = event.reply_token
        songnum=randint(0,len(songlist)-1)
        username=display_name(event)
        send_text_message(reply_token,username+"發起了猜歌遊戲!"+"\n輸入\"不猜了\"遊戲結束 公布正解\n輸入任意鍵開始遊戲:")
        self.go_back()

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
        username=display_name(event)
        print(username)
        global songnum
        global songurl
        reply_token = event.reply_token
        send_audio(reply_token,str(songurl[songnum]))

    def on_exit_song(self, event):
        print("Leaving song")

    def on_enter_again(self, event):
        print("I'm entering again")
        username=display_name(event)
        print(username)
        reply_token = event.reply_token
        send_text_message(reply_token,username+'答錯啦 再猜猜看')

    def on_exit_again(self, event):
        print("Leaving again")

    def on_enter_right(self, event):
        print("I'm entering right")
        username=display_name(event)
        reply_token = event.reply_token
        send_text_message(reply_token,username+" 贏得了勝利 恭喜!!!")
        push_message(event,"再次輸入menu選取要的功能吧><")
        self.go_back()

    def on_exit_right(self):
        print("Leaving right")

    def on_enter_wrong(self, event):
        global songnum
        print("I'm entering wrong")
        reply_token = event.reply_token
        send_text_message(reply_token,"遊戲結束~這首歌是 "+songlist[songnum]+" 啦")
        push_message(event,"再次輸入menu選取要的功能吧><")
        self.go_back()

    def on_exit_wrong(self):
        print("Leaving wrong")