import os
import sys
import getopt
from handler import Downloader

COOKIE_PATH = '~/Downloads/'

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
        path = os.path.expanduser(COOKIE_PATH)
        cookies_files = [os.path.join(path, i) for i in os.listdir(path) if os.path.isfile(os.path.join(path, i)) and 'mscookies' in i]
        for filename in cookies_files:
            try:
                os.remove(filename)
            except OSError:
                pass

        Downloader(username_arg, video_arg)
