import pandas as pd
fol = './/separate_text//'
files = ['4.csv', '7.csv','15.csv']
df1 = pd.read_csv(fol+files[0])
df2 = pd.read_csv(fol+files[1])
df3 = pd.read_csv(fol+files[2])

for j in range(len(df1)):	
	a = pd.DataFrame()
	a =a.append([""])
	a = a.append(["How did you keep yourself occupied during the pandemic?"])
	a = a.append(df1.iloc[j,4].split('.'))
	a = a.append(["Have you ever cheated in a rote learning based test before?"])
	a = a.append(df2.iloc[j,4].split('.'))
	a = a.append(["Which musical instruments do you play?"])
	a=a.append(df3.iloc[j,4].split('.'))
	a.rename(columns={0:'Transcript for each question'}, inplace=True)
	a['Mark Truth or Lie next to each statement. Mark N/A if neither'] = ""
	# print(a.head())
	a.to_csv(fol+'splits//'+str(df1.iloc[j,9])+'.csv', index=False)


