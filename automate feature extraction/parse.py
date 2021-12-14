import pandas as pd
import json
# with open('answer_chunk29.wav.json') as json_data:
#     data = json.load(json_data)
# ll =  pd.DataFrame(dict(list(data.items())[0:5]))
# print(ll)

with open('answer_chunk10.wav.json','r') as f:
    j = json.load(f)    
zz = pd.json_normalize(j, record_path=['combinedRecognizedPhrases'], meta=['source', 'durationInTicks', 'duration'])
zz.to_csv('transcript3.csv')