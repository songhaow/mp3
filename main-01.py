"""10-10-2018 This module is a script that processes mp3 songs in a directory to find bpm / beats, etc
"""
#! /usr/bin/env python
import boto3
import botocore
import sys, os
import typing
import json
from aubio import source, tempo
from numpy import median, diff

DATA_FOLDER = 'data'

# ---------------------------------------
def get_all_song_keys():
    all_song_keys = []
    allfiles=os.listdir(DATA_FOLDER) # need undstand path better such as: /songhaow-test-123/
    print ("allfiles: ", allfiles)

    for filename in allfiles:
        name=filename.split(".")[0]
        sufname=filename.split(".")[1]
        if(sufname=="mp3"):
          thismp3=name+".mp3"
          all_song_keys.append(thismp3)

    return all_song_keys
# -----------------------------------------
def calculate_song_bpm(path: str, params: typing.Dict=None):
    path = f'{DATA_FOLDER}/{path}'

    if params is None:
        params = {}
    # default:
    samplerate, win_s, hop_s = 44100, 1024, 512
    if 'mode' in params:
        if params.mode in ['super-fast']:
            # super fast
            samplerate, win_s, hop_s = 4000, 128, 64
        elif params.mode in ['fast']:
            # fast
            samplerate, win_s, hop_s = 8000, 512, 128
        elif params.mode in ['default']:
            pass
        else:
            print("unknown mode {:s}".format(params.mode))
    # manual settings
    if 'samplerate' in params:
        samplerate = params.samplerate
    if 'win_s' in params:
        win_s = params.win_s
    if 'hop_s' in params:
        hop_s = params.hop_s

    s = source(path, samplerate, hop_s)
    samplerate = s.samplerate
    o = tempo("specdiff", win_s, hop_s, samplerate)
    # List of beats, in samples
    beats = []
    # Total number of frames read
    total_frames = 0

    while True:
        samples, read = s()
        is_beat = o(samples)
        if is_beat:
          this_beat = o.get_last_s()
          beats.append(this_beat)
        #if o.get_confidence() > .2 and len(beats) > 2.: #  break
        total_frames += read
        if read < hop_s: break

    def beats_to_bpm(beats, path):
        if len(beats) > 1:
            if len(beats) < 4:
                print("few beats found in {:s}".format(path))
            bpms = 60./diff(beats) #bpm is an array
            medinbpm=median(bpms)  #medinbpm is a float number
            return medinbpm #needs to be understood
        else:
            print("not enough beats found in {:s}".format(path))
            return 0

    # print "beats-in-bpm: ", beats
    return beats_to_bpm(beats, path)

# ///////////////////////////////////////
def calculate_song_beats(path: str):
  path = f'{DATA_FOLDER}/{path}'
  win_s = 512                 # fft size
  hop_s = win_s // 2          # hop size
  filename=path
  samplerate = 0
  total_frames = 0
  s = source(filename, samplerate, hop_s)
  samplerate = s.samplerate
  o = tempo("default", win_s, hop_s, samplerate)
  delay = 4. * hop_s

# list of beats
  beats = []
  beats01=[]

  while True:
      samples, read = s()
      is_beat = o(samples)
      if is_beat:
        this_beat = int(total_frames - delay + is_beat[0] * hop_s)
        beats.append(this_beat)
        beats01.append(this_beat / float(samplerate))
      total_frames += read
      if read < hop_s: break

  return beats01

# -----------------------------------------------------
def process_songs():

  s3 = boto3.resource('s3')
  s3_client = boto3.client('s3')

  #download all files from AWS S3 into local directory
  BUCKET_NAME='songhaow-test'
  response01=s3_client.list_objects_v2(Bucket=BUCKET_NAME)
  print('The list of mp3 files: ')
  for  Iresponse01 in response01:
    if Iresponse01=="Contents":
        dict=response01[Iresponse01]
        for item in dict:
            imp3=item['Key']
            save_file_path = f'{DATA_FOLDER}/{imp3}'
            print(f'downloading to {save_file_path}')
            s3.Bucket(BUCKET_NAME).download_file(imp3, save_file_path)


 # beat_key=name+".txt"
    #filt and get all mp3 files in local directory
  all_song_keys = get_all_song_keys()
  print(f'all kays: {all_song_keys}')

#process every mp3 and store the .txt file locally
  for song_key in all_song_keys:

        name=song_key.split(".")[0]
        beat_key=name+".txt"
        beat_key_fname = f'{DATA_FOLDER}/{beat_key}'

        beat_list=calculate_song_beats(song_key)
        bpm = calculate_song_bpm(song_key, params = None)

        song_info_json = {
          "beat_file": beat_key,
          "beat_list": beat_list,
          "bpm": bpm
          }

        output_fp = open(beat_key_fname, "w")
        output_fp.write(json.dumps(song_info_json))
        output_fp.close()

#upload all txt files to AWS S3
  for song_key in all_song_keys:
       name=song_key.split(".")[0]
       beat_key=name+".txt"
       beat_key_fname = f'{DATA_FOLDER}/{beat_key}'
       # s3.upload_file(beat_key, BUCKET_NAME, beat_key)
       s3.Bucket(BUCKET_NAME).upload_file(beat_key_fname, beat_key)

if __name__ == '__main__':
    process_songs()


# Use the python json library (import json) to write a json dictionary to a file with json.dumps(song_info_json). Something like this:
#
# song_info_json = {
#   'beat_file': fname,
#   'beat_list': list_of_beats
# }
# output_fp.write(json.dumps(song_info_json))
