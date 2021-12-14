# from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
# import os
import pandas as pd
import numpy as np
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import ast
from moviepy.editor import *

def vid_parts(person,required_video_file,starttime,endtime,target_file_number):
	starttime=starttime/1000
	endtime=endtime/1000
	ffmpeg_extract_subclip(required_video_file, starttime, endtime, targetname=person+'//Audio Record//'+target_file_number+".mp4")
	print('done',target_file_number)

i='Vidya'
vid_parts(i,i+'//Audio Record//17.mp4',0,16000,"17_f")
vid_parts(i,i+'//Audio Record//17.mp4',16000,44000,"18")
# vid_parts(i,i+'//Audio Record//25.mp4',52000,77000,"27")

# ffmpeg_extract_subclip("video1.mp4", start_time, end_time, targetname="test.mp4")