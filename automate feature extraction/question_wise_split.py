import pandas as pd
import numpy as np

df = pd.read_csv('transcripts_edited.csv')

cols = df['question'].values

# print(type(cols))
uni=list(np.unique(cols))



list1=[]
for i in uni:
	if df[df['question']==i]['question'].count()<30:
		list1.append(i)

# print(list1)
listid=set(np.unique(df['id'].values))
# for i in list1:
# 	# print(df[df['question']==i].count())
# 	a=set(df[df['question']==i].loc[:,'id'])
# 	print(i,listid-a)
# 	print(i,a)

# 	for j in uni:
# 		if (df[df['id'==i]]['question']).count()==0:
# 			print(i,j)

for i in uni:
	# print(df[df['question']==i].count())
	a=df[df['question']==i]
	# print(a.head())

	# a.drop('question')
	a.to_csv('.//separate_questions//'+i+'.csv',index=False)