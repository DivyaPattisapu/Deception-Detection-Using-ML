from pydub import AudioSegment, silence
import pandas as pd
# audio_segment = AudioSegment.from_wav()



def match_target_amplitude(sound, target_dBFS):

	change_in_dBFS = target_dBFS - sound.dBFS

	return sound.apply_gain(change_in_dBFS)
# normalized_sound = match_target_amplitude(audio_segment, -20.0)

fol = './/Sanskruti//Audio Record2'
# df=pd.read_csv(fol+"//timestamps1_.csv",header= None)
		
		
# for  idx in range(len(df)):
# 	# print("split at [ {}:{}] ms".format(t[0],t[1]))
# 	# print(df[df.columns[3]].loc(idx).value)
# 	a = df.loc[idx,3]
# 	print(a)
# 	if df.loc[idx,3]<0:
# 		continue
# 	audio_chunk=normalized_sound[df.loc[idx,3]:df.loc[idx,4]]
# 	audio_chunk.export( fol+"//new_chunks"+"//answer_chunk1_{}.wav".format(idx), format="wav")



audio_segment = AudioSegment.from_wav(fol+'//'+)

normalized_sound = match_target_amplitude(audio_segment, -20.0)
print("length of audio_segment={} seconds".format(len(normalized_sound)/1000))
nonsilent_data = detect_nonsilent(normalized_sound, min_silence_len=5000, silence_thresh=-25, seek_step=1)
for k, chunks in enumerate(nonsilent_data):
	# print( [chunk/1000 for chunk in chunks])
    # 
	audio_chunk=normalized_sound[500+chunks[0]:500+chunks[1]]
	audio_chunk.export( fol+"//answer_chunk{}.wav".format(k), format="wav")
		