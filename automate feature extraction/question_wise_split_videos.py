import pandas as pd
import numpy as np
import os
import shutil

df = pd.read_csv('transcripts_edited3.csv')

cols = df['question'].values

# print(type(cols))
uni=list(np.unique(cols))



list1=[]
for i in uni:
	if df[df['question']==i]['question'].count()<30:
		list1.append(i)

# print(list1)
cols2=df['id'].values
# print(cols2)
listid=set(np.unique(cols2))
# for i in list1:
# 	# print(df[df['question']==i].count())
# 	a=set(df[df['question']+'.wav'==i].loc[:,'id'])
# 	# print(a)
# 	print(i,listid-a)
# 	# print(i,a)

	# for j in uni:
	# 	if (df[df['id'==i]]['question']).count()==0:
	# 		print(i,j)
os.mkdir('.//separate_videos')
for i in uni:
	# print(df[df['question']==i].count())
	a=df[df['question']==i]
	# print(a.head())

	path ='.//separate_videos//'+i
	os.mkdir(path)
	for j in range(len(a)):
		# print(j)
		# print(a['id'])
		fol = a['name'].iloc[j]
		if fol=='Prakriti' or fol=='Sanskruti':
			continue
		
		id_num = a['id'].iloc[j]
		print(fol,id_num)

		# if not id_num:
		# 	print(i,fol,id)
		path_to_file = './/'+fol+'//Audio Record//'+i+'.mp4'
		path_rename ='.//separate_videos//'+i+'//id'+str(int(id_num))+'.mp4'
		# print(path_to_fisle,path)
		# if i==str(id_num):
		# 	print("HIYAA")
		shutil.copy(path_to_file,path)
		os.rename(path+'//'+i+'.mp4',path_rename)
	# a.drop('question')
	# a.to_csv(+'.csv',index=False)

