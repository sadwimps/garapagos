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
G_GOTE = 1            # 後手

G_MANPC = 0           # 人対PCモード
G_MANCOM = 1          # 人対通信モード
G_PCCOM = 2           # PC対通信モード

# ------------------------------------------------------------------------------------------------------------------------------------------------------
# 定数宣言 開発用※開発終了したら削除(上のコメント化も戻す)
# ------------------------------------------------------------------------------------------------------------------------------------------------------
G_MAXSTONE = 35       # 石の最大数
G_ROW = 5            # 石を並べる行数
G_COL = 7            # 石を並べる列数

#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------
# モジュールimport
# --------------------------------------
import tkinter as tk  # GUIモジュール
import random  as rd  # 乱数モジュール
import datetime as dt # 日付モジュール
import socket as sk   # ソケットモジュール

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
# ------------------------------------------------------------------------------------------------------------------------------------------------------
# 思考ロジック関数（ここを作り込む！）
#
#     引数：なし
#     戻値：取る石の番号をカンマ区切で指定した文字列
# ------------------------------------------------------------------------------------------------------------------------------------------------------
def fncThinking():
    # ☆☆石の状態を保存するグローバル変数は自由に設定可とする
    # ☆☆その場合は「石の準備」、fncResetStones()、fncPickupStone()での操作を忘れずに！
    # ☆☆「取る石の番号をカンマ区切で指定した文字列」が戻値
    takePairNum = '1'
    l_liveStone = list(g_lstLiveStone)
# --石のペアの生成はここでやります！------------------

    g_lstLiveStone4 = list(fncAllForOne(g_lstLiveStone,'4'))
    g_lstLiveStone3 = list(fncAllForOne(g_lstLiveStone,'3'))
    g_lstLiveStone2 = list(fncAllForOne(g_lstLiveStone,'2'))

# --関数のエラーチェックはここでやります！------------------

#    if fncCheckEnd(g_lstLiveStone2) < 0:
#        fncPrintLog('「fncCheckEnd」で何か起きてるよ！')

#    if len(fncFirstGet(g_lstLiveStone,g_lstLiveStone4,g_lstLiveStone3,g_lstLiveStone2)) == 0:
#        fncPrintLog('「fncFirstGet」で何か起きてるよ！')

# --ペア作成後に使う定数の初期化はここでやります！------------------
    zanNum2 = len(g_lstLiveStone2)     # 残存石のペア2の数を取得
    zanNum3 = len(g_lstLiveStone3)     # 残存石のペア3の数を取得
    zanNum4 = len(g_lstLiveStone4)     # 残存石のペア4の数を取得
    TakeStoneList = ['00']             # 実際に取得するペアのリスト
    CheckStoneList = []                #はじめの方で取得していく石のリスト

# 序盤から中盤------------------------------------------------------
    # まずは真ん中からズバット--------------------------------------
    if len(g_lstLiveStone) > 20:
        CheckStoneList=['03','10','14','15','16','17','18','19','20','24','31']
        TakeStoneList = fncFirstGet(CheckStoneList,fncAllForOne(g_lstLiveStone,'432'))

        if len(TakeStoneList) > 1:
            return fncGetStoneStr(TakeStoneList)

    # 続いて--------------------------------------
    if len(g_lstLiveStone) > 12:
        CheckStoneList=['04','05','06','11','12','13','25','26','27','32','33','34']
        TakeStoneList = fncFirstGet(CheckStoneList,fncAllForOne(g_lstLiveStone,'432'))

        if len(TakeStoneList) > 1:
            return fncGetStoneStr(TakeStoneList)

# 考え始めるよ------------------------------------------------------
    loop = 0
    if len(l_liveStone) > 10:
        loop = 2
        takePairNum = '43'

    elif len(l_liveStone) < 11:
        loop = 4
        takePairNum = '321'

    elif zanNum4 < 2 and  zanNum3 < 2:
        loop = 3
        takePairNum = '431'

    TakeStoneList = fncCheckEnd(loop,l_liveStone,1,takePairNum)

    if TakeStoneList[0] > 0:
        i = rd.randint(1,len(TakeStoneList)-1)
        return fncGetStoneStr(TakeStoneList[i])

    # ここからは取り損ねた時用---------------------------------------
    if TakeStoneList[0] < 1:
        if zanNum4 > 0:
            go4 = rd.randint(0,zanNum4-1)       # 残存石のインデックスをランダムに生成
            TakeStoneList = g_lstLiveStone4[go4]
        elif zanNum3 > 0:
            go3 = rd.randint(0,zanNum3-1)       # 残存石のインデックスをランダムに生成
            TakeStoneList = g_lstLiveStone3[go3]
        elif zanNum2 > 0:
            go2 = rd.randint(0,zanNum2-1)       # 残存石のインデックスをランダムに生成
            TakeStoneList = g_lstLiveStone2[go2]
        else:
            go1 = rd.randint(0,len(g_lstLiveStone)-1)  # 残存石のインデックスをランダムに生成
            TakeStoneList = g_lstLiveStone[go1]

    return fncGetStoneStr(TakeStoneList)


# 実際の石の取得-----------------------------------------------------
def fncGetStoneStr(TakeStoneList):
    TakeStoneString = ''               # 実際に取得するのペアの文字列

    for i in range(len(TakeStoneList)):
        TakeStoneString=TakeStoneString+TakeStoneList[i]
        if i < len(TakeStoneList)-1 :
            TakeStoneString = TakeStoneString + ','

    return TakeStoneString


# -------------------------------------------------------------------
#実際に選択するときの思考を関数化したよ！
#■slectPairfncごとの思考
#　1:勝てるペアの多い組み合わせの方を選択
#　2:指定リストを含むもっとも多いものを選択
#
# -------------------------------------------------------------------
def fncSlectPair(slectPairfnc,rtnEndList):
    rtnSlectPair = [] #リターン用配列

    if slectPairfnc == 1:
        rtnSlectPair = rtnEndList[0]
        for chkPair in rtnEndList:
            if rtnSlectPair[0] < chkPair[0]:
                rtnSlectPair = chkPair
        return rtnSlectPair

    elif slectPairfnc == 4:
        for chkPair in rtnEndList:
            if rtnSlectPair[0] > chkPair[0]:
                rtnSlectPair = chkPair
    #まぁ、100は削るよね。。。
        if rtnSlectPair[0] == 100:
            rtnSlectPair[0] = -100
            return rtnSlectPair

        return rtnSlectPair

    #1番4番が選択されてなければとりあえず1番目を返すよーーー
    else:
        return rtnEndList[0]

# -------------------------------------------------------------------
# その番で勝てるペアの数とペアの組み合わせを返すよ！
# 勝ち確定の時は100が頭に入るからね！
# 勝ちパターンが無い場合は数が[0,[]]のリストを返すからね！
# (例)：01,02,03のときの値は[2,['01','02'],['02','03']]
# -------------------------------------------------------------------
def fncCheckEndOne(chkEndList,selectPairNum):
    rtnEndList = [0]
    l_chkEndList = []
    #その組み合わせがが残りの石から無くなったら残りの石が1個になるリストを作成
    chkOneList = fncAllForOne(chkEndList,selectPairNum)
    for chk in chkOneList:
        l_chkEndList = list(chkEndList)

        for chk2 in chk:
            l_chkEndList.remove(chk2)
        if fncAllForOne(l_chkEndList,'4') == 0 and fncAllForOne(l_chkEndList,'3') == 0 and fncAllForOne(l_chkEndList,'2') == 0:
            if len(l_chkEndList) > 1:
                if len(l_chkEndList) % 2 == 1:
                    rtnEndList.append(chk)

    #勝ち確定のパターンがあればパターンとパターンの個数をリターン
    rtnEndList[0] = len(rtnEndList) - 1
    if rtnEndList[0] == 0:
       rtnEndList.append([])

    return rtnEndList


# -------------------------------------------------------------------
# 自手を含めた「loopNum」ターン以内に詰めとなる(残り個数が1つになる)
# 組み合わせのリストを作成するよ！
# 絶対に勝てる訳じゃない場合は「slectPairfnc」で優先したものを返すよ！
# 勝ち確定の時は100が頭に入るからね！
#■slectPairfncごとの思考
#　1:勝てるペアの多い組み合わせを方を選択
#　2:指定リストを含むもっとも多いものを選択
#
#  100:相手番での勝ち確定を排除するロジック
#
# -------------------------------------------------------------------
def fncCheckEnd(loopNum,chkEndList,slectPairfnc,selectPairNum):
    rtnEndList = [0,[]]        #return用のリスト
    rtnEndListMid = []         #判定用の中間リスト
    chkListWork = []           #ループ中のWorkリスト
    chkListWorkMid = []        #ループ中のWorkリスト
    chkPairList = fncAllForOne(chkEndList,selectPairNum)
    l_chkEndList = []
    l_LoopNum = 0

#呼び出しエラーの回避------------------------------------------------
    #ループ回数が0で呼び出されたら終了
    if loopNum < 1 or len(chkEndList) < 2:
        del rtnEndList[1]
        rtnEndList.append(chkEndList)
        return rtnEndList
#--------------------------------------------------------------------
    #今回の手で勝てるかどうかの結果を格納
    checkLoopOne = fncCheckEndOne(chkEndList,selectPairNum)
    #今回のループ回数が1の時はそのまま返すし、
    #現段階で勝ち確定の手があればその先は見ない
    if checkLoopOne[0] > 0 or loopNum == 1:
        return checkLoopOne

    #ループが2以上の時は相手の手番で取れるパターン毎に評価
    #自手の全パターンに対して次の相手のパターンを評価
    #まずは相手の手番で取れるリストの準備
    loopNum -= 1
    #自分の取れるパターン毎に評価するよ

    for chk in chkPairList:
        l_chkEndList = list(chkEndList)
        del chkListWorkMid[:]
        #相手パターンを準備
        for chkMe in chk:
            l_chkEndList.remove(chkMe)

        #空っぽじゃなければ相手番の状態を取得しとこうかな～
        #相手番で回すよ～
        if len(l_chkEndList) > 0:
            chkPairListYou = fncAllForOne(l_chkEndList,selectPairNum)
            for chk2 in chkPairListYou:
                l_chkEndListYou = list(l_chkEndList)
                for chkYou in chk2:
                    l_chkEndListYou.remove(chkYou)
                if len(l_chkEndListYou) > 0:
                    chkEndListWork = list(fncCheckEnd(loopNum,l_chkEndListYou,slectPairfnc,selectPairNum))
                    if chkEndListWork[0] > 0:
                        chkListWorkMid.append(chkEndListWork[0])

            if len(chkListWorkMid) == 0:
                chkListWorkMid.append(0)

            #ただし、相手番で勝ち確定ならそれは除こう。

            if fncCheckEnd(loopNum,l_chkEndList,slectPairfnc,selectPairNum)[0] == 100:
                chkListWorkMid[0] = -100
                chkListWork.append(-100)

            #勝ち確定したらばその手を選択。後ろは振り返らない。
            if len(chkPairListYou) == len(chkListWorkMid):
                return [100,chk]

        if len(chkListWorkMid) == 0:
            chkListWorkMid.append(0)

        #勝ち手があればその手を選択
        if 0 < chkListWorkMid[0] and chkListWorkMid[0] < 99:
            chkEndListMid = fncSlectPair(loopNum,chkListWorkMid,slectPairfnc)
            midChk = chkEndListMid[0]
            chkListWork.append(midChk)

        rtnEndListMid.append(chk)

    #ここからが評価するとこっ！頑張るとこっ！
    if len(chkListWork) > 1:
        if len(rtnEndListMid) == 0:
           rtnEndListMid.appned(0)
        chkEndListMid = fncSlectPair(loopNum,chkListWork,slectPairfnc)
        rtnChk = chkEndListMid[0]
        del chkEndListMid[0]
        rtnEndList[0] = rtnChk
        del rtnEndList[1]
        loopNumEnd = 0
        for chk3 in chkEndListMid:
            if chk3 == 1:
               rtnEndList.append(rtnEndListMid[loopNumEnd])
            loopNumEnd += 1

    return rtnEndList

# -------------------------------------------------------------------
# 取得する全パターンを一つのリストにするよ
# -------------------------------------------------------------------
def fncAllForOne(l_lstLiveStone,selectPairNum):
    chkListAll = []
    if '4' in selectPairNum:
        chkListAll.extend(fncGeneratePair(4,l_lstLiveStone,[]))
    if '3' in selectPairNum:
        chkListAll.extend(fncGeneratePair(3,l_lstLiveStone,[]))
    if '2' in selectPairNum:
        chkListAll.extend(fncGeneratePair(2,l_lstLiveStone,[]))
    if '1' in selectPairNum:
        chkListAll.extend(fncGeneratePair(1,l_lstLiveStone,[]))
    if len(chkListAll) == 0:
        chkListAll.extend([])

    return chkListAll

# -------------------------------------------------------------------
# 連続する「pairNum」個の組の組み合わせ配列を作成しますよ！
# -------------------------------------------------------------------
def fncGeneratePair(pairNum,inListLiveStone,inChkListStone):
    #呼び出しエラーの回避--------------------------------
    #引数が無効な状態で呼び出されたら終了
    if len(inListLiveStone) < pairNum:
        return []
    elif pairNum < 1:
        return []
    #--------------------------------------------------------------------
    rtn_lstLiveStone = []    # 残存石のペア配列を初期化
    l_lstLiveStone = list(inListLiveStone)  # 残存石を処理用に格納
    l_lstchkLiveStone = list(l_lstLiveStone)
    l_ChkListStone = []

    #pairNumが0になるまでは準備を続ける！
    for i in l_lstLiveStone:
        l_ChkListStone.extend(inChkListStone)
        l_ChkListStone.append(i)
        if  pairNum == 1:
            rtn_chkLiveStone = list(l_ChkListStone)
            if fncCheckStones(rtn_chkLiveStone) == G_TURE:
                rtn_lstLiveStone.append(rtn_chkLiveStone)
        elif pairNum > 1 and len(l_lstchkLiveStone) > pairNum - 1:
            l_lstchkLiveStone.remove(i)
            outPairNum = pairNum - 1
            rtn_fnlstLiveStone = fncGeneratePair(outPairNum,l_lstchkLiveStone,l_ChkListStone)
            rtn_lstLiveStone.extend(rtn_fnlstLiveStone)
        del l_ChkListStone[:]
    return rtn_lstLiveStone


# -------------------------------------------------------------------
#実際に選択するときの思考を関数化したよ！
#■slectPairfncごとの思考⇒勝てるパターンを1つだけ返す
#　1:勝てるペアの多い組み合わせの方を選択
#　
#
#  4:相手番での勝ち確定を排除するロジック
#
# -------------------------------------------------------------------
def fncSlectPair(loopNum,rtnEndList,slectPairfnc):
    rtnSlectPair = [0 for i in range(len(rtnEndList)+1)]#リターン用配列
    l_rtnSlectPair = [0 for i in range(len(rtnEndList)+1)]#リターン用配列の初期化用
    l_loopNum = 0
    pairStatus = 0
#呼び出しエラーの回避------------------------------------------------
    #Loopが一回で評価が回ってきたときは、「4」の時以外はそのまま返す
#--------------------------------------------------------------------

    if slectPairfnc == 1:
        l_loopNum = 1
        l_chkPair = rtnEndList[0]
        for chkPair in rtnEndList:
            if l_chkPair < chkPair:
                rtnSlectPair = list(l_rtnSlectPair)
                rtnSlectPair[0] = chkPair
                rtnSlectPair[l_loopNum] = 1
                l_chkPair = chkPair
            elif l_chkPair == chkPair:
                rtnSlectPair[l_loopNum] = 1
            pairStatus = l_chkPair
            l_loopNum += 1
        rtnSlectPair[0] = pairStatus
        return rtnSlectPair

    elif slectPairfnc == 4:
        for chkPair in rtnEndList:
            if chkPair[0] == 10:
                del chkPair[0]
                rtnSlectPair.append(chkPair)
        return rtnSlectPair

    #1番4番が選択されてなければとりあえず1番目を返すよーーー
    else:
        return rtnEndList[0]

# -------------------------------------------------------------------
# 指定した範囲を含むペアに対して含む個数と配列の組を返しますよ！
# -------------------------------------------------------------------

def fncFirstGet(CheckStoneList,chkListPair):

    rtn = ['']

    if len(chkListPair) == 0 or len(CheckStoneList) == 0:
        return rtn

    for taget_pair in chkListPair:
        flg = 0

        for i in range(len(taget_pair)):
            if taget_pair[i] in CheckStoneList:
                flg += 1
            if flg == len(taget_pair):
                return taget_pair

    return rtn
#--------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------
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

#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------

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
    strTeam = g_strTeam.get()                          # チーム名を取得
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
