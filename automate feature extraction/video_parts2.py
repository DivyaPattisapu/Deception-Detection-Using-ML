import pandas as pd
import numpy as np
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import ast
from moviepy.editor import *
# required_video_file = "filename.mp4"
def vid_parts(person,required_video_file,starttime,endtime,target_file_number):
	starttime=starttime/1000
	endtime=endtime/1000
	ffmpeg_extract_subclip(required_video_file, starttime, endtime, targetname=person+'//Audio Record//'+target_file_number+".mp4")
	print('done',target_file_number)

def merge_parts(person,files,targetname):
	L=[]
	print(files)
	for file in files:
		video = VideoFileClip(file)
		L.append(video)
	final_clip2 = concatenate_videoclips(L)
	final_clip2.to_videofile(person+'//Audio Record//'+targetname+".mp4", fps=24, remove_temp=False)
 
 # Generate target video file
# final_clip.to_videofile("./target.mp4", fps=24, remove_temp=False)
df = pd.read_csv('transcripts_edited3.csv')

cols = df['name'].values
uni=list(np.unique(cols))

# print(len(uni))
# uni.remove('Vidya')
# uni.remove('Prakriti')
# uni.remove('Sanskruti')
print(uni)

k=0
for i in uni:
	# print(df[df['question']==i].count())
	# if i in ['Saloni','Abhinav', 'Aditya', 'Akshita', 'Amogh', 'Ankit', 'Apoorv', 'Harsh Khatri', 'Jovina', 'Kriti', 'Madhumita', 'Namya', 'Nandan', 'Nisha', 'Rajat Pramod', 'Rajat1', 'Rajat2', 'Rashmi', 'Ritik Bilala', 'Riya', 'Ronnie']:
	# 	k+question=1
	# 	continue	
	if i!= 'Sanskruti':
		continue
	k+=1	
	a=df[df['name']==i]
	try:
		df2 = pd.read_csv(i+'//timestamps3.csv', header=None)
	except:
		k+=1
		print('ALERT',i)
		continue	
	# print(df2.head())
	parts=[]
	for idx in range(len(df2)):
		# num= a.iloc[idx,7]
		# print(type(num))
		num=idx
		# # 
		# if num=='split' or num=='prev' or num=='':
		# 	print(i,'split')
		# elif '[' not in num :
			# print(i,int(num))
			# print(df2.iloc[int(num),1])
		# num=idx
		parts.append([df2.iloc[int(num),1],df2.iloc[int(num),2]])
		try:
			vid_parts(i,i+'//video.mp4',df2.iloc[int(num),1],df2.iloc[int(num),2],"chunk"+str(num))
		except:
			print('//video.mov',i)

		# else:
		# 	num = ast.literal_eval(num)
		# 	# print(type(num),num)

		# 	files=[]
		# 	for pts in num:
		# 		# print(i,pts,type(pts))
		# 		pts = idx
		# 		parts.append([df2.iloc[int(pts),1],df2.iloc[int(pts),2]])
		# 		try:
		# 			vid_parts(i,i+'//video.mp4',df2.iloc[int(pts),1],df2.iloc[int(pts),2],"chunk"+str(pts))
		# 		except:
		# 			print(i,pts)	
		# 		files.append(i+'//Audio Record//'+"chunk"+str(pts)+'.mp4')
			# try:
			# 	merge_parts(i,files,a.iloc[idx,5])
			# except:
			# 	print(i,a.iloc[idx,5])	
			# num
	print(i)		
print(parts)
				
