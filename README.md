# Line bot -終極密碼
* Base on line developer
* deploy webhooks on Heroku & AWS.

@670krxjr     
![image](https://github.com/f74066357/TOC-Project-2020/blob/master/670krxjr.png)


## purpose
聚會上炒熱氣氛的經典小遊戲，無須下載即可在line上使用

## API Reference


## Finitie State Machine
![image](https://github.com/f74066357/TOC-Project-2020/blob/master/fsm.png)


## Introduce
A.	經典數字猜猜看(game1)
    玩家選擇猜數字[1~100]->每次猜測會縮小範圍->直到猜中即遊戲結束   
B.  這首歌我知道!(game2)
    機器人傳送一段音訊，使用者在播放後回傳心目中的答案後回傳正確與否
    如果答錯了會傳送正確歌曲名稱
C.  添加game2中的歌曲庫
    傳送歌曲名稱/撥放連結 幫助遊戲變得更多采多姿吧