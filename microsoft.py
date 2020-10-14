import asyncio
import sys
import getopt
from handler import Downloader

if __name__ == '__main__':
    options = getopt.getopt(sys.argv[1:], '', ['username=', 'video='])
    username_arg = None
    video_arg = None
    errs = False

    for opt, arg in options[0]:
        if opt in '--username':
            username_arg = arg
        if opt in '--video':
            video_arg = arg

    if username_arg is None:
        print(
            '--username parameter is missing, pass your MS Stream account username with '
            '--username=myusername@email.com\n')
        errs = True
    if video_arg is None:
        print('--video parameter is missing, pass the video link with --video=link\n')
        errs = True

    if not errs:
        Downloader(username_arg, video_arg)
