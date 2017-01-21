# ----------------------------------------------------------
# 石取りゲーム クライアント（2016年度下期プロコン用）
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
# 最終更新日：2016/12/13
# ----------------------------------------------------------

# --------------------------------------
# エンコード宣言
# --------------------------------------
# -*- coding: utf-8 -*-

# --------------------------------------
# 定数宣言
# --------------------------------------
G_TURE = 0            # 正常判定
G_FALSE = -1          # エラー判定
#G_MAXSTONE = 35       # 石の最大数
#G_ROW = 5             # 石を並べる行数
#G_COL = 7             # 石を並べる列数
G_SENTE = 0           # 先手
G_G
OTE = 1            # 後手

G_MANPC = 0           # 人対PCモード
G_MANCOM = 1          # 人対通信モード
G_PCCOM = 2           # PC対通信モード

# --------------------------------------
# 定数宣言 開発用※開発終了したら削除(上のコメント化も戻す)
# --------------------------------------
G_MAXSTONE = 6       # 石の最大数
G_ROW = 2            # 石を並べる行数
G_COL = 3            # 石を並べる列数

# --------------------------------------
# モジュールimport
# --------------------------------------
import tkinter as tk  # GUIモジュール
import random  as rd  # 乱数モジュール
import datetime as dt # 日付モジュール
import socket as sk   # ソケットモジュール
import numpy as np    # 数列処理用

# --------------------------------------
# メインWindowの準備＆表示
# --------------------------------------
g_winBase = tk.Tk()
g_winBase.title(u'石取りゲーム')
# --------------------------------------
# メインFrameの準備＆表示
# --------------------------------------
g_frmMain = tk.Frame(g_winBase, width=630, height=365)
g_frmMain.pack()
# --------------------------------------
# 初期Frameの準備＆表示
# --------------------------------------
g_frmStart = tk.Frame(g_winBase, width=630, height=365)                                         # 初期Frameの生成
g_frmStart.place(x=0, y=0)                                                                      # 初期Frameの表示
g_ivMode = tk.IntVar()                                                                          # 対戦モードを用意（人対PC=0、人対通信=1、PC対通信=2）
g_ivMode.set(G_MANPC)                                                                           # 対戦モードを人対PCで初期化
g_lblMode = tk.Label(g_frmStart, text=u'＜対戦モード選択＞')                                    # 対戦モード選択タイトルの生成
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
g_rdbSente = tk.Radiobutton(g_frmMain, text=u'先手', fg='blue', variable=g_ivPlay, value=G_SENTE)   # 先手ボタンの生成
g_rdbGote = tk.Radiobutton(g_frmMain, text=u'後手', fg='purple', variable=g_ivPlay, value=G_GOTE)   # 後手ボタンの生成
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
g_lstStoneStat = [G_TURE]*G_MAXSTONE # 石状態リストを存在する(正常)で初期化
g_lstLiveStone = []                  # 残存石リストのみを格納するリストを用意

# --------------------------------------
# 状態保持変数 (追加分)
# --------------------------------------
g_lstLiveStone2 = np.array([[]])   # 残存石の2個のペアを格納するリストを用意
g_lstLiveStone3 = np.array([[]])   # 残存石の3個のペアを格納するリストを用意
g_lstLiveStone4 = np.array([[]])   # 残存石の4個のペアを格納するリストを用意

# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

# --------------------------------------
# 石の準備
# --------------------------------------
g_lstStoneLabel = []                 # 石表示リストを用意
for i in range(G_MAXSTONE):          # 石の数だけループ 
    # 石表示リストに石ラベルを格納
    g_lstStoneLabel.append(tk.Label(g_frmMain, text='{0:02d}'.format(i), fg='white', bg='green', width=4, relief='raised'))
    # 残存石リストにすべての石を設定
    g_lstLiveStone.append('{0:02d}'.format(i))

# --------------------------------------
# 石の表示
# --------------------------------------
x = 0                      # 石リストのインデックスを用意
for i in range(G_ROW):     # 石を表示する行の数だけループ
    for j in range(G_COL): # 石を表示する列の数だけループ
        # 石を所定の位置に表示
        g_lstStoneLabel[x].place(x=10+j*48, y=10+i*38)
        x = x+1            # 石リストのインデックスをインクリメント

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
#     戻値：取る石の番号をカンマ区切で指定した文字列
# ----------------------------------------------------------
def fncThinking():
    # ☆☆石の状態を保存するグローバル変数は自由に設定可とする
    # ☆☆その場合は「石の準備」、fncResetStones()、fncPickupStone()での操作を忘れずに！
    # ☆☆「取る石の番号をカンマ区切で指定した文字列」が戻値
    i = len(g_lstLiveStone)     # 残存石の数を取得

# --関数のエラーチェックはここでやります！------------------

    if fncCheckEnd() < 0:
        fncPrintLog('「fncCheckEnd」で何か起きてるよ！')

# ----------------------------------------------------------

# --石のペアの生成はここでやります！------------------
    fncGeneratePair2()
    fncGeneratePair3()
    fncGeneratePair4()

# 詰みの部分------------------------------------------------
    # 詰めない場合はスルー
    if fncCheckEnd() > 0:
        #勝ちパターンA
        if fncCheckEnd() == 1:
            return 0

        #勝ちパターンB
        elif fncCheckEnd() == 2:
            return 0

# 序盤から中盤----------------------------------------------
    j = rd.randint(0,i-1)       # 残存石のインデックスをランダムに生成

    # ゲームの初手らへん------------------------------------



    # 戦況を有利にする部分----------------------------------

    return g_lstLiveStone[j]    # サンプルは残存石を１つランダムに返す

# ----------------------------------------------------------
# 2個の組み合わせを作成しますよ！
# ----------------------------------------------------------
def fncGeneratePair2():
    l_lstCheckStone = []                         # 残存石をチェックする為のリストを用意
    g_lstLiveStone2 = [[]]                       # 残存石のペア配列を初期化

    for i in range(len(g_lstLiveStone)):
        j = j + i
        for j in range(len(g_lstLiveStone) - i - 1):
            l_lstCheckStone[0] = g_lstLiveStone[i]
            l_lstCheckStone[1] = g_lstLiveStone[i + j]
            if fncCheckStones(l_lstCheckStone) == G_TURE:
                g_lstLiveStone2.append(l_lstCheckStone)

        fncPrintLog(len(g_lstLiveStone2))

# ----------------------------------------------------------
# 3個の組み合わせを作成しますよ！
# ----------------------------------------------------------
def fncGeneratePair3():
    l_lstCheckStone = []                         # 残存石をチェックする為のリストを用意
    g_lstLiveStone3 = [[]]                           # 残存石のペア配列を初期化

    for i in range(len(g_lstLiveStone)):
        j = j + i
        for j in range(len(g_lstLiveStone) - i - 1):
            l_lstCheckStone[0] = g_lstLiveStone[i]
            l_lstCheckStone[1] = [i + j]
            for k in range(len(g_lstLiveStone) - i - j - 1):
                l_lstCheckStone[0] = g_lstLiveStone[i]
                l_lstCheckStone[1] = g_lstLiveStone[i + j]
                l_lstCheckStone[1] = g_lstLiveStone[i + j + k]
                if fncCheckStones(l_lstCheckStone) == G_TURE:
                    g_lstLiveStone3.append(l_lstCheckStone)

        fncPrintLog(len(g_lstLiveStone3))

# ----------------------------------------------------------
# 4個の組み合わせを作成しますよ！
# ----------------------------------------------------------
def fncGeneratePair2():
    l_lstCheckStone = []                          # 残存石をチェックする為のリストを用意
    g_lstLiveStone2 = [[]]              # 残存石のペア配列を初期化

    for i in range(len(g_lstLiveStone)):
        j = j + i
        for j in range(len(g_lstLiveStone) - i - 1):
            l_lstCheckStone[0] = g_lstLiveStone[i]
            l_lstCheckStone[1] = [i + j]
            for k in range(len(g_lstLiveStone) - i - j - 1):
                l_lstCheckStone[0] = g_lstLiveStone[i]
                l_lstCheckStone[1] = g_lstLiveStone[i + j]
                l_lstCheckStone[1] = g_lstLiveStone[i + j + k]
                for k in range(len(g_lstLiveStone) - i - j - 1):
                    l_lstCheckStone[0] = g_lstLiveStone[i]
                    l_lstCheckStone[1] = g_lstLiveStone[i + j]
                    l_lstCheckStone[1] = g_lstLiveStone[i + j + k]
                    if fncCheckStones(l_lstCheckStone) == G_TURE:
                        g_lstLiveStone3.append(l_lstCheckStone)

        fncPrintLog(len(g_lstLiveStone4))

# ----------------------------------------------------------
# ここで詰みの部分を作成しますよ！
# ----------------------------------------------------------
def fncCheckEnd():
    # ☆☆終わりパターンに当てはまるかを確認する。
    # パターン0「0」：何も考えない。※どれでもいいので1つをとる場合もこれ（仮）
    # パターンA「1」：離れた1つをとる。
    # パターンB「2」：連続するうちの1つをとる。
    # パターンC「3」：連続するうちの2つをとる。

    #一旦7個以上は考えない。
    if len(g_lstLiveStone) > 7:
        return 0

    #2個のとき
    if len(g_lstLiveStone) == 2:
        return 0

    #3個のとき
    elif len(g_lstLiveStone) == 3:
        #3個バラバラのとき
        #2個と1個のとき
        #3個のとき
        
        return 0

    #4個のとき
    elif len(g_lstLiveStone) == 4:
        return 0

    #5個のとき
    elif len(g_lstLiveStone) == 5:
        return 0

    #6個のとき
    elif len(g_lstLiveStone) == 6:
        return 0

    #7個のとき
    elif len(g_lstLiveStone) == 7:
        return 0

    #念のためエラー回避
    return -1

# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ----------------------------------------------------------
# 勝敗処理関数（デモンストレーションはここを作り込む！）
#
#     引数：真(G_TRUE)/偽(G_FLASE)
#     戻値：なし
# ----------------------------------------------------------
def fncWin(a_intTF):
    # 引数が真なら手番が勝利、偽なら手番が敗北
    intWinnwr = g_ivTeban.get() + a_intTF
    # ログ出力の手番を設定
    if intWinnwr == G_TURE:                 # 先手が勝者なら
        strWinner = u'先手の勝利！！'       # 先手を勝者としたログ文字を設定
    else:                                   # 後手が勝者なら
        strWinner = u'後手の勝利！！'       # 後手を勝者としたログ文字を設定
    fncPrintLog(strWinner)                  # ログに勝者を出力
    g_entInput.configure(state='disabled')  # 指し手入力を使用不可
    g_btnGet.configure(state='disabled')    # Getボタンを使用不可

# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

# ----------------------------------------------------------
# 石の表示の初期化関数
#
#     引数：なし
#     戻値：なし
# ----------------------------------------------------------
def fncResetStones():
    del g_lstLiveStone[:]                                                  # 残存石リストを全クリア
    for i in range(G_MAXSTONE):                                            # 石の数だけループ
        g_lstStoneLabel[i].config(fg='white', bg='green', relief='raised') # 石を表示
        g_lstStoneStat[i] = G_TURE                                         # 石状態リストを存在する(正常)で初期化
        g_lstLiveStone.append('{0:02d}'.format(i))                         # 残存石リストにすべての石を設定

# ----------------------------------------------------------
# 単数の石を取る関数
#
#     引数：取る石の番号の文字列
#     戻値：正常(G_TRUE)もしくはエラー(G_FALSE)
# ----------------------------------------------------------
def fncPickupStone(a_strStone):
    i = int(a_strStone)                 # 引数を数値化
    if i < 0 or i > (G_MAXSTONE -1):    # 存在しないインデックスなら
        return G_FALSE                  # エラーを返す
    elif g_lstStoneStat[i] != G_TURE:   # 石状態が不在なら
        return G_FALSE                  # エラーを返す
    if g_ivTeban.get() == G_SENTE:      # 先手ならば
        strColor = 'blue'               # 取った石は青表示
    else :                              # 後手ならば
        strColor = 'purple'             # 取った石は紫表示
    g_lstStoneLabel[i].config(fg=strColor, bg=strColor, relief='sunken') # 単数の石を非表示化
    g_lstStoneStat[i] = G_FALSE                                          # 石状態を不在(エラー)に設定
    g_lstLiveStone.remove(a_strStone)                                    # 残存石リストから該当を削除
    return G_TURE                                                        # 正常を返す

# ----------------------------------------------------------
# 複数の石の連続性をチェックする関数
#
#     引数：取る石の番号を格納した文字列リスト
#     戻値：正常(G_TRUE)もしくはエラー(G_FALSE)
# ----------------------------------------------------------
def fncCheckStones(a_lstTakeStone):
    i = len(a_lstTakeStone)           # 石の数を取得
    iMin = int(a_lstTakeStone[0])     # 最小値を取得
    iMax = int(a_lstTakeStone[i - 1]) # 最大値を取得

    iMinDiv = int(iMin / G_COL) # 最小を列数で割った整数部
    iMaxDiv = int(iMax / G_COL) # 最大を列数で割った整数部
    iMinMod = iMin % G_COL      # 最小を列数で割った余り
    iMaxMod = iMax % G_COL      # 最大を列数で割った余り

    # 最大が石数＋最小で、最大と最小を列数で割った結果が同じなら
    if iMax == (iMin + i -1) and iMinDiv == iMaxDiv:
        # 横の連続なので
        return G_TURE # 正常を返す

    # 最大が最小＋石数×列数で、
    # 最大を列数で割った余りと最小を列数で割った余りが同じなら
    if iMax == iMin + ((i -1)* G_COL) and iMinMod == iMaxMod:
        # 他に石がなければ縦の連続なので
        if i == 2:
            return G_TURE # 正常を返す
        # 列数で割った余りがすべて同じでないなら
        for j in range(len(a_lstTakeStone)): # 石の数だけループ
            # 石を列数で割った余りがすべて一致しないなら
            if (int(a_lstTakeStone[j]) % G_COL) != iMinMod:
                return G_FALSE # エラーを返す
        # 縦の連続なので
        return G_TURE # 正常を返す

    # 最大が初期値＋長さ×(列数-1)で、
    # 最小を列数で割った余りが最大を列数で割った余りより小さいなら
    if iMax == iMin + ((i - 1) * (G_COL - 1)) and iMinMod > iMaxMod:
	# 列数-1で割った余りがすべて同じでないなら
        for j in range(len(a_lstTakeStone)): # 石の数だけループ
            # 石を列数-1で割った余りがすべて一致しないなら
            if (int(a_lstTakeStone[j]) % (G_COL - 1)) != iMin % (G_COL - 1):
                return -1 # エラーを返す
        # 斜め左の連続なので
        return G_TURE # 正常を返す

    # 最大が初期値＋長さ×(列数+1)で、
    # 最小を列数で割った余りが最大を列数で割った余りより大きいなら
    if iMax == iMin + ((i - 1) * (G_COL + 1)) and iMinMod < iMaxMod:
        # 列数+1で割った余りがすべて同じでないなら
        for j in range(len(a_lstTakeStone)): # 石の数だけループ
            # 石を列数+1で割った余りがすべて一致しないなら
            if (int(a_lstTakeStone[j])) % (G_COL + 1) != iMin % (G_COL + 1):
                return -1 # エラーを返す
        # 斜め右の連続なので
        return G_TURE # 正常を返す

    # どのパターンにも当てはまらなければ
    return G_FALSE # エラーを返す
 
# ----------------------------------------------------------
# 複数の石を取る関数
#
#     引数：取る石の番号をカンマ区切で指定した文字列
#     戻値：正常(G_TRUE)もしくはエラー(G_FALSE)
# ----------------------------------------------------------
def fncTakeStones(a_strTakeStone):
    # 取る石の指定が空なら
    if a_strTakeStone == "":
        fncPrintLog(u'取る石の数が 0 個と不正です！')
        fncWin(G_FALSE)         # 勝敗処理を実施
        return G_FALSE          # エラーを返す
    # 取る石をカンマで分解
    lstTakeStone = a_strTakeStone.split(',')
    # 取る石のインデックスを小さい順に並べ替え
    for i in range(len(lstTakeStone)): # 石の数だけループ
        if len(lstTakeStone[i]) == 1:  # 一桁の場合、
            # ソート順を確保するため頭をゼロ埋め
            lstTakeStone[i] = '0' + lstTakeStone[i]
    lstTakeStone.sort()  # 石の並べ替え
    # 取る石の数が5以上もしくは0未満なら
    i = len(lstTakeStone)
    if i > 4:
        fncPrintLog(a_strTakeStone+u'：取る石の数が ' + str(i) + u' 個と不正です！')
        fncWin(G_FALSE)         # 勝敗処理を実施
        return G_FALSE          # エラーを返す
    # 有効なインデックスかチェック
    # 石が連続していなければ
    if i > 1:
        if fncCheckStones(lstTakeStone) == G_FALSE: # 複数の石の連続性をチェック
            fncPrintLog(a_strTakeStone+u'：指定した石は連続していません！')
            fncWin(G_FALSE)             # 勝敗処理を実施
            return G_FALSE              # エラーを返す
    # 指定した石を取った表示に変更
    for i in range(len(lstTakeStone)):  # 石の数だけループ
        if fncPickupStone(lstTakeStone[i]) != G_TURE: # 単数の石を取る
            fncPrintLog(a_strTakeStone+u'：不正なインデックス '+lstTakeStone[i]+u' が指定されました!')
            fncWin(G_FALSE)             # 勝敗処理を実施
            return G_FALSE              # エラーを返す
    # ログ出力の手番を設定
    if g_ivTeban.get() == G_SENTE:          # 先手なら
        strTeban = u'先手：'                # ログ表示手番を先手に設定
        g_ivTeban.set(G_GOTE)               # 次を後手に設定
    else:                                   # 後手なら
        strTeban = u'後手：'                # ログ表示手番を後手に設定
        g_ivTeban.set(G_SENTE)              # 次を先手に設定
    fncPrintLog(strTeban + a_strTakeStone)  # ログに差し手を出力
    # 勝敗チェック
    intLen = len(g_lstLiveStone)            # 残った石数を取得
    if intLen == 1:                         # 残った石が1つなら
        fncWin(G_FALSE)                     # 勝敗処理を実施
        return G_FALSE                      # エラーを返す
    elif intLen == 0:                       # 残った石が0なら
        fncWin(G_TURE)                      # 勝敗処理を実施
        return G_FALSE                      # エラーを返す
    # 正常にすべての処理が終了
    return G_TURE                           # 正常を返す

# ----------------------------------------------------------
# サーバ接続関数
#
#     引数：なし
#     戻値：正常(G_TRUE)もしくはエラー(G_FALSE)
# ----------------------------------------------------------
def fncConectServer():
    strTeam = g_strTeam.get()                          # チーム名を取得
    if len(strTeam) == 0:                              # チーム名が空白ならエラー
        fncPrintLog(u'チーム名が指定されていません')   # エラーメッセージを記録
        return G_FALSE                                 # エラーを返す
    strIpadd = g_strIpadd.get()                        # IPアドレスを取得
    if len(strIpadd) == 0:                             # IPアドレスが空白ならエラー
        fncPrintLog(u'IPアドレスが指定されていません') # エラーメッセージを記録
        return G_FALSE                                 # エラーを返す
    strPort = g_strPort.get()                          # ポート番号を取得
    if len(strPort) == 0:                              # ポート番号が空白ならエラー
        fncPrintLog(u'ポート番号が指定されていません') # エラーメッセージを記録
        return G_FALSE                                 # エラーを返す
    try:                                               # 例外を監視
        g_skServer.connect(strIpadd, int(strPort))     # サーバ接続
        g_skServer.send(strTeam.encode('utf-8'))       # チーム名を送信
        bytRecv = g_skServer.recv(4096)                # 先手後手を受信
        strRecv = bytRecv.decode('utf-8')              # 先手後手を受信
        if int(strRecv) == G_SENTE:                    # 先手なら
            g_ivPlay.set(G_SENTE)                      # 手番表示を先手で初期化
        else:                                          # 後手なら
            g_ivPlay.set(G_GOTE)                       # 手番表示を先手で初期化
            g_skServer.send('OK'.encode('utf-8'))      # 後手なら受信待ちの状態にするためOKを送信
    except:                                            # 例外が発生したら
        fncPrintLog(u'接続に失敗しました')             # エラーメッセージを記録
        return G_FALSE                                 # エラーを返す
    fncPrintLog('----- Conect Server -----')           # サーバ接続を記録
    return G_TURE                                      # 正常を返す

# ----------------------------------------------------------
# 取る石を送信する関数
#
#     引数：取る石の番号をカンマ区切で指定した文字列
#     戻値：正常(G_TRUE)もしくはエラー(G_FALSE)
# ----------------------------------------------------------
def fncSendStones(a_strTakeStone):
    try:                                                # 例外を監視
        g_skServer.send(a_strTakeStone.encode('utf-8')) # 取る石を送信
    except:                                             # 例外が発生したら
        fncPrintLog(u'送信に失敗しました')              # エラーメッセージを記録
        return G_FALSE                                  # エラーを返す
    return G_TURE                                       # 正常を返す

# ----------------------------------------------------------
# 取られた石を受信する関数
#
#     引数：なし
#     戻値：取られた石の番号をカンマ区切で指定した文字列
# ----------------------------------------------------------
def fncRecvStones():
    try:                                                # 例外を監視
        bytRecv = g_skServer.recv(4096)                 # 取られた石を受信
        strTakeStone = bytRecv.decode('utf-8')          # 取られた石を受信
    except:                                             # 例外が発生したら
        fncPrintLog(u'受信に失敗しました')              # エラーメッセージを記録
        return ''                                       # エラーを返す
    return strTakeStone                                 # 取られた石を返す

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
    
    if g_ivPlay.get() == G_GOTE:                # 先手が通信ならば
        strStones = fncRecvStones()             # 取られた石を受信
        fncTakeStones(strStones)                # 受信結果を初手に反映
    g_entInput.focus_set()                      # フォーカスの設定

# ----------------------------------------------------------
# Selectボタンのクリックイベント関数
#
#     引数：なし
#     戻値：なし
# ----------------------------------------------------------
def fncPushSelect() :
    g_ivTeban.set(G_SENTE)                          # 先手に初期化
    strMode = u'人 対 PC'                           # 表示対戦モードを人対PCに設定
    intMode = g_ivMode.get()                        # 対戦モードを取得
    if intMode == G_MANCOM:                         # 人対通信ならば
        if fncConectServer() == G_FALSE:            # サーバへ接続
            return                                  # 接続に失敗したらイベントを終了
        strMode = u'人 対 通信'                     # 表示対戦モードを人対通信に設定
        fncSetConectFrame()                         # メインFrameを通信モードで初期化
    elif intMode == G_PCCOM:                        # PC対通信ならば
        if fncConectServer() == G_FALSE:            # コネクション
            return                                  # コネクションに失敗したらイベントを終了
        strMode = u'PC 対 通信'                     # 表示対戦モードをPC対通信に設定
        fncSetConectFrame()                         # メインFrameを通信モードで初期化
        strStones = fncThinking()                   # 思考ロジックを呼び出し
        g_strInput,set(strStones)                   # 思考ロジックの初手を指し手入力へ設定
    g_frmStart.lower(g_frmMain)                     # 初期Frameを非表示
    fncPrintLog('----- Selected Mode --> '+strMode) # 対戦モード選択を記録
    g_winBase.title(u'石取りゲーム：'+strTeam)      # 画面タイトルへチーム名を追加

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
def fncPushStart() :
    g_rdbSente.configure(state='disabled')      # 先手を使用不可
    g_rdbGote.configure(state='disabled')       # 後手を使用不可
    g_btnStart.configure(state='disabled')      # Startボタンを使用不可
    g_entInput.configure(state='normal')        # 指し手入力を使用可能
    g_btnGet.configure(state='normal')          # Getボタンを使用可能
    g_ivTeban.set(G_SENTE)                      # 先手に初期化
    fncPrintLog('----- New Game Start -----')   # ログにゲーム開始を記録

    # プレーヤーが後手なら先手は思考ロジック
    if g_ivPlay.get() == G_GOTE:
        strStones = fncThinking()   # 思考ロジックを呼び出し
        fncTakeStones(strStones)    # 思考ロジックの初手を反映
    # フォーカスの設定
    g_entInput.focus_set()

# ----------------------------------------------------------
# Getボタンのクリックイベント関数
#
#     引数：なし
#     戻値：なし
# ----------------------------------------------------------
def fncPushGet():
    strInput = g_strInput.get()                     # 指定された石を取得
    if fncTakeStones(g_strInput.get()) == G_FALSE:  # 指定された石を取る
        return                                      # エラーが発生したら返す
    intMode = g_ivMode.get()                        # 対戦モードを取得
    if intMode == G_MANCOM:                         # 人対通信ならば
        fncSendStones(strInput)                     # 取る石を送信
        strStones = fncRecvStones()                 # 取られた石を受信
        fncTakeStones(strStones)                    # 受信結果を反映
        g_strInput.set('')                          # 正常終了なら石の指定をクリア
    elif intMode == G_PCCOM:                        # PC対通信ならば
        fncSendStones(strInput)                     # 取る石を送信
        strStones = fncRecvStones()                 # 取られた石を受信
        fncTakeStones(strStones)                    # 受信結果を反映
        strStones = fncThinking()                   # 思考ロジックを呼び出し
        g_strInput,set(strStones)                   # 思考ロジックを指し手入力へ設定
    else:                                           # 人対PCならば
        g_strInput.set('')                          # 石の指定をクリア
        strStones = fncThinking()                   # 思考ロジックを呼び出し
        fncTakeStones(strStones)                    # 思考ロジックの結果を反映

# ----------------------------------------------------------
# Resetボタンのクリックイベント関数
#
#     引数：なし
#     戻値：なし
# ----------------------------------------------------------
def fncPushReset():
    fncPrintLog('----- Game Reset -----')         # 初期化を記録
    fncResetStones()                              # 画面を初期化
    intMode = g_ivMode.get()                      # 対戦モードを取得
    if intMode == G_MANCOM or intMode == G_PCCOM: # 通信モードならば
        g_skServer.close()                        # 通信を切断
        fncPushSelect()                           # 通信を初期化
    else:                                         # 人対PCならば
        g_strInput.set('')                        # 石の指定をクリア
        g_rdbSente.configure(state='normal')      # 先手を使用可能
        g_rdbGote.configure(state='normal')       # 後手を使用可能
        g_btnStart.configure(state='normal')      # Startボタンを使用可能
        g_entInput.configure(state='disabled')    # 指し手入力を使用不可
        g_btnGet.configure(state='disabled')      # Getボタンを使用不可

# ----------------------------------------------------------
# Exitボタンのクリックイベント関数
#
#     引数：なし
#     戻値：なし
# ----------------------------------------------------------
def fncPushExit():
    fncPushReset()                                  # 画面を初期化
    intMode = g_ivMode.get()                        # 対戦モードを取得
    if intMode == G_MANCOM or intMode == G_PCCOM:   # 通信モードならば
        g_skServer.close()                          # 通信を切断
    g_frmStart.tkraise(g_frmMain)                   # 初期画面を表示
    fncPrintLog('----- Game Exit -----')            # 初期画面移行を記録

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
g_rdbSente.place(x=5+340, y=10)   # 先手を表示
g_rdbGote.place(x=70+340, y=10)   # 後手を表示
g_lblInput.place(x=10+340, y=60)  # 入力タイトルの表示
g_entInput.place(x=92+340, y=60)  # 入力エリアの表示
# --------------------------------------
g_btnStart.place(x=200+340, y=10) # Startボタンの表示
g_btnGet.place(x=10+340, y=100)    # Getボタンの表示
g_btnReset.place(x=105+340, y=100) # Resetボタンの表示
g_btnExit.place(x=200+340, y=100)  # Exitボタンの表示

# --------------------------------------
# メインループ開始
# --------------------------------------
tk.mainloop()

# 通信インターフェース
# 切断までソケットを維持
# 手番指定はアクティブ
# 通信ならリセットは使用不可
# 状態管理
# エラーハンドリング
