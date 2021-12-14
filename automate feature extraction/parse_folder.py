import os
import pandas as pd
import json

def my_function(directory):
      # print("Listing: " + directory)
      return os.listdir(directory) # List current working directory
directory_to_check = 'Transcriptions//ankittranscript'
# Get all the subdirectories of directory_to_check recursively and store them in a list:
directories = [os.path.abspath(x[0]) for x in os.walk(directory_to_check)]
directories.remove(os.path.abspath(directory_to_check)) # If you don't want your main directory included

df = pd.DataFrame()
colname= []
filename = []
all_files = my_function(directory_to_check)      # Run your function
for fol in all_files:
	fol2 = my_function(directory_to_check+'//'+fol)
	for i in fol2:
		if i!='audioall':
			if os.path.isdir(directory_to_check+'//'+fol+'//'+i):
				
				list2 = my_function(directory_to_check+'//'+fol+'//'+i)
				for k in list2:
					# print(i,k)
					with open('.//'+directory_to_check+'//' +fol+'//'+ i+'//'+ k,'r') as f:
						j = json.load(f) 
					zz = pd.json_normalize(j, record_path=['combinedRecognizedPhrases'], meta=['source', 'durationInTicks', 'duration'])
					colname.append(i)
					filename.append(k)
					# print(zz['itn'])
					df = df.append(zz)
		elif i=='audioall':
			list3=my_function(directory_to_check+'//'+fol+'//'+i)
			for i2 in list3:
				list2=my_function(directory_to_check+'//'+fol+'//'+i+'//'+i2)
				for k in list2:
					# print(i2,k)
					with open('.//'+directory_to_check+'//' +fol+'//'+ i+'//'+i2+'//'+ k,'r') as f:
						j = json.load(f) 
					zz = pd.json_normalize(j, record_path=['combinedRecognizedPhrases'], meta=['source', 'durationInTicks', 'duration'])
					# print(zz['itn'])
					colname.append(i2)
					filename.append(k)
					df= df.append(zz)			


df['name'] = colname
df['filename'] = filename
   

df.to_csv('ankit_final_transcripts3.csv')
# directory_to_check = "./Transcriptions" # Which directory do you want to start with?
