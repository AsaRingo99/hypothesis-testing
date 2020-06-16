# -*- coding: utf-8 -*-
import os, tkinter, tkinter.filedialog, tkinter.messagebox
import tkinter.ttk as ttk
import pandas as pd
from scipy.stats import chi2_contingency
from scipy import stats
import numpy as np
import csv
import os

path = 0
def btn_click():
	# 選択候補を拡張子csvに絞る（絞らない場合は *.csv → *）
    global path
    filetype = [("", "*.csv")]
    dirpath = os.path.abspath(os.path.dirname(__file__))
	# 選択したファイルのパスを取得
    filepath = tkinter.filedialog.askopenfilename(filetypes = filetype, initialdir = dirpath)

	# 選択したファイル名を戻す
    path=str(filepath)
    
	
#メインウィンドウ	
a = tkinter.Tk()
a.geometry('300x370')
a.title('仮説検定アプリ')

#参照ボタン

frame_btn=tkinter.Frame(a,pady=1)
frame_btn.pack(fill='x')
label_btn=tkinter.Label(frame_btn,font=('',14),justify="center",text='ファイルを選択')
label_btn.pack()
btn = tkinter.Button(frame_btn, text='参照',command=btn_click, height=1,width=10)
print(path)
btn.pack()

#検定選択
frame_ken=tkinter.Frame(a,pady=1)
frame_ken.pack(fill='x')
label_ken=tkinter.Label(frame_ken,font=('',14),justify="center",text='検定手法')
label_ken.pack()
combo_ken = ttk.Combobox(frame_ken,font=("",14),justify="center",width=15,state='readyonly')
combo_ken['values']=("t検定","f検定","z検定",'カイ2乗検定')
combo_ken.pack()

#入力値欄(行)
frame_row=tkinter.Frame(a,pady=1)
frame_row.pack(fill='x')
label_row=tkinter.Label(frame_row,font=('',14),justify="center",text='スタートの行座標を入力してください')
label_row.pack()
entry_row = tkinter.Entry(frame_row,font=("",14),justify="center",width=15)
entry_row.pack()


#入力値欄(列)
frame_column=tkinter.Frame(a,pady=1)
frame_column.pack(fill='x')
label_column=tkinter.Label(frame_row,font=('',14),justify="center",text='スタートの列座標を入力してください')
label_column.pack()
entry_column = tkinter.Entry(frame_column,font=("",14),justify="center",width=15)
entry_column.pack()


#入力値欄(長さ)
frame_wid=tkinter.Frame(a,pady=1)
frame_wid.pack(fill='x')
label_wid=tkinter.Label(frame_wid,font=('',14),justify="center",text='データの長さを入力してください')
label_wid.pack()
entry_wid = tkinter.Entry(frame_wid,font=("",14),justify="center",width=15)
entry_wid.pack()




#path = btn_click()
#実行ボタン

def kentei():
	row=int(entry_row.get())
	column=int(entry_column.get())
	wid=int(entry_wid.get())
	p=0
	gyou=row-1
	retu=column-1
	nagasa=wid
	name=path
	if combo_ken.get()=='カイ2乗検定':  
    	#カイ二乗検定
		def kai(name,gyou,retu,nagasa) :
			f = open(name,"r")
			rd = csv.reader(f)
			ka = []
			Q = 0
			for i in rd :
				if Q < gyou or Q >= gyou + 2 :
					Q = Q + 1
					continue
				val = []
				for j in range(retu,retu+nagasa) :
					val.append(int(i[j]))
				ka.append(val)
				Q = Q + 1
			ka = np.array(ka).tolist()
			f.close()
			df = pd.DataFrame(ka)
			chi2, p, dof, expected = chi2_contingency(df, correction=False)
			return chi2,p,dof,expected    
		if p == 0 :
			chi2,p,dof,expected = kai(name,gyou,retu,nagasa)
			tkinter.messagebox.showinfo('カイ二乗検定結果','カイ二乗値:{}\np値:{}\n自由度:{}\n期待度数:{}'.format(chi2,p,dof,expected))
	elif combo_ken.get()=='t検定':
		def t(name,gyou=0,retu=0,nagasa=12) :
			f = open(name,"r")
			rd = csv.reader(f)
			ka = []
			Q = 0
			for i in rd :
				if Q < gyou or Q >= gyou + nagasa :
					Q = Q + 1
					continue
				val = []
				for j in range(retu,retu+2) :
					val.append(int(i[j]))
				ka.append(val)
				Q = Q + 1
			ka = np.array(ka).T.tolist()
			f.close()
			t, p = stats.ttest_ind(ka[0], ka[1])
			return t,p

		t,p = t(name,gyou,retu,nagasa)
		tkinter.messagebox.showinfo('t検定結果','t値:{}\np値:{}'.format(t,p))
	elif combo_ken.get()=='f検定':
		def FK(name,gyou=0,retu=0,nagasa=12) :
			f = open(name,"r")
			rd = csv.reader(f)
			ka = []
			Q = 0
			for i in rd :
				if Q < gyou or Q >= gyou + nagasa :
					Q = Q + 1
					continue
				val = []
				for j in range(retu,retu+2) :
					val.append(int(i[j]))
				ka.append(val)
				Q = Q + 1
			ka = np.array(ka).T.tolist()
			f.close()
			F = np.var(ka[1])/np.var(ka[0])
			df1 = len(ka[1]) - 1
			df2 = len(ka[0]) - 1
			p = stats.f.cdf(F, df1, df2)
			return F,p

		F,p = FK(name,nagasa=18)
		tkinter.messagebox.showinfo('t検定結果','f値:{}\np値:{}'.format(F,p))
	#elif combo_ken.get()=='t検定':

frame_ken=tkinter.Frame(a,pady=30)
frame_ken.pack(fill='x')

btn = tkinter.Button(frame_ken, text='実行',command=kentei, height=1,width=10)
btn.pack()


a.mainloop()