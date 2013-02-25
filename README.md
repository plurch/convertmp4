MP4 Video Converter
========

Description
--------

This program converts all **FLV** and **MKV** video files in a directory to the **MP4** container format. The resulting MP4 format is suitable for playback on a range of devices including iOS (iPhone and iPad), Android, and Playstation 3.

Efficient conversion is accomplished by copying the video stream (H.264) and transcoding the audio stream to AAC if necessary.

Requirements
--------

The [ffmpeg program](http://www.ffmpeg.org/) must be installed and in your system path.

Usage
--------

This program runs using Python 2.7. 

    positional arguments:
      input_dir   Input directory

Example:

    > python convertmp4.py /path/to/videos


