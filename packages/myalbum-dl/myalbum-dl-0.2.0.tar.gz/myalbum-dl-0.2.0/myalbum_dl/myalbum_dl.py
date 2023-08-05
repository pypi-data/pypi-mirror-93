import os
import sys
import re
import argparse
import concurrent.futures
import logging
import time
from threading import Thread, Event
import platform
import shutil
import glob
import mimetypes

import requests

from myalbum_dl.constants import (
    HEADERS,
    DOMAINS
)
if platform.system() == 'Windows':
    from myalbum_dl.constants import (
        WIN_SPINNERS as SPINNERS,
        WIN_COLORS as COLORS)
else:
    from myalbum_dl.constants import (
        SPINNERS,
        COLORS
    )


class Logger:
    FORMAT = '%(levelname)s: %(message)s'
    FORMAT_DEBUG = '%(asctime) | %(levelname)s: %(message)s'

    def __init__(self, debug):
        self.log = logging.getLogger(__name__)
        if debug:
            self.log.setLevel(logging.DEBUG)
        else:
            self.log.setLevel(logging.INFO)
        if not self.log.handlers:
            stream_handler = logging.StreamHandler()
            if debug:
                formatter = logging.Formatter(fmt=self.FORMAT_DEBUG)
                stream_handler.setLevel(logging.DEBUG)
            else:
                stream_handler.setLevel(logging.INFO)
                formatter = logging.Formatter(fmt=self.FORMAT)
            stream_handler.setFormatter(fmt=formatter)
            self.log.addHandler(stream_handler)

    def debug(self, message):
        self.log.debug(message)

    def info(self, message):
        self.log.info(message)

    def error(self, message):
        self.log.error(message)


class MyAlbum(Logger):
    def __init__(self,
                 args,
                 cwd=os.getcwd(),
                 title=None,
                 medias=[],
                 total=0,
                 count=0):
        self.separate = args.separate
        super().__init__(args.debug)
        self.cwd = cwd
        HEADERS['referer'] = args.album
        self.headers = HEADERS
        self.album_json = args.album + \
            'json' if args.album.endswith('/') else args.album + '/json'
        self.title = title
        self.medias = medias
        self.total = total
        self.count = count

    def scrape_album(self):
        with requests.get(self.album_json, headers=self.headers) as r:
            if not r.ok:
                self.log.error(
                    f'Unable to load album page——STATUS CODE: {r.status_code}')
                sys.exit(0)
        if r.ok:
            content = r.json()
            self.title = self.clean_text(content['album']['title'])
            itemdata = content['itemdata']
            ids = list(itemdata)
            for id_ in ids:
                media = itemdata[id_]
                if media['type'] == 10:
                    media_url = media['sizes'][-1][-2]
                    filename = media['photo']['fileName'].rsplit('.', 1)[
                        0] + '.mp4'
                    self.medias.append((media_url, filename))
                elif media['type'] == 1:
                    media_url = media['sizes'][-1][-2]
                    filename = media['fileName']
                    self.medias.append((media_url, filename))
                else:
                    pass
            self.log.info(f"{self.title} : {content['album']['subTitle']}")
            self.total = len(self.medias)

    def prepare_download(self):
        if self.medias:
            self.headers['accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            os.makedirs(os.path.join(self.cwd, self.title), exist_ok=True)
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {
                    executor.submit(self.download, media): media for media in self.medias}
                for future in concurrent.futures.as_completed(futures):
                    future.result
            if self.separate:
                self.separate_media()
        else:
            self.log.info(f'Found 0 items in album——quitting program')
            sys.exit(0)

    def download(self, media):
        count = 0
        while True:
            url = DOMAINS[count] + media[0]
            filename = media[1]
            with requests.get(url, headers=self.headers) as r:
                if not r.ok:
                    count += 1
                else:
                    with open(os.path.join(self.cwd, self.title, filename), 'wb') as f:
                        for chunk in r.iter_content(chunk_size=1024):
                            f.write(chunk)
                    self.count += 1
                    break
            if count > 2:
                self.log.error(
                    f'Unable to download media ({filename})——STATUS CODE: {r.status_code}')

    def separate_media(self):
        dir_ = os.path.join(self.cwd, self.title)
        files = glob.glob(dir_ + '\\*.*')
        if files:
            image_pattern = re.compile(r'image/\w+')
            video_pattern = re.compile(r'video/\w+')
            image_files, video_files = [], []
            for file in files:
                try:
                    if re.search(image_pattern, mimetypes.guess_type(file)[0]):
                        image_files.append(file)
                    elif re.search(video_pattern, mimetypes.guess_type(file)[0]):
                        video_files.append(file)
                    else:
                        pass
                except TypeError:
                    pass
            if image_files:
                image_dir = os.path.join(dir_, 'Images')
                os.makedirs(image_dir, exist_ok=True)
                for file in image_files:
                    shutil.move(os.path.join(dir_, file), image_dir)
            if video_files:
                video_dir = os.path.join(dir_, 'Videos')
                os.makedirs(video_dir, exist_ok=True)
                for file in video_files:
                    shutil.move(os.path.join(dir_, file), video_dir)
        return

    def spinner(self, event):
        while True:
            for color in COLORS:
                for spinner in SPINNERS:
                    if event.is_set():
                        return None
                    print(f' {color[0]}{spinner}{color[1]} [{self.count}/{self.total}]',
                          end='\r', flush=True)
                    time.sleep(0.1)

    @staticmethod
    def clean_text(text):
        pattern = re.compile(r'[:./\\\\]')
        cleaned_text = re.sub(pattern, '_', text)
        return cleaned_text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'album', type=str, help='URL of the album to scrape')
    parser.add_argument(
        '--debug', type=int, help='option to enable debugging', choices=[0, 1], nargs='?', const=1, default=0, required=False)
    parser.add_argument(
        '-s', '--separate', type=int, help='separate media types into their own directories', nargs='?', const=1, default=0, choices=[0, 1], required=False)
    args = parser.parse_args()
    myalbum = MyAlbum(args)
    myalbum.scrape_album()
    e1 = Event()
    t1 = Thread(target=myalbum.spinner, args=(e1,))
    t1.start()
    myalbum.prepare_download()
    e1.set()


if __name__ == '__main__':
    main()
