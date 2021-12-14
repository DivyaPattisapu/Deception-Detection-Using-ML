from pydub import AudioSegment

from pydub.silence import detect_nonsilent
import pandas as pd
#adjust target amplitude

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-a', nargs='?', default="check_string_for_empty")
parser.add_argument('-b', nargs='?', default="check_string_for_empty")
parser.add_argument('-f', nargs='?', default="check_string_for_empty")
# parser.add_argument("a")
args = parser.parse_args()


def match_target_amplitude(sound, target_dBFS):

	change_in_dBFS = target_dBFS - sound.dBFS

	return sound.apply_gain(change_in_dBFS)

#Convert wav to audio_segment

audio_segment = AudioSegment.from_wav(args.a)
audio_segment2 = AudioSegment.from_wav(args.b)

#normalize audio_segment to -20dBFS

normalized_sound = match_target_amplitude(audio_segment, -20.0)

print("length of audio_segment={} seconds".format(len(normalized_sound)/1000))

#Print detected non-silent chunks, which in our case would be spoken words.

nonsilent_data = detect_nonsilent(normalized_sound, min_silence_len=5000, silence_thresh=-25, seek_step=1)

#convert ms to seconds

print("start,Stop")
df = pd.DataFrame(columns=["start_time","stop_time"])
prev, nex = 0,0
list1 = []
flg = 0
for i, chunks in enumerate(nonsilent_data):
	print( [chunk/1000 for chunk in chunks])
    
	audio_chunk1=normalized_sound[chunks[0]:chunks[1]]
	audio_chunk1.export( ".//"+args.f+"//Interviewer//"+"question_chunk{}.wav".format(i), format="wav")
	if flg==1:
		prev = chunks[0]
		df.loc[len(df)] = [nex, prev]
		list1.append((nex,prev))
	nex = chunks[1]
	flg=1
df.loc[len(df)] = [nex,len(normalized_sound)]
list1.append((nex,len(normalized_sound)))
df.to_csv(args.f+"timestamps.csv",header= False)
print(list1)




# list1= [(515, 9807), (12392, 104550), (107653, 180135), (181090, 199881), (202760, 280087), (283642, 345833), (348144, 426668), (431105, 505443), (511114, 558509), (564396, 649699), (655117, 708059), (708722, 797375), (807254, 876296), (878176, 878176)]
normalized_sound2 = match_target_amplitude(audio_segment2, -20.0)


print("length of audio_segment={} seconds".format(len(normalized_sound2)/1000))

#Print detected non-silent chunks, which in our case would be spoken words.

# nonsilent_data = detect_nonsilent(normalized_sound, min_silence_len=5000, silence_thresh=-25, seek_step=1)


# list_of_timestamps = [ 10, 20, 30, 40, 50 ,60, 70, 80, 90 ] #and so on in *seconds*

# start = ""
for  idx,t in enumerate(list1):
    #break loop if at last element of list
    # if idx == len(list_of_timestamps):
    #     break

    # end = t * 1000 #pydub works in millisec
    print("split at [ {}:{}] ms".format(t[0],t[1]))
    audio_chunk=normalized_sound2[t[0]:t[1]]
    audio_chunk.export( ".//"+args.f+"answer_chunk{}.wav".format(idx), format="wav")

    # start = end * 1000 #pydub works in millisec


