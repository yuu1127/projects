# coding: utf-8

import numpy as np
from gensim.models import word2vec
from janome.tokenizer import Tokenizer
model = word2vec.Word2Vec.load("wikimodel.txt")
to = Tokenizer()
sim = ""
global cnt
#A,Bの会話数cnt
cnt   = 0
listA = 0
listB = 0
limitA,limitB,limitC = 0,0,0
shikiA,shikiB,shikiC = 0,0,0

def worddivide(listA,Kaiwa):

	tokensA = to.tokenize(Kaiwa)
	SpilitA = []
	for token in tokensA:
		SpilitB = token.part_of_speech.split(',')[0]
		A = token.surface
		if SpilitB == '助詞' or SpilitB == '助動詞' or SpilitB == '記号' or SpilitB == '接頭詞':
			continue
		SpilitA.append(A)
		
	if(cnt == 0):
		listA = [SpilitA]
	else:
		listA.append(SpilitA)
		
	return listA
	

def pastsim(list):
	#関数の中のものは必ず初期化
	print("pastsimが呼ばれました")
	shiki = 0
	limit = 0
	for u in range(cnt-2):
															#u番目の文章の何単語目か
		for t in range(len(list[u])):
															#比較する
			for r in range(1,cnt-1):
			
				for s in range(len(list[r])):
				
						tangoA = list[u][t]
						tangoB = list[r][s]
						out = model.similarity(tangoA,tangoB)
						shiki += 1
						if out < 0.5:
							print(tangoA, tangoB)
							limit += 1
	return (shiki,limit)

def absim(listA, listB):
	#AとBの類似度計算
	print("absimが呼ばれました")
	abshiki = 0
	ablimit = 0
	for m in range(cnt):
	
		for n in range(len(listA[m])):
		
			for p in range(cnt):
			
				for q in range(len(listB[p])):
				
					tangoC = listA[m][n]
					tcngoD = listB[p][q]
					about = model.similarity(tangoC, tcngoD)
					abshiki += 1
					if about < 0.5:
						print(tangoC, tcngoD)
						ablimit += 1
	return (abshiki, ablimit)
			
		
print("m:こんにちは!")

while True :
	#Aさん、Bさんの会話から話の区切りをみつける、話の流れを見る
	#会話をみて、会話4つ分ぐらいで区切りつける？
	#単語が学習に入ってないならそれはカウントしない

	#ここでmecabを使って文章を単語に分割
	#助詞、助動詞だけ外す

	KaiwaA  = input("あなた:")
	listA   = worddivide(listA,KaiwaA)
	KaiwaB  = input("m:")
	listB   = worddivide(listB,KaiwaB)
													#文章の回数inputの回数
	cnt += 1		
	
	print(listA)
	print(listB)
	#もしその単語がword2vecでうまく取れていないようならスキップか何か0とか値をあてる
	#二重配列でa[会話の回数][会話の単語数]要素ごと繰り返す
	#とりあえず二文で
	#cntで合わせたらひとつ前の会話文と対比できない
	
	
	if(cnt >= 2):		
		#A君の類似度計算
		shikiA,limitA = pastsim(listA)
		#B君の類似度計算
		shikiB,limitB = pastsim(listB)
		
	#A君,B君の類似度計算
	shikiC,limitC = absim(listA,listB)
		
	limit  = limitA + limitB + limitC
	shikii = shikiA + shikiB + shikiC
	#forループで使う変数は残らねえ!
	if limit > shikii/2:
		print("m:流れ変りましたね…!")
		break
	
print("m:ばいばーい")



