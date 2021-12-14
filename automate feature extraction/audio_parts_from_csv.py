from pydub import AudioSegment
import pandas as pd

# audio_segment = AudioSegment.from_wav()



def match_target_amplitude(sound, target_dBFS):

	change_in_dBFS = target_dBFS - sound.dBFS

	return sound.apply_gain(change_in_dBFS)
# normalized_sound = match_target_amplitude(audio_segment, -20.0)

fol = './/Saloni//Audio Record2//'


audio_segment = AudioSegment.from_wav(fol+'//'+)

normalized_sound = match_target_amplitude(audio_segment, -20.0)
print("length of audio_segment={} seconds".format(len(normalized_sound)/1000))
# nonsilent_data = detect_nonsilent(normalized_sound, min_silence_len=5000, silence_thresh=-25, seek_step=1)
df = pd.read_csv('Audio Record2timestamps.csv', header=None)
new_zero = df.iloc[42,1]

for k in range(42,59):
	# print( [chunk/1000 for chunk in chunks])
    # 
	audio_chunk=normalized_sound[df.iloc[k,1]-new_zero:df.iloc[k,2]-new_zero]
	audio_chunk.export( fol+"//answer_chunk{}.wav".format(k-1), format="wav")
		