"""This module is a script that processes AWS songs to find bpm / beats, etc
"""
#! /usr/bin/env python
import sys
from aubio import source, tempo
from numpy import median, diff
import os

def get_all_song_keys():
    """Connect to AWS and find all songs in a storage location (in AWS, this is
    called a bucket). Get all the song storage location names and return them
    in a list.
    :return: example -
      [
        'songhaow-test-123/fb752f5e-e8f1-4b8a-b114-4fd3d1c937d7',
        'songhaow-test-123/some-other-hash-key',
        ...
      ]
    """
    allfiles=os.listdir()
    print ("allfiles: ", allfiles)
    all_song_kays=[]

    for filename in allfiles:
        name=filename.split(".")[0]
        sufname=filename.split(".")[1]
        if(sufname=="mp3"):
          thismp3=name+".mp3"
          all_song_kays.append(thismp3)
        else: pass

    print ("\n")
    for filename in all_song_kays:
      print (filename)

    return all_song_kays

def calculate_song_bpm(path, params=None):
 # def calculate_song_bpm(song_fp):
 #    """Call the functions you wrote in bpmndbeats.py to find the song's bpm and
 #    then return that value.
 #    """
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

fh1=open("BeatsMusic.txt", "w")
fh1.write('{ "The Music of": ')

# ///////////////////////////////////////
def calculate_song_beats(path, params=None):
 # def calculate_song_beats(song_fp):
 #    """Call the functions you wrote in bpmndbeats.py to calculate the song's
 #    beats
 #    """
  win_s = 512                 # fft size
  hop_s = win_s // 2          # hop size
  filename=path
  samplerate = 0
  total_frames = 0
  s = source(filename, samplerate, hop_s)
  samplerate = s.samplerate
  o = tempo("default", win_s, hop_s, samplerate)
  delay = 4. * hop_s
    # list of beats, in samples
  beats = []
  beats01=[]
  fh1.write(filename)
  fh1.write(",")
  fh1.write("\n")
  fh1.write('"beat_list": [')

  while True:
      samples, read = s()
      is_beat = o(samples)
      if is_beat:
        this_beat = int(total_frames - delay + is_beat[0] * hop_s)
        beats.append(this_beat)
        # beats01.append(this_beat / float(samplerate))
        # print("%6.1f" % (this_beat / float(samplerate)))
        fh1.write("%6.1f" % (this_beat / float(samplerate)))
      total_frames += read
      if read < hop_s: break

  return 0.0

# Try to write beats into a file at once
# import numpy as np
# np.set_printoptions(formatter={'float': '{: 0.3f}'.format})
# # np.set_printoptions(precision=3)
# print beats01
# fh1.write("beats: ", beats01)
# return []  # empty list of beats
# if __name__ == '__main__':
def process_songs():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', help="mode [default|fast|super-fast]", dest="mode")
    """
    when you type : python demo_bpm_extract.py -m fast
    add_arguent will put the word "fast" under the "mode" keyu in your dictionary
    """
    parser.add_argument('sources', nargs='*', help="input_files")
    args = parser.parse_args()

    all_song_keys=get_all_song_keys()

    for filename in all_song_kays:
        beat_list=calculate_song_beats(filename, params = args)
        bpm = calculate_song_bpm(filename, params = args)
        # print("{:6s} {:s}".format("{:2f}".format(bpm),f))
        print ("source file: ",filename)
        print (("The bpm is: %7.1f.") %bpm)
        fh1.write("]")
        fh1.write(",")
        fh1.write("\n")
        fh1.write(('"bpm": %i') %bpm)
        fh1.write("}")
        fh1.close()

if __name__ == '__main__':
    process_songs()

# fh1.write("]")
# fh1.write(",")
# fh1.write("\n")
# fh1.write(('"bpm": %i') %bpm)
# fh1.write("}")
# fh1.close()

# def process_songs():
#     """This is the main function for looping through all the songs you find in
#     AWS S3 bucket, downloading, processing, and then uploading meta info.
#      We wnat to keep logic simple so it is easy to read what is going on. So we
#     break everything into small component functions. This also makes writing
#     the functions easier because each function does a small simple task.
#     """
#     all_song_keys = get_all_song_keys()
#     for song_key in all_song_keys:
#         song_fp = download_song_to_memory(song_key)
#         song_bpm = calculate_song_bpm(song_fp)
#         beats_list = calculate_song_beats(song_fp)
#         info_json = create_song_info_json(song_bpm, beats_list)
#         write_json_info_to_s3(json_info, song_key)
#


    # return 0.0

# 1)  def create_song_info_json(song_bpm, beats_list):
#     """This is complete -- it just creates the json object you want to write
#     """
#     return {
#         'bpm': song_bpm,
#         'beats_list': beats_list
#     }
#
# 2)  def download_song_to_memory():
#     """Use AWS boto API to download the song into the program's memory as a
#     File object
#     """
#     return None  # returning nothing for now
#
# 3)  def get_all_song_keys():
#     """Connect to AWS and find all songs in a storage location (in AWS, this is
#     called a bucket). Get all the song storage location names and return them
#     in a list.
#     :return: example -
#       [
#         'songhaow-test-123/fb752f5e-e8f1-4b8a-b114-4fd3d1c937d7',
#         'songhaow-test-123/some-other-hash-key',
#         ...
#       ]
#     """
#     return []
#
# 4)  def write_json_info_to_s3(json_info, song_key):
#     """Writes the json_info to AWS S3 under the same name as the song except
#     with a .info postfix. Example:
#         If the song S3 key is songhaow-test-123/song1, your info file would be
#         songhaow-test-123/song1.info
#     """
#     pass  # pass means do nothing
#
# 5)  def process_songs():
#     """This is the main function for looping through all the songs you find in
#     AWS S3 bucket, downloading, processing, and then uploading meta info.
#      We wnat to keep logic simple so it is easy to read what is going on. So we
#     break everything into small component functions. This also makes writing
#     the functions easier because each function does a small simple task.
#     """
#     all_song_keys = get_all_song_keys()
#     for song_key in all_song_keys:
#         song_fp = download_song_to_memory(song_key)
#         song_bpm = calculate_song_bpm(song_fp)
#         beats_list = calculate_song_beats(song_fp)
#         info_json = create_song_info_json(song_bpm, beats_list)
#         write_json_info_to_s3(json_info, song_key)
#
# 6) if __name__ == '__main__':
#     process_songs()
