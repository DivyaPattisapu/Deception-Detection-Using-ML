import os
import pandas as pd
import json

def my_function(directory):
      # print("Listing: " + directory)
      return os.listdir(directory) # List current working directory
directory_to_check = 'Transcriptions//ankittranscript//c852bc4f-326a-4d56-9daf-7ef57a580f1e'
# Get all the subdirectories of directory_to_check recursively and store them in a list:
directories = [os.path.abspath(x[0]) for x in os.walk(directory_to_check)]
directories.remove(os.path.abspath(directory_to_check)) # If you don't want your main directory included

df = pd.DataFrame()
colname= []
filename = []
all_files = my_function(directory_to_check)      # Run your function
for fol in all_files:
	print(fol)
	if os.path.isdir(directory_to_check+'//'+fol):
		list2 = my_function(directory_to_check+'//'+fol)
		print(list2)
		for p in list2:
			list3 = my_function(directory_to_check+'//'+fol+'//'+p)
			for k in list3:
			# print(k)
				with open('.//'+directory_to_check+'//' +fol+'//'+p+'//'+ k,'r') as f:
					j = json.load(f) 
				zz = pd.json_normalize(j, record_path=['combinedRecognizedPhrases'], meta=['source', 'durationInTicks'])
				colname.append(p)
				filename.append(k)
				# print(zz['itn'])
				df = df.append(zz)
	# else:
	# 	k = fol
	# 		# print(k)
	# 			with open('.//'+directory_to_check+'//' + k,'r') as f:
	# 				j = json.load(f) 
	# 			zz = pd.json_normalize(j, record_path=['combinedRecognizedPhrases'], meta=['source', 'durationInTicks', 'duration'])
	# 			colname.append(p)
	# 			filename.append(k)
	# 			# print(zz['itn'])
	# 			df = df.append(zz)
			


df['name'] = colname
df['filename'] = filename
   

df.to_csv('ankit_transcripts.csv')
# directory_to_check = "./Transcriptions" # Which directory do you want to start with?
