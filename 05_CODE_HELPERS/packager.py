#!/usr/bin/env python3
import subprocess, pathlib, sys

def run(cmd):
    print(' '.join(cmd))
    subprocess.check_call(cmd)

def burn(video_in, srt, video_out):
    run(['ffmpeg','-y','-i',video_in,'-vf',f'subtitles={srt}','-c:a','copy',video_out])

def concat(out, files):
    list_file = pathlib.Path(out).with_suffix('.txt')
    list_file.write_text('\n'.join([f"file '{pathlib.Path(f).as_posix()}'" for f in files]), encoding='utf-8')
    run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(list_file),'-c','copy',out])

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'burn':
        _, vin, srt, vout = sys.argv
        burn(vin, srt, vout)
    elif mode == 'concat':
        out = sys.argv[2]
        concat(out, sys.argv[3:])
    else:
        raise SystemExit('Unknown mode')
