# ----------------------------------------------------------
# 陣取ゲーム サーバ（2017年度下期プロコン用）
# ----------------------------------------------------------
# 開発環境：Python3.5.2
#
# ＜ネーミングルール＞
#   グローバル定数    ：G_大文字
#   グローバル変数    ：g_型略称＋名称（インスタンスでないと変更不可）
#   関数              ：fnc＋動詞＋名称
#   引数              ：a_型略称＋名称
#   ローカル変数      ：型略称＋名称
#   インデックス      ：小文字1文字
#
# 最終更新日：2017/11/29
# ----------------------------------------------------------

# --------------------------------------
# エンコード宣言
# --------------------------------------
# -*- coding: utf-8 -*-

# --------------------------------------
# 定数宣言
# --------------------------------------
G_TRUE = 0            # 正常判定
G_FALSE = -1          # エラー判定
G_MAXSTONE = 35       # 陣地の最大数
G_ROW = 5             # 陣地を並べる行数
G_COL = 7             # 陣地を並べる列数
G_SENTE = 1           # 先手
G_GOTE = -1           # 後手

# --------------------------------------
# モジュールimport
# --------------------------------------
import tkinter as tk    # GUIモジュール
import datetime as dt   # 日付モジュール
import socket as sk     # ソケットモジュール
import threading as th  # スレッドモジュール
import sys              # システムモジュール

# --------------------------------------
# メインWindowの準備＆表示
# --------------------------------------
g_winBase = tk.Tk()
g_winBase.title(u'陣取ゲーム サーバ')
# --------------------------------------
# 初期Frameの準備＆表示
# --------------------------------------
g_frmStart = tk.Frame(g_winBase, width=370, height=220) # 初期Frameの生成
g_frmStart.place(x=0, y=0)                              # 初期Frameの表示位置の設定
g_frmStart.pack()                                       # 初期Frameの表示

g_lblTeam = tk.Label(g_frmStart, text=u'チーム名：')    # チーム名：
g_lblPort = tk.Label(g_frmStart, text=u'ポート番号：')  # ポート番号：

g_lblSente = tk.Label(g_frmStart, text=u'赤：先手', fg='red')                                  # 先手タイトルの生成
g_strSenteTeam = tk.StringVar()                                                                # 先手チーム名入力文字格納変数
g_strSenteTeam.set(u'未接続')                                                                  # 先手チーム名の初期化
g_entSenteTeam = tk.Entry(g_frmStart, textvariable=g_strSenteTeam, state='disabled', width=20, fg='red')    # 先手チーム名入力エリアの生成      
g_strSentePort = tk.StringVar()                                                                # 先手接続ポート番号入力文字格納変数
g_entSentePort = tk.Entry(g_frmStart, textvariable=g_strSentePort, state='normal', width=10, fg='red')      # 先手接続ポート番号入力エリアの生成

g_lblGote = tk.Label(g_frmStart, text=u'青：後手', fg='blue')                                  # 後手タイトルの生成
g_strGoteTeam = tk.StringVar()                                                                 # 先手チーム名入力文字格納変数
g_strGoteTeam.set(u'未接続')                                                                   # 後手チーム名の初期化
g_entGoteTeam = tk.Entry(g_frmStart, textvariable=g_strGoteTeam, state='disabled', width=20, fg='blue')     # 先手チーム名入力エリアの生成      
g_strGotePort = tk.StringVar()                                                                 # 先手接続ポート番号入力文字格納変数
g_entGotePort = tk.Entry(g_frmStart, textvariable=g_strGotePort, state='normal', width=10, fg='blue')       # 先手接続ポート番号入力エリアの生成

# --------------------------------------
# 各ボタンの準備
# --------------------------------------
g_btnSetting = tk.Button(g_frmStart, text='Setting', width=9)           # Settingボタンの生成
g_btnEnd = tk.Button(g_frmStart, text='End', width=9)                   # Endボタンの生成

# --------------------------------------
# 状態保持変数
# --------------------------------------
g_ivTeban = tk.IntVar()              # 現在の手番（先手番=G_SENTE、後手番=G_GOTE）
g_lstPlaceStat = [G_TRUE]*G_MAXSTONE # 陣地状態リストを存在する(正常)で初期化
g_lstLivePlace = []                  # 残存陣地リストのみを格納するリストを用意

# ----------------------------------------------------------
# Log出力関数
#
#     引数：ログに出力する文字列
#     戻値：なし
# ----------------------------------------------------------
def fncPrintLog(a_strText):
    dtNow = dt.datetime.now()                            # 現在日時を取得
    strNow = '<'+dtNow.strftime('%Y/%m/%d %H:%M:%S')+'>' # 現在日時を文字列化
    print(strNow)                                        # コンソールに日付を出力
    print(a_strText)                                     # コンソールに引数を出力

# ----------------------------------------------------------
# サーバ処理関数
#
#     引数：なし
#     戻値：なし
# ----------------------------------------------------------
def fncSetServer():
    g_entSentePort.configure(state='disabled')          # 先手ポート番号入力を使用不可
    g_entGotePort.configure(state='disabled')           # 後手ポート番号入力を使用不可
    g_btnSetting.configure(state='disabled')            # Settingボタンを使用不可
    g_btnEnd.configure(state='disabled')                # Endボタンを使用不可
    g_frmStart.configure(cursor='watch')                # マウスカーソルをウォッチに変更
    try:                                                # 例外を監視
        # 先手設定
        skBaseSente = sk.socket(sk.AF_INET, sk.SOCK_STREAM)       # 先手用ソケットを生成
        skBaseSente.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1) # 先手用ソケットを設定
        strPort = g_strSentePort.get()                  # 先手ポート番号を取得
        skBaseSente.bind(('',int(strPort)))               # IPとPORTを指定して先手バインド
        skBaseSente.listen(10)                            # 接続の待ち受け（キューの最大数を指定）
        sktSente, addSente = skBaseSente.accept()         # 先手PCへ接続
        bytMsg = sktSente.recv(1024)                    # 先手のチーム名を取得
        g_strSenteTeam.set(bytMsg.decode('utf-8'))      # 先手のチーム名を表示
        strSend = str(G_SENTE)                          # 先手を設定
        sktSente.sendall(strSend.encode('utf-8'))       # 先手である事を返す
        bytMsg = sktSente.recv(1024)                    # OKを取得
        fncPrintLog('----- 先手 接続完了 -----')        # 先手 接続完了を記録
        fncPrintLog('先手チーム名 ＞ ' + g_strSenteTeam.get()) # 先手チーム名を記録
        g_lblSente.update()                             # 画面を再描画
        # 後手設定
        skBaseGote = sk.socket(sk.AF_INET, sk.SOCK_STREAM)        # 後手用ソケットを生成
        skBaseGote.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)  # 後手用ソケットを設定
        strPort = g_strGotePort.get()                   # 後手ポート番号を取得
        skBaseGote.bind(('',int(strPort)))                # IPとPORTを指定して後手バインド
        skBaseGote.listen(10)                             # 接続の待ち受け（キューの最大数を指定）
        sktGote, addGote = skBaseGote.accept()            # 後手PCへ接続
        bytMsg = sktGote.recv(1024)                     # 後手のチーム名を取得
        g_strGoteTeam.set(bytMsg.decode('utf-8'))       # 後手のチーム名を表示
        strSend = str(G_GOTE)                           # 後手を設定
        sktGote.sendall(strSend.encode('utf-8'))        # 後手である事を返す
        bytMsg = sktGote.recv(1024)                     # OKを取得
        fncPrintLog('----- 後手 接続完了 -----')               # 後手 接続完了を記録
        fncPrintLog('後手チーム名 ＞ ' + g_strGoteTeam.get())  # 後手チーム名を記録
        g_lblGote.update()                              # 画面を再描画
        fncPrintLog('----- 対局開始 -----')     # 対戦開始を記録
        while True:                             # 無限ループ
            bytMsg = sktSente.recv(1024)        # 先手の指手を受け取る
            strMsg = bytMsg.decode('utf-8')     # 指手をデコード
            if len(strMsg) == 0:                # 指手が空なら
                break                           # ループ終了
            fncPrintLog('先手 ＞ ' + strMsg)    # 先手を記録
            sktGote.sendall(bytMsg)             # 後手に先手の指手を渡す
            bytMsg = sktGote.recv(1024)         # 後手の指手を受け取る
            strMsg = bytMsg.decode('utf-8')     # 指手をデコード
            if len(strMsg) == 0:                # 指手が空なら
                break                           # ループ終了
            fncPrintLog('後手 ＞ ' + strMsg)    # 後手を記録
            sktSente.sendall(bytMsg)            # 先手に後手の指手を渡す
        fncPrintLog('----- 対局終了 -----')     # 対戦終了を記録
        sktSente.close()                        # 先手の接続を切断
        sktGote.close()                         # 後手の接続を切断
    except:                                     # 例外が発生したら
        fncPrintLog('通信エラー発生')           # エラーメッセージを記録
    g_strSenteTeam.set('未接続')                        # 先手のチーム名をクリア
    g_strGoteTeam.set('未接続')                         # 後手のチーム名をクリア
    g_entSentePort.configure(state='normal')            # 先手ポート番号入力を使用可
    g_entGotePort.configure(state='normal')             # 後手ポート番号入力を使用可
    g_btnSetting.configure(state='normal')              # Settingボタンを使用可
    g_btnEnd.configure(state='normal')                  # Endボタンを使用可
    g_frmStart.configure(cursor='arrow')                # マウスカーソルを矢印に変更

# ----------------------------------------------------------
# Settingボタンのクリックイベント関数
#
#     引数：なし
#     戻値：なし
# ----------------------------------------------------------
def fncPushSetting():
    fncPrintLog('----- Game Start -----')       # ゲーム開始を記録
    thServer = th.Thread(target=fncSetServer)   # マルチスレッドにサーバ処理関数を設定
    thServer.start()                            # マルチスレッドにてサーバ処理を開始

# ----------------------------------------------------------
# Endボタンのクリックイベント関数
#
#     引数：なし
#     戻値：なし
# ----------------------------------------------------------
def fncPushEnd():
    fncPrintLog('----- Game End -----')     # ゲーム終了を記録
    sys.exit()                              # プログラム終了

# --------------------------------------
# 各ボタンへの関数の割り当て
# --------------------------------------
g_btnSetting.configure(command=fncPushSetting)
g_btnEnd.configure(command=fncPushEnd)

# --------------------------------------
# 初期画面部品の表示
# --------------------------------------
g_lblTeam.place(x=100, y=15)
g_lblPort.place(x=250, y=15)

g_lblSente.place(x=30, y=50)
g_entSenteTeam.place(x=100, y=50)
g_entSentePort.place(x=250, y=50)

g_lblGote.place(x=30, y=90)
g_entGoteTeam.place(x=100, y=90)
g_entGotePort.place(x=250, y=90)

g_btnSetting.place(x=35, y=150)
g_btnEnd.place(x=245, y=150)

# --------------------------------------
# メインループ開始
# --------------------------------------
tk.mainloop()
