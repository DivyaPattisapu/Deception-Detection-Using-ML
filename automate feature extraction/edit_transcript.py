import pandas as pd


df = pd.read_csv('transcripts_draft1.csv')
# print(df.iloc[:,6].describe())
df2 = pd.DataFrame(columns=df.columns[[0,1,2,3,4,6,10,11,8]])
del_list={}
keep_list=[]
# df['duration'] = df['duration']
k=-1
for i in range(len(df)):
	if df.iloc[i,4]=='del':
		if del_list.get(df.iloc[i,11]):
			del_list[df.iloc[i,11]].append(df.iloc[i,10])
		else:
			del_list[df.iloc[i,11]]=[]
			del_list[df.iloc[i,11]].append(df.iloc[i,10])

	elif df.iloc[i,4]=='merge':
		df2.iloc[k,0]=str(str(df2.iloc[k,0])+str(df.iloc[i,0]))
		df2.iloc[k,1]=str(df2.iloc[k,1])+str(df.iloc[i,1])
		df2.iloc[k,2]=str(df2.iloc[k,2])+str(df.iloc[i,2])
		df2.iloc[k,3]=str(df2.iloc[k,3])+str(df.iloc[i,3])

		# print(df2.iloc[k,5],df.iloc[i,6])
		print(i,k)
		df2.iloc[k,5]=df2.iloc[k,5]+df.iloc[i,6]
		if isinstance(df2.iloc[k,6],list):
			df2.iloc[k,6].append(df.iloc[i,10])
		else:
			df2.iloc[k,6] = [int(df2.iloc[k,6]),int(df.iloc[i,10])]


	else:
		k=k+1
		keep_list.append(df.iloc[i,10])
		df2.loc[k,:] = df.loc[i,df.columns[[0,1,2,3,4,6,10,11,8]]]

		


		
df2.to_csv('transcripts_edited3.csv')