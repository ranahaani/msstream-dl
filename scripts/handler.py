#!/usr/bin/env python3
import getpass
import logging
import os
import re
from pathlib import Path, PurePath
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

LOG = logging.getLogger(__name__)


class Downloader:
    def __init__(self, username, video_url):
        self.username = username
        self.password = getpass.getpass()
        self.video_url = video_url
        self.title = ''
        driver_manager = ChromeDriverManager().install()
        chrome_options = Options()
        try:
            ext_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets", 'cookies')
            print(ext_path)
            chrome_options.add_argument('--load-extension={}'.format(ext_path))
        except NoSuchElementException as err:
            LOG.error(err.message)
            exit()
        self.driver = webdriver.Chrome(executable_path=driver_manager, options=chrome_options)
        self.login()

    def login(self):
        """
        Login to MS stream
        """
        LOG.info(f'Trying to login user: {self.username}...')
        self.driver.get('https://web.microsoftstream.com/')

        self.driver.find_element_by_css_selector('input[type="email"]').send_keys(self.username)
        self.driver.find_element_by_css_selector('input[type="submit"]').click()
        self.driver.find_element_by_css_selector('input[type="password"]').send_keys(self.password)
        sleep(2)
        self.driver.find_element_by_css_selector('input[type="submit"]').click()
        sleep(2)
        try:
            self.driver.find_element_by_css_selector('input[type="submit"]').click()
        except Exception as ex:
            print(ex)
        self.driver.execute_script(f"window.open('https://web.microsoftstream.com/')")
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.get(self.video_url)
        LOG.info(f'Logged in user: {self.username} successfully...')
        sleep(8)  # Waiting until cookie file download into your system
        LOG.info(f'closing browser...')
        self.title = re.sub('[^A-Za-z0-9]+', ' ', self.driver.title)
        self.driver.quit()
        self.download_video()

    @staticmethod
    def __add_cookies_with_file():
        LOG.info('looking for cookies file...')
        cookie_path = str(PurePath(Path.home(), "Downloads"))
        cookie_files = sorted([i for i in os.listdir(cookie_path) if os.path.isfile(os.path.join(cookie_path, i)) and \
                               'mscookies' in i])
        if len(cookie_files) > 0:
            LOG.info(f'Found {cookie_files[-1]} in {cookie_path} directory.')
            with open(os.path.join(cookie_path, cookie_files[-1]), 'r') as file:
                content = file.read().split(';')
                return content
        else:
            LOG.error('No cookies files found...')
            exit()

    def __extract_info(self):
        header_details = self.__add_cookies_with_file()
        manifest_url = [i for i in header_details if 'https://' in i]
        if manifest_url:
            manifest_url = manifest_url[0]
        else:
            print('[ERROR] something missing in cookies, ty again!!!')
        header_details.remove(manifest_url)
        m3u8_manifest_url = manifest_url[:manifest_url.rfind('/')] + '/manifest(format=m3u8-aapl)'
        return header_details, m3u8_manifest_url, self.title.replace(" ", "_")

    def download_video(self):
        header_details, url, video_title = self.__extract_info()
        yt_dl_command = f"youtube-dl --output '{video_title}.mp4' --no-call-home --add-header " \
                        f"\"Cookie:{header_details[0]};{header_details[1]}\" \"{url}\" "
        os.system(yt_dl_command)
