import os
from pydub import AudioSegment

from pydub.silence import detect_nonsilent
import pandas as pd

directory_to_check = "./" # Which directory do you want to start with?

def my_function(directory):
      # print("Listing: " + directory)
      return os.listdir(directory) # List current working directory

# Get all the subdirectories of directory_to_check recursively and store them in a list:
directories = [os.path.abspath(x[0]) for x in os.walk(directory_to_check)]
directories.remove(os.path.abspath(directory_to_check)) # If you don't want your main directory included

all_files = my_function(directory_to_check)      # Run your function
 
def match_target_amplitude(sound, target_dBFS):

	change_in_dBFS = target_dBFS - sound.dBFS

	return sound.apply_gain(change_in_dBFS)

count=0

# for i in all_files:
list2 = ['Sanskruti']
for i in list2:

	# if i=='Abinav':
	# 	continue
	# count=count+1
	# if count>3:
	# 	break
	# print(i)
	if os.path.isdir(i):
		# print(i)
		fol =".//" + i +"//Audio Record2"
		print(i)
		file_list = my_function(fol)
		print(file_list)

		audio_segment = AudioSegment.from_wav(".//" + i + ".//Audio Record2//"+ file_list[0])
		audio_segment2 = AudioSegment.from_wav(".//" + i + ".//Audio Record2//"+ file_list[1])
		normalized_sound = match_target_amplitude(audio_segment, -20.0)
		print("length of audio_segment={} seconds".format(len(normalized_sound)/1000))
		nonsilent_data = detect_nonsilent(normalized_sound, min_silence_len=5000, silence_thresh=-25, seek_step=1)
		# print("start,Stop")
		df = pd.DataFrame(columns=["start_time","stop_time"])
		prev, nex = 0,0
		list1 = []
		flg = 0
		for k, chunks in enumerate(nonsilent_data):
			# print( [chunk/1000 for chunk in chunks])
		    
			audio_chunk1=normalized_sound[chunks[0]:chunks[1]]
			audio_chunk1.export( fol+"//question_chunk{}.wav".format(k), format="wav")
			if flg==1:
				prev = chunks[0]
				df.loc[len(df)] = [nex, prev]
				list1.append((nex,prev))
			nex = chunks[1]
			flg=1
		df.loc[len(df)] = [nex,len(normalized_sound)]
		list1.append((nex,len(normalized_sound)))
		df.to_csv(fol+"timestamps.csv",header= False)
		normalized_sound2 = match_target_amplitude(audio_segment2, -20.0)
		print("length of audio_segment={} seconds".format(len(normalized_sound2)/1000))
		for  idx,t in enumerate(list1):
		    # print("split at [ {}:{}] ms".format(t[0],t[1]))
		    audio_chunk=normalized_sound2[t[0]:t[1]]
		    audio_chunk.export( fol+"//answer_chunk{}.wav".format(idx), format="wav")


		audio_segment = AudioSegment.from_wav(".//" + i + ".//Audio Record2//"+ file_list[2])
		audio_segment2 = AudioSegment.from_wav(".//" + i + ".//Audio Record2//"+ file_list[3])
		normalized_sound = match_target_amplitude(audio_segment, -20.0)
		print("length of audio_segment={} seconds".format(len(normalized_sound)/1000))
		nonsilent_data = detect_nonsilent(normalized_sound, min_silence_len=5000, silence_thresh=-25, seek_step=1)
		# print("start,Stop")
		df = pd.DataFrame(columns=["start_time","stop_time"])
		prev, nex = 0,0
		list1 = []
		flg = 0
		for k, chunks in enumerate(nonsilent_data):
			# print( [chunk/1000 for chunk in chunks])
		    
			audio_chunk1=normalized_sound[chunks[0]:chunks[1]]
			audio_chunk1.export( fol+"//question_chunk1_{}.wav".format(k), format="wav")
			if flg==1:
				prev = chunks[0]
				df.loc[len(df)] = [nex, prev]
				list1.append((nex,prev))
			nex = chunks[1]
			flg=1
		df.loc[len(df)] = [nex,len(normalized_sound)]
		list1.append((nex,len(normalized_sound)))
		df.to_csv(fol+"//timestamps1_.csv",header= False)
		normalized_sound2 = match_target_amplitude(audio_segment2, -20.0)
		print("length of audio_segment={} seconds".format(len(normalized_sound2)/1000))
		for  idx,t in enumerate(list1):
		    # print("split at [ {}:{}] ms".format(t[0],t[1]))
		    audio_chunk=normalized_sound2[t[0]:t[1]]
		    audio_chunk.export( fol+"//answer_chunk1_{}.wav".format(idx), format="wav")