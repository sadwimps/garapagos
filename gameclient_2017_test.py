# coding: utf-8
# ----------------------------------------------------------
# 陣取ゲーム クライアント（2017年度下期プロコン用）
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
# 定数宣言
# --------------------------------------
G_TRUE = 0            # 正常判定
G_FALSE = -1          # エラー判定
G_MAXPLACE = 49       # 陣地の最大数
G_ROW = 7             # 陣地を並べる行数
G_COL = 7             # 陣地を並べる列数
G_SENTE = 1           # 先手
G_GOTE = -1           # 後手
G_MANPC = 0           # 人対PCモード
G_MANCOM = 1          # 人対通信モード
G_PCCOM = 2           # PC対通信モード
G_GETSENTE = 99       # 先手の取得陣地
G_GETGOTE = -99       # 後手の取得陣地

# --------------------------------------
# モジュールimport
# --------------------------------------
import tkinter as tk    # GUIモジュール
import random  as rd    # 乱数モジュール
import datetime as dt   # 日付モジュール
import time as tm       # 時間モジュール
import socket as sk     # ソケットモジュール
import threading as th  # スレッドモジュール
# import numpy as np

# --------------------------------------
# メインWindowの準備＆表示
# --------------------------------------
g_winBase = tk.Tk()
g_winBase.title(u'陣取ゲーム')
# --------------------------------------
# メインFrameの準備＆表示
# --------------------------------------
g_frmMain = tk.Frame(g_winBase, width=630, height=365)
g_frmMain.pack()
# --------------------------------------
# 初期Frameの準備＆表示
# --------------------------------------
g_frmStart = tk.Frame(g_winBase, width=630, height=365)                         # 初期Frameの生成
g_frmStart.place(x=0, y=0)                                                      # 初期Frameの表示
g_ivMode = tk.IntVar()                                                          # 対戦モードを用意（人対PC=0、人対通信=1、PC対通信=2）
g_ivMode.set(G_MANPC)                                                           # 対戦モードを人対PCで初期化
g_lblMode = tk.Label(g_frmStart, text=u'＜対戦モード選択＞')                    # 対戦モード選択タイトルの生成
g_rdbManPc  = tk.Radiobutton(g_frmStart, text=u'人 対 PC', variable=g_ivMode, value=G_MANPC)    # 人対PCボタンの生成
g_rdbManCom = tk.Radiobutton(g_frmStart, text=u'人 対 通信', variable=g_ivMode, value=G_MANCOM) # 人対通信ボタンの生成
g_rdbPcCom  = tk.Radiobutton(g_frmStart, text=u'PC 対 通信', variable=g_ivMode, value=G_PCCOM)  # PC対通信ボタンの生成
g_lblTeam = tk.Label(g_frmStart, text=u'チーム名：')                            # チーム名タイトルの生成
g_strTeam = tk.StringVar()                                                      # チーム名入力文字格納変数
g_entTeam = tk.Entry(g_frmStart, textvariable=g_strTeam, state='normal')        # チーム名入力エリアの生成
g_lblIpadd = tk.Label(g_frmStart, text=u'接続先IPアドレス：')                   # 接続先IPアドレスタイトルの生成
g_strIpadd = tk.StringVar()                                                     # 接続先IPアドレス入力文字格納変数
g_entIpadd = tk.Entry(g_frmStart, textvariable=g_strIpadd, state='normal')      # 接続先IPアドレス入力エリアの生成
g_lblPort = tk.Label(g_frmStart, text=u'接続ポート番号：')                      # 接続ポート番号タイトルの生成
g_strPort = tk.StringVar()                                                      # 接続ポート番号入力文字格納変数
g_entPort = tk.Entry(g_frmStart, textvariable=g_strPort, state='normal')        # 接続ポート番号入力エリアの生成

# --------------------------------------
# Log表示エリアの準備＆表示
# --------------------------------------
# ログ用LabelFrameの生成＆表示
g_lfrmLog = tk.LabelFrame(g_frmMain, width=610, height=135, text=u' ＜ 対戦LOG ＞ ', relief='sunken', borderwidth=5)
g_lfrmLog.place(x=10, y=220)
# ログ用Listboxの生成
g_lbLog = tk.Listbox(g_lfrmLog, width=82, height=6, bg='silver')
# ログ用Scrollbarの生成
g_sbLog1 = tk.Scrollbar(g_lfrmLog, orient='v', command=g_lbLog.yview)
# ログ用Listboxへログ用Scrollbarを設定
g_lbLog.configure(yscrollcommand=g_sbLog1.set)
# ログ用Listbox、ログ用Scrollbarの表示
g_lbLog.place(x=5, y=0)
g_sbLog1.place(x=585, y=0, height=100)

# --------------------------------------
# 指し手入力エリアの準備
# --------------------------------------
g_ivPlay = tk.IntVar()                                                      # プレーヤー手番を用意（先手=0、後手=1）
g_ivPlay.set(G_SENTE)                                                       # プレーヤー手番を先手で初期化
g_rdbSente = tk.Radiobutton(g_frmMain, text=u'赤：先手', fg='red', variable=g_ivPlay, value=G_SENTE)   # 先手ボタンの生成
g_rdbGote = tk.Radiobutton(g_frmMain, text=u'青：後手', fg='blue', variable=g_ivPlay, value=G_GOTE)   # 後手ボタンの生成
g_lblInput = tk.Label(g_frmMain, text=u'次の一手：')                        # 入力タイトルの生成
g_strInput = tk.StringVar()                                                 # 指し手入力文字格納変数
g_entInput = tk.Entry(g_frmMain, textvariable=g_strInput, state='disabled') # 指し手入力エリアの生成

# --------------------------------------
# 各ボタンの準備
# --------------------------------------
g_btnSelect = tk.Button(g_frmStart, text='Select', width=8)             # Selectボタンの生成
g_btnEnd = tk.Button(g_frmStart, text='End', width=8)                   # Endボタンの生成
g_btnStart = tk.Button(g_frmMain, text='Start', width=8)                # Startボタンの生成
g_btnGet = tk.Button(g_frmMain, text='Get', width=8, state='disabled')  # Getボタンの生成
g_btnReset = tk.Button(g_frmMain, text='Reset', width=8)                # Resetボタンの生成
g_btnExit = tk.Button(g_frmMain, text='Exit', width=8)                  # Exitボタンの生成

# --------------------------------------
# 通信の準備
# --------------------------------------
g_skServer = sk.socket(sk.AF_INET, sk.SOCK_STREAM) # サーバ接続用ソケットを生成

# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# --------------------------------------
# 状態保持変数 (思考ロジックに必要なら追加)
# --------------------------------------
g_ivTeban = tk.IntVar()              # 現在の手番（先手番=G_SENTE、後手番=G_GOTE）
g_lstPlaceStat = [0]*G_MAXPLACE      # 陣地状態リストをゼロで初期化
g_lstLivePlace = []                  # 残存陣地リストのみを格納するリストを用意
g_lstZeroPlace = []                  # 取得可能陣地リストのみを格納するリストを用意
g_ivWin = tk.IntVar()                # 勝利判定
g_lstPlace = []                      # 残存陣地から取得可能陣地を引く値を格納(+1 or -1を算出)
g_lstZeroPlaceInt = []

# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

# --------------------------------------
# 陣地の準備
# --------------------------------------
g_lstPlaceLabel = []                 # 陣地表示リストを用意
for i in range(G_MAXPLACE):          # 陣地の数だけループ
    # 陣地表示リストに陣地ラベルを格納
    g_lstPlaceLabel.append(tk.Label(g_frmMain, text='{0:02d}'.format(i), fg='black', bg='white', width=5, height=2, relief='ridge'))
    # 残存陣地リストにすべての陣地を設定
    g_lstLivePlace.append('{0:02d}'.format(i))
    g_lstZeroPlace.append('{0:02d}'.format(i))

# --------------------------------------
# 陣地の表示
# --------------------------------------
x = 0                      # 陣地リストのインデックスを用意
for i in range(G_ROW):     # 陣地を表示する行の数だけループ
    for j in range(G_COL): # 陣地を表示する列の数だけループ
        # 陣地を所定の位置に表示
        g_lstPlaceLabel[x].place(x=10+j*38, y=5+i*30)
        x = x+1            # 陣地リストのインデックスをインクリメント

# ----------------------------------------------------------
# Log出力関数
#
#     引数：ログに出力する文字列
#     戻値：なし
# ----------------------------------------------------------
def fncPrintLog(a_strText):
    dtNow = dt.datetime.now()                            # 現在日時を取得
    strNow = '<'+dtNow.strftime('%Y/%m/%d %H:%M:%S')+'>' # 現在日時を文字列化
    g_lbLog.insert('end', strNow)                        # 画面に現在日時を格納
    g_lbLog.see('end')                                   # 画面で現在日時を表示
    print(strNow)                                        # コンソールに日付を出力
    g_lbLog.insert('end', a_strText)                     # 画面に引数を格納
    g_lbLog.see('end')                                   # 画面で引数を表示
    print(a_strText)                                     # コンソールに引数を出力

# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ----------------------------------------------------------
# 思考ロジック関数（ここを作り込む！）
#
#     引数：なし
#     戻値：取る陣地の番号をカンマ区切で指定した文字列
# ----------------------------------------------------------
def fncThinking():
    # ☆☆陣地の状態を保存するグローバル変数は自由に設定可とする
    # ☆☆その場合は「陣地の準備」、fncResetPlaces()、fncPickupPlace()、fncEffectPlace()の修正を忘れずに！
    # ☆☆「取る陣地の番号をカンマ区切で指定した文字列」が戻値
#    i = len(g_lstZeroPlace)     # 残存陣地の数を取得
#    j = rd.randint(0,i-1)       # 残存陣地のインデックスをランダムに生成

    i = fncTactics()
    return i

#    return g_lstZeroPlace[j]

def fncTactics():
    g_lstPlace[:] = g_lstPlaceStat
    g_lstZeroPlaceInt = list(map(int,g_lstZeroPlace))
    sum_0 = [0] * len(g_lstZeroPlace)               # 1手先、各盤面の回りに0がいくつできるかをカウント
    sum_1 = [0] * len(g_lstZeroPlace)               # 1手先、各盤面の回りに1がいくつできるかをカウント
    index_Min = 0
    for i in range(len(g_lstPlace)):
        g_lstPlace[i] = g_lstPlace[i] + 1           # 盤全てのステータスに+1をする
    k = 0
    for i in g_lstZeroPlaceInt:
        intMod = i % G_COL                          # 取得陣地を列数で割った余り
        intMaxMod = G_COL - 1                       # 余りの最大値

        # 斜左上
        j = i - G_COL - 1                           # 処理対象を取得
        if j >= 0 and intMod > 0:                   # 処理対象が盤面上なら
            if g_lstPlace[j] == 0:
                sum_0[k] = sum_0[k] + 1
            elif g_lstPlace[j] == 1:
                sum_1[k] = sum_1[k] + 1
        else:
            sum_0[k] = sum_0[k] + 1
            sum_1[k] = sum_1[k] + 1

        # 真上を処理
        j = i - G_COL                               # 処理対象を取得
        if j >= 0:                                  # 処理対象が盤面上なら
            if g_lstPlace[j] == 0:
                sum_0[k] = sum_0[k] + 1
            elif g_lstPlace[j] == 1:
                sum_1[k] = sum_1[k] + 1
        else:
            sum_0[k] = sum_0[k] + 1
            sum_1[k] = sum_1[k] + 1

        # 斜右上を処理
        j = i - G_COL + 1                           # 処理対象を取得
        if j >= 0 and intMod < intMaxMod:           # 処理対象が盤面上なら
            if g_lstPlace[j] == 0:
                sum_0[k] = sum_0[k] + 1
            elif g_lstPlace[j] == 1:
                sum_1[k] = sum_1[k] + 1
        else:
            sum_0[k] = sum_0[k] + 1
            sum_1[k] = sum_1[k] + 1

        # 左横を処理
        j = i - 1                                   # 処理対象を取得
        if j >= 0 and intMod > 0:                   # 処理対象が盤面上なら
            if g_lstPlace[j] == 0:
                sum_0[k] = sum_0[k] + 1
            elif g_lstPlace[j] == 1:
                sum_1[k] = sum_1[k] + 1
        else:
            sum_0[k] = sum_0[k] + 1
            sum_1[k] = sum_1[k] + 1

        # 右横を処理
        j = i + 1                                   # 処理対象を取得
        if j < G_MAXPLACE and intMod < intMaxMod:   # 処理対象が盤面上なら
            if g_lstPlace[j] == 0:
                sum_0[k] = sum_0[k] + 1
            elif g_lstPlace[j] == 1:
                sum_1[k] = sum_1[k] + 1
        else:
            sum_0[k] = sum_0[k] + 1
            sum_1[k] = sum_1[k] + 1

        # 斜左下を処理
        j = i + G_COL - 1                           # 処理対象を取得
        if j < G_MAXPLACE and intMod > 0:           # 処理対象が盤面上なら
            if g_lstPlace[j] == 0:
                sum_0[k] = sum_0[k] + 1
            elif g_lstPlace[j] == 1:
                sum_1[k] = sum_1[k] + 1
        else:
            sum_0[k] = sum_0[k] + 1
            sum_1[k] = sum_1[k] + 1

        # 真下を処理
        j = i + G_COL                               # 処理対象を取得
        if j < G_MAXPLACE:                          # 処理対象が盤面上なら
            if g_lstPlace[j] == 0:
                sum_0[k] = sum_0[k] + 1
            elif g_lstPlace[j] == 1:
                sum_1[k] = sum_1[k] + 1
        else:
            sum_0[k] = sum_0[k] + 1
            sum_1[k] = sum_1[k] + 1

        # 斜右下を処理
        j = i + G_COL + 1                           # 処理対象を取得
        if j < G_MAXPLACE and intMod < intMaxMod:   # 処理対象が盤面上なら
            if g_lstPlace[j] == 0:
                sum_0[k] = sum_0[k] + 1
            elif g_lstPlace[j] == 1:
                sum_1[k] = sum_1[k] + 1
        else:
            sum_0[k] = sum_0[k] + 1
            sum_1[k] = sum_1[k] + 1

        k = k + 1

    for m in range(len(g_lstZeroPlace)):
        index_Min = sum_0.index(min(sum_0))
        print("sum_0")
        print(sum_0)
        print("-----------------------------------")
        print("g_lstZeroPlaceInt")
        print(g_lstZeroPlaceInt)
        print("-----------------------------------")





        # print(index_Min)
        # if index_Min in g_lstZeroPlaceInt:
        #     index_Min = g_lstZeroPlaceInt.index(index_Min)
        #     print("true")
        #     print(index_Min)
        #     break
        # else:
        #     print("false")
        #     print(index_Min)
        #     sum_0[index_Min] = sum_0[index_Min] + 99

    # return index_Min
    return g_lstZeroPlace[index_Min]

# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ----------------------------------------------------------
# 勝敗処理関数（デモンストレーションはここを作り込む！）
#
#     引数：真(G_TRUE)/偽(G_FLASE)
#     戻値：なし
# ----------------------------------------------------------
def fncWin(a_intTF):
    if a_intTF == G_TRUE:                                       # 引数が真なら勝利判定
        intWin = g_ivWin.get()                                  # 勝利判定を取得
        if intWin > 0:                                          # 先手が勝利なら
            intWinner = int((G_MAXPLACE + intWin) / 2)          # 陣地数を算出
            strWinner = '{0:02d}'.format(intWinner) + u' 対 ' + '{0:02d}'.format(G_MAXPLACE - intWinner) + u' にて赤の勝利！！'
        else:                                                   # 後手が勝利なら
            intWinner = int((G_MAXPLACE - intWin) / 2)          # 陣地数を算出
            strWinner = '{0:02d}'.format(G_MAXPLACE - intWinner) + u' 対 ' + '{0:02d}'.format(intWinner) + u' にて青の勝利！！'
    else:                                                       # 偽なら反則負け
        if g_ivTeban.get() == G_SENTE:                          # 手番が先手なら
            strWinner = u'青の勝利！！'                         # 後手を勝者としたログ文字を設定
        else:                                                   # 手番が後手なら
            strWinner = u'赤の勝利！！'                         # 先手を勝者としたログ文字を設定
    fncPrintLog(strWinner)                                      # ログに勝者を出力
    g_entInput.configure(state='disabled')                      # 指し手入力を使用不可
    g_btnGet.configure(state='disabled')                        # Getボタンを使用不可

# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

# ----------------------------------------------------------
# 陣地の表示の初期化関数
#
#     引数：なし
#     戻値：なし
# ----------------------------------------------------------
def fncResetPlaces():
    del g_lstLivePlace[:]                                                  # 残存陣地リストを全クリア
    del g_lstZeroPlace[:]                                                  # 取得可能陣地リストを全クリア
    for i in range(G_MAXPLACE):                                            # 陣地の数だけループ
        g_lstPlaceLabel[i].config(text=('{0:02d}'.format(i)), fg='black', bg='white', relief='ridge')   # 陣地を表示
        g_lstPlaceStat[i] = 0                                              # 陣地状態リストをゼロで初期化
        g_lstLivePlace.append('{0:02d}'.format(i))                         # 残存陣地リストにすべての陣地を設定
        g_lstZeroPlace.append('{0:02d}'.format(i))                         # 取得可能陣地リストにすべての陣地を設定
    g_strInput.set('')                          # 陣地の指定をクリア
    g_rdbSente.configure(state='normal')        # 先手を使用可能
    g_rdbGote.configure(state='normal')         # 後手を使用可能
    g_btnStart.configure(state='normal')        # Startボタンを使用可能
    g_entInput.configure(state='disabled')      # 指し手入力を使用不可
    g_btnGet.configure(state='disabled')        # Getボタンを使用不可

# ----------------------------------------------------------
# メイン画面入力を使用不可にする関数
#
#     引数：なし
#     戻値：なし
# ----------------------------------------------------------
def fncDisabledMainFrame():
    g_entInput.configure(state='disabled')          # 指し手入力を使用不可
    g_btnGet.configure(state='disabled')            # Getボタンを使用不可
    g_btnReset.configure(state='disabled')          # Resetボタンを使用不可
    g_btnExit.configure(state='disabled')           # Exitボタンを使用不可
    g_lstPlaceLabel[0].update()                     # 再描画

# ----------------------------------------------------------
# メイン画面入力を使用可にする関数
#
#     引数：なし
#     戻値：なし
# ----------------------------------------------------------
def fncNormalMainFrame():
    g_entInput.configure(state='normal')            # 指し手入力を使用不可
    g_btnGet.configure(state='normal')              # Getボタンを使用不可
    g_btnReset.configure(state='normal')            # Resetボタンを使用不可
    g_btnExit.configure(state='normal')             # Exitボタンを使用不可
    g_lstPlaceLabel[0].update()                     # 再描画

# ----------------------------------------------------------
# 単数の陣地を取る関数
#
#     引数：取る陣地の番号の文字列
#     戻値：正常(G_TRUE)もしくはエラー(G_FALSE)
# ----------------------------------------------------------
def fncPickupPlace(a_strPlace):
    i = int(a_strPlace)                 # 引数を数値化
    if i < 0 or i > (G_MAXPLACE -1):    # 存在しないインデックスなら
        return G_FALSE                  # エラーを返す
    try:                                       # 例外を監視
        j = g_lstZeroPlace.index(a_strPlace)   # 取得可能陣地リストを引数で検索
    except:                                    # 例外が発生したら
        return G_FALSE                         # 取得が不可と判断してエラーを返す
    intWin = g_ivWin.get()              # 勝利判定を取得
    if g_ivTeban.get() == G_SENTE:      # 先手ならば
        strColor = 'red'                # 取った陣地は赤表示
        k = G_GETSENTE                  # 先手占有状態
        g_ivWin.set(intWin  + 1)        # 勝利判定を＋１
    else :                              # 後手ならば
        strColor = 'blue'               # 取った陣地は青表示
        k = G_GETGOTE                   # 後手占有状態
        g_ivWin.set(intWin  - 1)        # 勝利判定を－１
    fncDisabledMainFrame()              # メイン画面入力を使用不可
    for l in range(3):                  # 取得陣地をフラッシュ
        g_lstPlaceLabel[i].config(fg='black', bg='white')   # 陣地を表示
        g_lstPlaceLabel[i].update()                         # 再描画
        tm.sleep(0.1)                                       # ウェイト
        g_lstPlaceLabel[i].config(fg='white', bg=strColor)  # 陣地を表示
        g_lstPlaceLabel[i].update()                         # 再描画
        tm.sleep(0.1)                                       # ウェイト
    fncNormalMainFrame()                # メイン画面を使用可
    g_lstPlaceStat[i] = k               # 陣地状態を占有に設定
    g_lstLivePlace.remove(a_strPlace)   # 残存陣地リストから該当を削除
    g_lstZeroPlace.remove(a_strPlace)   # 取得可能陣地リストから該当を削除
    return G_TRUE                       # 正常を返す

# ----------------------------------------------------------
# 取得陣地の影響を個別反映する関数
#
#     引数：該当陣地
#     引数：影響度変化
#     引数：陣地表示色
#     戻値：正常(G_TRUE)もしくはエラー(G_FALSE)
# ----------------------------------------------------------
def fncEffectPlace(a_intIndex, a_intCnt, a_strColor):
    i = g_lstPlaceStat[a_intIndex]              # 処理対象の影響度を取得
    if i == G_GETSENTE or i == G_GETGOTE:       # 取得済み陣地ならば
        return G_TRUE                           # 何もせず正常を返す
    i = i + a_intCnt                            # 処理対象の影響度を変化
    g_lstPlaceStat[a_intIndex] = i              # 変化した影響度をリストに格納
    if i == 0:                                  # 変化して影響度がゼロに戻ったなら
        g_lstPlaceLabel[a_intIndex].config(text='{0:02d}'.format(a_intIndex), bg='white')   # インデックスを白色表示
        g_lstZeroPlace.append('{0:02d}'.format(a_intIndex))                                 # 取得可能陣地リストに該当を復活
        g_lstZeroPlace.sort()                                                               # 取得可能陣地リストをソート
    else:                                       # 変化した影響度で陣地化したなら
        g_lstPlaceLabel[a_intIndex].config(text='{0:+d}'.format(i))                         # 影響度を表示
        try:
            g_lstZeroPlace.remove('{0:02d}'.format(a_intIndex))                             # 取得可能陣地リストから該当を削除
        except:                                                                             # 既に削除済みなら無視
            return G_TRUE                                                                   # 正常を返す
        g_lstPlaceLabel[a_intIndex].config(bg=a_strColor)                                   # 表示色を変更
    g_lstPlaceLabel[a_intIndex].update()                                                    # 画面を再描画
    intWin = g_ivWin.get()                                                                  # 勝利判定を取得
    g_ivWin.set(intWin + a_intCnt)                                                          # 取得可能陣地を陣地化したら勝利判定に反映
    return G_TRUE                               # 正常を返す

# ----------------------------------------------------------
# 取得陣地の影響を反映する関数
#
#     引数：取る陣地の番号
#     戻値：正常(G_TRUE)もしくはエラー(G_FALSE)
# ----------------------------------------------------------
def fncCheckPlaces(a_strCheckPlace):
    intPlace = int(a_strCheckPlace)     # 取得陣地を数値化
    intMod = intPlace % G_COL           # 取得陣地を列数で割った余り
    intMaxMod = G_COL - 1               # 余りの最大値
    if g_ivTeban.get() == G_SENTE:      # 先手ならば
        strColor = '#ffdddd'            # 影響陣地は薄赤表示
        intCnt = 1                      # 影響度の変化は+1
    else :                              # 後手ならば
        strColor = '#ddddff'            # 影響陣地は薄青表示
        intCnt = -1                     # 影響度の変化は-1
    # 斜左上を処理
    i = intPlace - G_COL - 1                    # 処理対象を取得
    if i >= 0 and intMod > 0:                   # 処理対象が盤面上なら
        fncEffectPlace(i, intCnt, strColor)     # 効果を反映
    # 真上を処理
    i = intPlace - G_COL                        # 処理対象を取得
    if i >= 0:                                  # 処理対象が盤面上なら
        fncEffectPlace(i, intCnt, strColor)     # 効果を反映
    # 斜右上を処理
    i = intPlace - G_COL + 1                    # 処理対象を取得
    if i >= 0 and intMod < intMaxMod:           # 処理対象が盤面上なら
        fncEffectPlace(i, intCnt, strColor)     # 効果を反映
    # 左横を処理
    i = intPlace - 1                            # 処理対象を取得
    if i >= 0 and intMod > 0:                   # 処理対象が盤面上なら
        fncEffectPlace(i, intCnt, strColor)     # 効果を反映
    # 右横を処理
    i = intPlace + 1                            # 処理対象を取得
    if i < G_MAXPLACE and intMod < intMaxMod:   # 処理対象が盤面上なら
        fncEffectPlace(i, intCnt, strColor)     # 効果を反映
    # 斜左下を処理
    i = intPlace + G_COL - 1                    # 処理対象を取得
    if i < G_MAXPLACE and intMod > 0:           # 処理対象が盤面上なら
        fncEffectPlace(i, intCnt, strColor)     # 効果を反映
    # 真下を処理
    i = intPlace + G_COL                        # 処理対象を取得
    if i < G_MAXPLACE:                          # 処理対象が盤面上なら
        fncEffectPlace(i, intCnt, strColor)     # 効果を反映
    # 斜右下を処理
    i = intPlace + G_COL + 1                    # 処理対象を取得
    if i < G_MAXPLACE and intMod < intMaxMod:   # 処理対象が盤面上なら
        fncEffectPlace(i, intCnt, strColor)     # 効果を反映
    return G_TRUE                               # 正常を返す

# ----------------------------------------------------------
# 複数の陣地を取る関数
#
#     引数：取る陣地の番号を指定した文字列
#     戻値：正常(G_TRUE)もしくはエラー(G_FALSE)
# ----------------------------------------------------------
def fncTakePlaces(a_strTakePlace):
    # 取る陣地の指定が空なら
    if a_strTakePlace == "":
        fncPrintLog(u'取る陣地の数が 0 個と不正です！')
        fncWin(G_FALSE)                     # 勝敗処理を実施
        return G_FALSE                      # エラーを返す
    # 指定陣地が一桁の場合
    strTakePlace = a_strTakePlace
    if len(strTakePlace) == 1:
        strTakePlace = '0' + strTakePlace   # 頭をゼロ埋める
    # 単数の陣地を取る
    if fncPickupPlace(strTakePlace) != G_TRUE:
        fncPrintLog(a_strTakePlace+u'：不正なインデックス '+strTakePlace+u' が指定されました!')
        fncWin(G_FALSE)                     # 勝敗処理を実施
        return G_FALSE                      # エラーを返す
    # 取得陣地の影響を反映
    if fncCheckPlaces(strTakePlace) == G_FALSE:
        fncPrintLog(a_strTakePlace+u'：インデックス '+strTakePlace+u' において影響度がチェックできません!')
        fncWin(G_FALSE)                     # 勝敗処理を実施
        return G_FALSE                      # エラーを返す
    # ログ出力の手番を設定
    if g_ivTeban.get() == G_SENTE:          # 先手なら
        strTeban = u'先手：'                # ログ表示手番を先手に設定
        g_ivTeban.set(G_GOTE)               # 次を後手に設定
    else:                                   # 後手なら
        strTeban = u'後手：'                # ログ表示手番を後手に設定
        g_ivTeban.set(G_SENTE)              # 次を先手に設定
    fncPrintLog(strTeban + a_strTakePlace)  # ログに差し手を出力
    # 勝敗チェック
    intLen = len(g_lstZeroPlace)            # 残った取得可能陣地数を取得
    if intLen == 0:                         # 残った取得可能陣地が0なら
        fncWin(G_TRUE)                      # 勝敗処理を実施
        return G_FALSE                      # 終了を返す
    # 正常にすべての処理が終了
    return G_TRUE                           # 正常を返す

# ----------------------------------------------------------
# サーバ接続関数
#
#     引数：なし
#     戻値：正常(G_TRUE)もしくはエラー(G_FALSE)
# ----------------------------------------------------------
def fncConectServer():
    strTeam = g_strTeam.get()                           # チーム名を取得
    if len(strTeam) == 0:                               # チーム名が空白ならエラー
        fncPrintLog(u'チーム名が指定されていません')    # エラーメッセージを記録
        return G_FALSE                                  # エラーを返す
    strIpadd = g_strIpadd.get()                         # IPアドレスを取得
    if len(strIpadd) == 0:                              # IPアドレスが空白ならエラー
        fncPrintLog(u'IPアドレスが指定されていません')  # エラーメッセージを記録
        return G_FALSE                                  # エラーを返す
    strPort = g_strPort.get()                           # ポート番号を取得
    if len(strPort) == 0:                               # ポート番号が空白ならエラー
        fncPrintLog(u'ポート番号が指定されていません')  # エラーメッセージを記録
        return G_FALSE                                  # エラーを返す
    try:                                                # 例外を監視
        fncPrintLog(u'IP > ' + strIpadd)                # IPアドレスを記録
        fncPrintLog(u'Port > ' + strPort)               # ポート番号を記録
        g_skServer.connect((strIpadd, int(strPort)))    # サーバ接続
        fncPrintLog(u'connect')                         # サーバ接続成功を記録
        g_skServer.send(strTeam.encode('utf-8'))        # チーム名を送信
        bytRecv = g_skServer.recv(4096)                 # 先手後手を受信
        strRecv = bytRecv.decode('utf-8')               # 先手後手をエンコード
        fncPrintLog(u'strRecv >' + strRecv)             # 先手後手を記録
        if int(strRecv) == G_SENTE:                     # 先手なら
            g_ivPlay.set(G_SENTE)                       # 手番表示を先手で初期化
            fncPrintLog(u'先手')                        # 先手を記録
        else:                                           # 後手なら
            g_ivPlay.set(G_GOTE)                        # 手番表示を先手で初期化
            fncPrintLog(u'後手')                        # 先手を記録
        g_skServer.send('OK'.encode('utf-8'))           # OKを送信
    except:                                             # 例外が発生したら
        fncPrintLog(u'接続に失敗しました')              # エラーメッセージを記録
        return G_FALSE                                  # エラーを返す
    fncPrintLog('----- Conect Server -----')            # サーバ接続を記録
    return G_TRUE                                       # 正常を返す

# ----------------------------------------------------------
# 取る陣地を送信する関数
#
#     引数：取る陣地の番号をカンマ区切で指定した文字列
#     戻値：正常(G_TRUE)もしくはエラー(G_FALSE)
# ----------------------------------------------------------
def fncSendPlaces(a_strTakePlace):
    try:                                                # 例外を監視
        g_skServer.send(a_strTakePlace.encode('utf-8')) # 取る陣地を送信
    except:                                             # 例外が発生したら
        fncPrintLog(u'送信に失敗しました')              # エラーメッセージを記録
        return G_FALSE                                  # エラーを返す
    return G_TRUE                                       # 正常を返す

# ----------------------------------------------------------
# 取られた陣地を受信する関数
#
#     引数：なし
#     戻値：取られた陣地の番号をカンマ区切で指定した文字列
# ----------------------------------------------------------
def fncRecvPlaces():
    fncDisabledMainFrame()                              # メイン画面入力を使用不可
    try:                                                # 例外を監視
        bytRecv = g_skServer.recv(4096)                 # 取られた陣地を受信
        strTakePlace = bytRecv.decode('utf-8')          # 取られた陣地を受信
    except:                                             # 例外が発生したら
        fncPrintLog(u'受信に失敗しました')              # エラーメッセージを記録
        strTakePlace = ''                               # エラーを返す
    fncNormalMainFrame()                                # メイン画面を使用可
    return strTakePlace                                 # 取られた陣地を返す

# ----------------------------------------------------------
# メインFrameを通信モードで初期化する関数
#
#     引数：なし
#     戻値：なし
# ----------------------------------------------------------
def fncSetConectFrame():
    g_rdbSente.configure(state='disabled')      # 先手を使用不可
    g_rdbGote.configure(state='disabled')       # 後手を使用不可
    g_btnStart.configure(state='disabled')      # Startボタンを使用不可
    g_entInput.configure(state='normal')        # 指し手入力を使用可能
    g_btnGet.configure(state='normal')          # Getボタンを使用可能
    strTeam = g_strTeam.get()                   # チーム名を取得
    if g_ivPlay.get() == G_SENTE:               # 先手ならば（後手が通信ならば）
        strTeam = strTeam + ' ＜赤：先手＞'     # 画面タイトルに先手を表示
        if fncSendPlaces('00') == G_FALSE:      # ハンディキャップを送信
            return                              # 処理終了
        if fncTakePlaces('00') == G_FALSE:      # ハンディキャップを盤上に反映
            return                              # 処理終了
    else:                                       # 後手ならば（先手が通信ならば）
        strTeam = strTeam + ' ＜青：後手＞'     # 画面タイトルに先手を表示
    g_winBase.title(u'陣取ゲーム：' + strTeam)  # 画面タイトルへチーム名を追加
    strPlaces = fncRecvPlaces()                 # 取られた陣地を受信
    fncTakePlaces(strPlaces)                    # 受信結果を初手に反映
    g_entInput.focus_set()                      # フォーカスの設定

# ----------------------------------------------------------
# メインFrameを通信モードと思考ロジックの初手で初期化する関数
#
#     引数：なし
#     戻値：なし
# ----------------------------------------------------------
def fncSetConectFramePc():
    fncSetConectFrame()                         # メインFrameを通信モードで初期化
    strPlaces = fncThinking()                   # 思考ロジックを呼び出し
    g_strInput.set(strPlaces)                   # 思考ロジックの初手を指し手入力へ設定

# ----------------------------------------------------------
# Selectボタンのクリックイベント関数
#
#     引数：なし
#     戻値：なし
# ----------------------------------------------------------
def fncSelect():
    g_frmMain.configure(cursor='watch')             # マウスカーソルをウォッチに変更
    g_ivTeban.set(G_SENTE)                          # 先手に初期化
    g_frmStart.lower(g_frmMain)                     # 初期Frameを非表示
    intMode = g_ivMode.get()                        # 対戦モードを取得
    if intMode == G_MANCOM:                         # 人対通信ならば
        if fncConectServer() == G_FALSE:            # サーバへ接続
            g_frmStart.tkraise(g_frmMain)           # 初期画面を表示
            g_frmMain.configure(cursor='arrow')     # マウスカーソルを矢印に変更
            return                                  # 接続に失敗したらイベントを終了
        strMode = u'人 対 通信'                     # 表示対戦モードを人対通信に設定
        fncPrintLog('----- Selected Mode --> ' + strMode)   # 対戦モード選択を記録
        fncSetConectFrame()                         # メインFrameを通信モードで初期化
    elif intMode == G_PCCOM:                        # PC対通信ならば
        if fncConectServer() == G_FALSE:            # コネクション
            g_frmStart.tkraise(g_frmMain)           # 初期画面を表示
            g_frmMain.configure(cursor='arrow')     # マウスカーソルを矢印に変更
            return                                  # コネクションに失敗したらイベントを終了
        strMode = u'PC 対 通信'                     # 表示対戦モードをPC対通信に設定
        fncPrintLog('----- Selected Mode --> ' + strMode)   # 対戦モード選択を記録
        fncSetConectFramePc()                       # メインFrameを通信モードと思考ロジックの初手で初期化
    else:                                           # 人対PCならば
        strMode = u'人 対 PC'                       # 表示対戦モード人対PCに設定
        fncPrintLog('----- Selected Mode --> ' + strMode)   # 対戦モード選択を記録
        strTeam = g_strTeam.get()                   # チーム名を取得
        g_winBase.title(u'陣取ゲーム：' + strTeam)  # 画面タイトルへチーム名を追加
    g_frmMain.configure(cursor='arrow')             # マウスカーソルを矢印に変更

# ----------------------------------------------------------
# Selectボタンのクリックイベント関数
#
#     引数：なし
#     戻値：なし
# ----------------------------------------------------------
def fncPushSelect():
    thSelect = th.Thread(target=fncSelect)          # マルチスレッドにSelectボタン処理関数を設定
    thSelect.start()                                # マルチスレッドにてSelectボタン処理を開始

# ----------------------------------------------------------
# Endボタンのクリックイベント関数
#
#     引数：なし
#     戻値：なし
# ----------------------------------------------------------
def fncPushEnd():
    fncPrintLog('----- Game End -----')     # ゲーム終了を記録
    g_winBase.destroy()                     # メインWindowを破棄⇒プログラム終了

# ----------------------------------------------------------
# Startボタンのクリックイベント関数
#
#     引数：なし
#     戻値：なし
# ----------------------------------------------------------
def fncPushStart():
    g_frmMain.configure(cursor='watch')         # マウスカーソルをウォッチに変更
    g_rdbSente.configure(state='disabled')      # 先手を使用不可
    g_rdbGote.configure(state='disabled')       # 後手を使用不可
    g_btnStart.configure(state='disabled')      # Startボタンを使用不可
    g_entInput.configure(state='normal')        # 指し手入力を使用可能
    g_btnGet.configure(state='normal')          # Getボタンを使用可能
    g_ivTeban.set(G_SENTE)                      # 先手に初期化
    g_ivWin.set(0)                              # 勝利判定を初期化
    fncPrintLog('----- New Game Start -----')   # ログにゲーム開始を記録
    if fncTakePlaces('00') == G_FALSE:          # ハンディキャップを設定
        g_frmMain.configure(cursor='arrow')     # マウスカーソルを矢印に変更
        return                                  # エラーが発生したら返す
    if g_ivPlay.get() == G_SENTE:               # プレーヤーが先手なら後手は思考ロジック
        strPlaces = fncThinking()               # 思考ロジックを呼び出し
        fncTakePlaces(strPlaces)                # 思考ロジックの初手を反映
    g_entInput.focus_set()                      # フォーカスの設定
    g_frmMain.configure(cursor='arrow')         # マウスカーソルを矢印に変更

# ----------------------------------------------------------
# Getボタンのクリックイベント関数
#
#     引数：なし
#     戻値：なし
# ----------------------------------------------------------
def fncGet():
    g_frmMain.configure(cursor='watch')             # マウスカーソルをウォッチに変更
    strInput = g_strInput.get()                     # 指定された陣地を取得
    fError = fncTakePlaces(strInput)                # 指定された陣地を取る
    intLen = len(g_lstZeroPlace)                    # 残った取得可能陣地数を取得
    intMode = g_ivMode.get()                        # 対戦モードを取得
    if intMode == G_MANCOM:                         # 人対通信ならば
        fncSendPlaces(strInput)                     # 取る陣地を送信
        if intLen > 0 and fError == G_TRUE:         # 取得可能陣地が存在するなら
            strPlaces = fncRecvPlaces()             # 取られた陣地を受信
            fError = fncTakePlaces(strPlaces)       # 受信結果を反映
        g_strInput.set('')                          # 正常終了なら陣地の指定をクリア
    elif intMode == G_PCCOM:                        # PC対通信ならば
        fncSendPlaces(strInput)                     # 取る陣地を送信
        if intLen > 0 and fError == G_TRUE:         # 取得可能陣地が存在するなら
            strPlaces = fncRecvPlaces()             # 取られた陣地を受信
            fError = fncTakePlaces(strPlaces)       # 受信結果を反映
        intLen = len(g_lstZeroPlace)                # 残った取得可能陣地数を取得
        if intLen > 0 and fError == G_TRUE:         # 取得可能陣地が存在するなら
            strPlaces = fncThinking()               # 思考ロジックを呼び出し
            g_strInput.set(strPlaces)               # 思考ロジックを指し手入力へ設定
    else:                                           # 人対PCならば
        if intLen > 0:                              # 取得可能陣地が存在するなら
            strPlaces = fncThinking()               # 思考ロジックを呼び出し
            fncTakePlaces(strPlaces)                # 思考ロジックの結果を反映
            g_strInput.set('')                      # 陣地の指定をクリア
    g_frmMain.configure(cursor='arrow')             # マウスカーソルを矢印に変更

# ----------------------------------------------------------
# Getボタンのクリックイベント関数
#
#     引数：なし
#     戻値：なし
# ----------------------------------------------------------
def fncPushGet():
    thGet = th.Thread(target=fncGet)                # マルチスレッドにGetボタン処理関数を設定
    thGet.start()                                   # マルチスレッドにてGetボタン処理を開始

# ----------------------------------------------------------
# Exitボタンのクリックイベント関数
#
#     引数：なし
#     戻値：なし
# ----------------------------------------------------------
def fncPushExit():
    fncResetPlaces()                                # 画面を初期化
    intMode = g_ivMode.get()                        # 対戦モードを取得
    if intMode == G_MANCOM or intMode == G_PCCOM:   # 通信モードならば
        g_skServer.close()                          # 通信を切断
        g_rdbManCom.configure(state='disabled')     # 人対通信を選択不可
        g_rdbPcCom.configure(state='disabled')      # PC対通信を選択不可
        g_ivMode.set(G_MANPC)                       # 人対PCを選択
    g_frmStart.tkraise(g_frmMain)                   # 初期画面を表示
    fncPrintLog('----- Game Exit -----')            # 初期画面移行を記録

# ----------------------------------------------------------
# Resetボタンのクリックイベント関数
#
#     引数：なし
#     戻値：なし
# ----------------------------------------------------------
def fncPushReset():
    fncPrintLog('----- Game Reset -----')           # 初期化を記録
    intMode = g_ivMode.get()                        # 対戦モードを取得
    if intMode == G_MANCOM or intMode == G_PCCOM:   # 通信モードならば
        fncPushExit()                               # Exitボタン処理
    else:                                           # 人対PCならば
        fncResetPlaces()                            # 画面を初期化

# --------------------------------------
# 各ボタンへの関数の割り当て
# --------------------------------------
g_btnSelect.configure(command=fncPushSelect)
g_btnEnd.configure(command=fncPushEnd)
g_btnStart.configure(command=fncPushStart)
g_btnGet.configure(command=fncPushGet)
g_btnReset.configure(command=fncPushReset)
g_btnExit.configure(command=fncPushExit)

# --------------------------------------
# 初期画面部品の表示
# --------------------------------------
g_lblMode.place(x=10, y=10)
g_rdbManPc.place(x=20, y=30)
g_rdbManCom.place(x=20, y=50)
g_rdbPcCom.place(x=20, y=70)
g_lblTeam.place(x=10, y=120)
g_entTeam.place(x=120, y=120)
g_lblIpadd.place(x=10, y=150)
g_entIpadd.place(x=120, y=150)
g_lblPort.place(x=10, y=180)
g_entPort.place(x=120, y=180)
g_btnSelect.place(x=10, y=230)
g_btnEnd.place(x=120, y=230)

# --------------------------------------
# メイン画面部品の表示
# --------------------------------------
g_rdbSente.place(x=5+340, y=10)     # 先手を表示
g_rdbGote.place(x=90+340, y=10)     # 後手を表示
g_lblInput.place(x=10+340, y=60)    # 入力タイトルの表示
g_entInput.place(x=92+340, y=60)    # 入力エリアの表示
# --------------------------------------
g_btnStart.place(x=200+340, y=10)   # Startボタンの表示
g_btnGet.place(x=10+340, y=100)     # Getボタンの表示
g_btnReset.place(x=105+340, y=100)  # Resetボタンの表示
g_btnExit.place(x=200+340, y=100)   # Exitボタンの表示
# --------------------------------------
# メインループ開始
# --------------------------------------
tk.mainloop()
