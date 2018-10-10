# Overview

Program to process songs and upload meta info

# How to run
run:
python main-01.py
1) Download all files from AWS Bucket 'songhaow-test' store them in the local directory of "data";
2) process beats & bpm and write into txt files (in jason format) into local directory of "data";
3) Upload the txt files into the "songhaow-test" BUCKET in the AWS cloud.

run:
python get_all_song_keys.py
you get all keys for the music files.

main-00.py is the original code without calling jason function.

The formulations in beats_list and bpm calculations are from the source codes of aubio. The logic and the results need to be verified.
