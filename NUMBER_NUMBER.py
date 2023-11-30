from tkinter import *
import tkinter.messagebox as msg
from tkinter import scrolledtext

import random
import pygame

####------------関数-----------####
##----関数で使用する変数----##

#乱数を生成し、答えを作る
#乱数を生成し、答えを作る
gen_rand=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
random.shuffle(gen_rand)
rand_num = gen_rand[0:4]

ans = ""        #答え
#整数を文字列に変換
for z in range(0,4):
            ans = ans + str(rand_num[z])
            
#blowカウンター
count_blow = 0

#Hitカウンター
count_hit = 0

#listの行
num_line = 1.0

#あなたのターンかどうか
is_your_turn = False



##----関数の記述----##

##ボタンを押す音
def play_push_sound():
    pygame.mixer.init()
    pygame.mixer.music.load("./music/music1.mp3")
    pygame.mixer.music.play(1)

##受信する音
def play_get_sound():
    pygame.mixer.init()
    pygame.mixer.music.load("./music/music2.mp3")
    pygame.mixer.music.play(1)


##音楽を再生
def play_bgm():
    # 初期化
    pygame.mixer.init()
    # BGMファイルのパスを指定して再生
    pygame.mixer.music.load("./music/015_long_BPM150.mp3")  # ファイルパスを適切なものに変更
    pygame.mixer.music.play(-1)  # -1を指定することでループ再生





#メッセージを表示する
def show_message(title,info):
        
    msg.showinfo(title,info)


    
#ゲームを操作する。
def game_controller(client,send_d,is_your_turn):
    
    #変数
    inp = ""                #受信したデータを格納する
    recived_result = ""     #受信したデータの処理結果を格納する
    sent_result = ""        #送信したデータの処理結果を格納する
    game_result = ""       #ゲーム結果を格納する
    is_going = True       #ゲームを続けるかどうか
    buff = ""               

#####HitとBlowのcountを初期化する#####
    clear_count()

    play_push_sound()


#####あいてのターンの場合#####
    if(is_your_turn==False):
        print("あいてのターンです")
        
        #readyを送信する①
        #print("readyを送信します")
        #send_data(client,"ready")

        
        #データを受信する②
        add_list("あいてがデータを送信するのを待っています...")
        play_get_sound()
        print("データを受信します")
        inp = get_data(client)

        #データを処理する。
        print("データを処理します")
        received_result = hit_or_blow(inp)

        #処理結果を送信する③
        print("処理結果を送信します")
        send_data(client,received_result)


        #相手の処理結果を表示する
        add_list("あいて が処理結果を送信しました。")
        add_list(received_result)

        #ゲームを続けるかどうか送信し、その後の処理を行う④
        #相手がクリアした場合
        if(count_hit == 4):
            print("ゲーム結果を送信します")
            send_data(client,"e")
            
            show_message("敗北","あなたのまけです。\nクリックでゲームを終了します")
            root.destroy()              #ウィンドウを閉じる
        #相手がクリアしていない場合
        else:
            print("ゲーム結果を送信します")
            send_data(client,"g")
            delete_entry()              #入力欄を削除する

            
#####自分のターンの場合#####
    elif(is_your_turn==True):
        print("あなたのターンです")
        

        #####入力内容を審査する。#####
        is_enough_to_send    =   check_entry(send_d)
        if(is_enough_to_send < 0):
            add_list(send_d + " : 再入力してください")
            return

        

        #readyを受信する①
        #print("readyを受信します")
        #buff = get_data(client)

        #データを送信する②
        add_list("あいてがデータを受信するのを待っています...")
        print("データを送信します")
        send_data(client,send_d)

        #処理結果を受信する③
        play_get_sound()
        print("処理結果を受信します")
        sent_result = get_data(client)

        #相手の処理結果を表示する
        add_list("結果："+sent_result)

        #ゲーム結果を受信する④
        print("ゲーム結果を受信します")
        game_result = get_data(client)
        print(game_result)

        #ゲームを続けるかどうかを判断する
        print("ゲームを続けるかどうか判断します。")
        is_going = is_game_going(game_result)

        

        #ゲームを続ける場合
        if(is_going == True):
            print("ゲームを続けます。")
            delete_entry()              #入力欄を削除する

        elif(is_going == False):
            print("ゲームを終了します。")
            show_message("勝利","あなたのかちです。\nクリックでゲームを終了します")
            root.destroy()              #ウィンドウを閉じる
    
    #ターンを変える
    print("ターンを交代します")
    if(is_your_turn==True and is_going==True):
        add_list("")
        add_list("あいてのターンです")
        add_list("[Play]ボタンを押してデータを受信します。")
        change_turn()
    elif(is_your_turn==False and is_going==True):
        add_list("")
        add_list("あなたのターンです")
        add_list("[Play]ボタンを押してデータを送信します。")
        change_turn()

    print("本文へ戻ります")


        

def is_game_going(string):
    if(string=="e"):
        return False
    elif(string=="g"):
        return True

    

#入力されたデータの数を調べる。4ならTrue,それ以外ならFalse
def is_Entry_4(entry):
    if( len(entry)  == 4 ):
        return True
    else:
        return False



#コマンドを実行する
def do_command(com):
    global rand_num
    if(com == 1):
        print("\nゲームを終了します\n")
    elif(com == 2):
        #Hit&Blowの答えを表示する
        show_answer()
               

        
#入力されたデータから文字・数字を判定する。
#文字→コマンドかどうか調べる。その後、コマンドを実行する
#数字→いくつか調べる。
def check_entry(entry):
    if( entry == "q" or entry == "Q" ):
        #entry = 終了コマンド
        return 1
    
    elif(entry == "list"):
        #entry = 答え表示
        return 2
    
    elif(is_Entry_4(entry) == True and entry.isdigit() == True):
        #entry = 4桁の数字
        return 3
    else:
        #再入力
        return -1



#引数がhitもしくはblowなのかを判定する。
def hit_or_blow(num):
    global rand_num
    global count_blow
    global count_hit

    numi = list(num)
    answer = rand_num
    result = ""
    
    #------------------------------判定部(HIT判定)---------------------------------#
    for i in range(0,4):
        if(num[i] == str(answer[i]) ):#入力した数が乱数と一致しているかどうか調べる
            count_hit = count_hit+1
            answer[i] = -2
    #------------------------------判定部(BLOW判定)---------------------------------#
    for i in range(0,4):
        for j in range(0,4):
            #print("{0} : {1}".format(int(inp[i]),j))
            if(numi[i] == str(answer[j]) and not i == j):#入力した数が乱数と一致しているかどうか調べる
                count_blow = count_blow+1
                numi[i] = "a"
                answer[j] = -2

    #------------------------------出力部---------------------------------#
    result = num +"  →  HIT:" + str(count_hit) + " , BLOW:" + str(count_blow)
    return result
    
#カウンターを初期化する
def clear_count():
    global count_blow
    global count_hit

    count_blow  = 0
    count_hit   = 0




#stringをlistに追加する
def add_list(string):
    global entry_list
    global num_line
    
    num_line = num_line + 1.0

    entry_list.configure(state='normal')            #テキストボックスを入力不可にする
    entry_list.insert(num_line ,"\n"+str(string))#テキストボックスに文字を追加
    entry_list.configure(state='disabled')          #テキストボックスを入力不可にする
    entry_list.see("end")                           #テキストの最後の列を表示する
    entry_list.update()                             #即座に画面に表示する。


#テキストボックスの中身を削除
def delete_entry():
    global ent1

    ent1.delete(0,END)


def show_answer():
    global ans
    
    show_message("答え","こたえ　：　"+str(ans))


import socket

##文字数を制限するプログラム
def limit_char(string):
    return len(string) <= 4

def change_turn():
    global is_your_turn

    if(is_your_turn==True):
        is_your_turn = False
    elif(is_your_turn==False):
        is_your_turn = True

####接続を開始する
def start_connection(select):

    if(select==1):
        port = 50000
        #サーバとして接続を行う
        print("サーバーとして機能します")
        host = socket.gethostname()     #サーバのホスト名を取得する
        ip = socket.gethostbyname(host) #サーバのIPアドレスを取得する
        print("サーバのIPアドレス:"+str(ip))
        print("サーバのポート番号:"+str(port))
        ser,cli,addr = do_server(port)
        
    elif(select==2):
        #クライアントとして接続を行う
        print("クライアントとして機能します")
        ser_addr = input("サーバのIPアドレスを記入してください：")
        ser_port = input("サーバのポート番号を記入してください：")
        ser = None
        addr = None
        cli = do_client(ser_addr,ser_port)

    else:
        #不正なデータ
        print("クライアントとして機能します")
        ser,cli,addr = None

    return ser,cli,addr

def do_server(port):

    PORT = port
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(("",PORT))
    server.listen()

    client, addr = server.accept()

    return server , client , addr

def do_client(ser_addr,ser_port):
    HOST = ser_addr
    PORT = int(ser_port)

    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((HOST,PORT))

    return client

####データを受信する    
def get_data(client):
    data = client.recv(4096)

    dec_data = data.decode("UTF-8")
    print(dec_data)

    return dec_data

####データを送信する
def send_data(client,data):
    enc_data = bytes(data,'UTF-8')
    
    client.send(enc_data)


####接続を終了する
def close_connection(client,server):
    if(select==1):
        #サーバとして接続を終了する
        server.close()
        client.close()
        
    elif(select==2):
        #クライアントとして接続を行う
        client.close()
 


####------------------------------------本文-----------------------------------####

##----ソケット通信を開始する----##
print("機能を選んでください。")
print("1:サーバ  2:クライアント")
select = int(input(">"))
print("接続を開始します")
my_ser,my_cli,addr = start_connection(select)#サーバとソケットの情報を取得

if(select == 1):        #サーバの場合は先攻
    
    is_your_turn = True
else:                   #クライアントの場合は後攻
    is_your_turn = False
        
##----変数----##
w   =   50
h   =   25
is_Received = False     #データを受信したかどうか


##----処理の記述----##    
root    =   Tk()
root.geometry("800x600")

#大フレームを作成
frm0    = Frame(root)
frm0.pack()



#左フレームを作成
frm1    = Frame(frm0,bg="green")        #中フレームを使って小フレームをまとめる。
frm1.pack(side=LEFT )

frm1_1    = Frame(frm1)        #フレームを使ってラベルとテキストボックスをまとめる
frm1_1.pack()

frm1_2    = Frame(frm1)        #フレームを使ってラベルとテキストボックスをまとめる
frm1_2.pack()

lab0    = Label(frm1_1,text="自分の数字 : "+ans+"\n",font=("Helvetica",20))
lab0.pack(anchor=NE )

lab1    = Label(frm1_1,text="数字を入力してください",font=("Helvetica",20))
lab1.pack(side=LEFT)

vc = frm1_2.register(limit_char)#文字数を制限するプログラム

ent1 = Entry(frm1_2, validate="key", validatecommand=(vc, "%P"),width=4,font=("Helvetica",28))
ent1.pack(side=LEFT)

but1     = Button(frm1_2,text="Play",command=lambda:game_controller(my_cli,ent1.get(),is_your_turn),width=12,height=2)
but1.pack(side=LEFT)

but2     = Button(frm1_2,text="AllClear",command=delete_entry,width=12,height=2)
but2.pack(side=LEFT)



#右フレームを作成
frm2    = Frame(frm0,bg='blue')        #フレームを使ってラベルとテキストボックスをまとめる
frm2.pack(side=RIGHT)


entry_list    = scrolledtext.ScrolledText(frm2,font=("Helvetica",16))
entry_list.configure(state='disabled')      #テキストボックスを入力不可にする
entry_list.pack(expand=True)


#先攻と後攻を表示する
if(select==1):
    add_list("あなたは先攻です。")
    add_list("[Play]ボタンを押してデータを送信します。")
else:
    add_list("あなたは後攻です。")
    add_list("[Play]ボタンを押してデータを受信します。")

#play_bgm()

#ウィンドウを表示
root.mainloop()



##----接続を終了する----##
close_connection(my_cli,my_ser)
print("接続を終了しました")


