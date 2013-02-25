import os
import glob
import subprocess
import json
import argparse


def main(input_dir):
    input_files = []
    file_types = ['*.flv', '*.mkv']

    # get all FLV or MKV files
    for file_type in file_types:
        input_files.extend(glob.glob(os.path.join(input_dir, file_type)))

    # loop over files
    for input_file in input_files:
        output_file = os.path.splitext(input_file)[0] + '.mp4'

        # check if mp4 already exists
        if os.path.isfile(output_file):
            continue

        print "Processing: " + input_file

        # get audio and video information
        cmd_res = subprocess.Popen(
            ['ffprobe', '-loglevel', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', input_file],
            stdout=subprocess.PIPE)
        ffprobe_json, stderr_out = cmd_res.communicate()

        ffprobe_data = json.loads(ffprobe_json)

        # get codec index
        if ffprobe_data['streams'][0]['codec_type'] == 'video':
            vidIndex = 0
            audIndex = 1
        else:
            vidIndex = 1
            audIndex = 0

        # check video codec
        if ffprobe_data['streams'][vidIndex]['codec_name'] != 'h264':
            print "File does not contain Video:h264. Cannot change container format."
            continue

        # check audio codec
        if ffprobe_data['streams'][audIndex]['codec_name'] == 'aac':
            audOpt = ['-c:a', 'copy']  # simply copy the stream if already in AAC
        else:
            print "Converting audio to aac"
            audOpt = ['-c:a', 'libvo_aacenc', '-ac', '2', '-ab', '192k']

        # convert the file
        cmd_opts = ['ffmpeg', '-loglevel', 'quiet', '-i', input_file, '-c:v', 'copy'] + audOpt + [output_file]
        cmd_res = subprocess.Popen(cmd_opts, stdout=subprocess.PIPE)
        cmd_res.wait()

        if cmd_res.returncode == 0:
            print "Done"
        else:
            print "ffmpeg returned non-zero status code"

    # finished processing    
    raw_input("Complete. Press ENTER to quit.\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert video files to MP4 container format.')
    parser.add_argument('input_dir', default="", help='Input directory')
    args = parser.parse_args()
    main(args.input_dir)