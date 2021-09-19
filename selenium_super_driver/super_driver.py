import os
import pickle
import random
import time
import unittest
from pathlib import PurePath
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from logger import get_logger, get_test_logger


class SuperDriver:
    def __init__(self, logger):
        self.logger = logger

    def createOption(self):
        options = Options()
        options.binary_location = self.binary_location()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--single-process")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280x800")
        options.add_argument('--start-maximized')
        options.add_argument("--disable-application-cache")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-infobars")
        options.add_argument("--hide-scrollbars")
        options.add_argument("--enable-logging")
        options.add_argument("--log-level=0")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument('--user-data-dir=' + self.user_session_dir())
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36')
        return options

    def createService(self):
        service = Service(executable_path=self.chromedriver_path())
        return service

    def createSeleniumWireOptions(self):
        options = {}
        proxy = None
        host = os.getenv('PROXY_HOST')
        port = os.getenv('PROXY_PORT')
        user = os.getenv('PROXY_USER')
        password = os.getenv('PROXY_PASSWORD')
        if (host and port):
            if (user and password):
                proxy = f'http://{user}:{password}@{host}:{port}'
            else:
                proxy = f'http://{host}:{port}'
        if (proxy):
            options = {
                'proxy': {
                    'https': proxy,
                }
            }
        return options

    def createDriver(self, service, options):
        seleniumwire_options = self.createSeleniumWireOptions()
        if (seleniumwire_options):
            from seleniumwire import webdriver
            return webdriver.Remote(
                service.service_url,
                desired_capabilities=options.to_capabilities(),
                seleniumwire_options=self.createSeleniumWireOptions()
            )
        from selenium import webdriver
        return webdriver.Remote(
            service.service_url,
            desired_capabilities=options.to_capabilities(),
        )

    def make(self, waiter):
        self.options = self.createOption()
        self.service = self.createService()
        self.waiter = waiter
        self.driver = False
        return self

    def standby(self):
        if (not self.driver):
            self.service.start()
            self.driver = self.createDriver(self.service, self.options)
            self.load_cookies()
            self.driver.implicitly_wait(5)
        return self.waiting()

    def waiting(self):
        return self.waiter.waiting()

    def get(self, url):
        self.standby()
        return self.driver.get(url)

    def find_element_by_id(self, id):
        self.standby()
        return self.driver.find_element_by_id(id)

    def find_element_by_class_name(self, name):
        self.standby()
        return self.driver.find_element_by_class_name(name)

    def find_element_by_name(self, name):
        self.standby()
        return self.driver.find_element_by_name(name)

    def find_elements_by_name(self, name):
        self.standby()
        return self.driver.find_elements_by_name(name)

    def fetch_element_by_id(self, name, target=0, found=1):
        self.standby()
        return self.fetch_element(self.driver.find_elements_by_id(name), target, found)

    def fetch_element_by_name(self, name, target=0, found=1):
        self.standby()
        return self.fetch_element(self.driver.find_elements_by_name(name), target, found)

    def find_element_by_xpath(self, xpath):
        self.standby()
        return self.driver.find_element_by_xpath(xpath)

    def find_elements_by_xpath(self, xpath):
        self.standby()
        return self.driver.find_elements_by_xpath(xpath)

    def fetch_element_by_xpath(self, xpath, target=0, found=1):
        self.standby()
        return self.fetch_element(self.driver.find_elements_by_xpath(xpath), target, found)

    def find_element_by_css_selector(self, css):
        self.standby()
        return self.driver.find_element_by_css_selector(css)

    def find_elements_by_css_selector(self, css):
        self.standby()
        return self.driver.find_elements_by_css_selector(css)

    def fetch_element_by_css_selector(self, css, target=0, found=1):
        self.standby()
        return self.fetch_element(self.driver.find_elements_by_css_selector(css), target, found)

    def find_element_by_link_text(self, text):
        self.standby()
        return self.driver.find_element_by_link_text(text)

    def find_elements_by_link_text(self, text):
        self.standby()
        return self.driver.find_elements_by_link_text(text)

    def fetch_element_by_link_text(self, text, target=0, found=1):
        self.standby()
        return self.fetch_element(self.driver.find_elements_by_link_text(text), target, found)

    def fetch_element(self, elements, target, found):
        if len(elements) == found:
            return elements[target]
        return

    def element_to_be_clickable_by_xpath(self, name, sec=5):
        return self.element_to_be_clickable_by(By.XPATH, name, sec=5)

    def element_to_be_clickable_by(self, by, name, sec=5):
        try:
            element = WebDriverWait(self.driver, sec).until(
                EC.element_to_be_clickable((by, name))
            )
        except TimeoutException:
            return
        return element

    def visibility_of_element_located_by_css_selector(self, name, sec=5):
        return self.visibility_of_element_located_by(By.CSS_SELECTOR, name, sec=5)

    def visibility_of_element_located_by_xpath(self, name, sec=5):
        return self.visibility_of_element_located_by(By.XPATH, name, sec=5)

    def visibility_of_element_located_by(self, by, name, sec=5):
        try:
            element = WebDriverWait(self.driver, sec).until(
                EC.visibility_of_element_located((by, name))
            )
        except TimeoutException:
            return
        return element

    def switch_to_frame(self, iframe):
        self.standby()
        self.driver.switch_to_frame(iframe)
        return self

    def accept(self):
        self.standby()
        self.standby()
        self.standby()
        Alert(self.driver).accept()

    def print_title(self):
        self.logger.info(self.driver.title)
        return self

    def print_url(self):
        self.logger.info(self.driver.current_url)
        return self

    def ss(self, filename='ss'):
        self.screen_shot(filename + '.png')
        self.screen_shot_html(filename + '.html')
        return self

    def screen_shot(self, filename='ss.png'):
        os.makedirs(self.screen_shot_img_path(), exist_ok=True)
        self.driver.save_screenshot(
            self.screen_shot_img_path() + "/" + filename)

    def screen_shot_html(self, filename='ss.html'):
        os.makedirs(self.screen_shot_html_path(), exist_ok=True)
        html = self.driver.page_source
        with open(self.screen_shot_html_path() + "/" + filename, 'w', encoding='utf-8') as f:
            f.write(html)

    def load_cookies(self):
        if not os.path.isfile(self.cookies_path()):
            return
        self.get_dummy_page()
        cookies = pickle.load(open(self.cookies_path(), 'rb'))
        for cookie in cookies:
            self.driver.add_cookie(cookie)

    # どこでもいいのでページを開かないとクッキーを読み込めないため、仕方なく
    def get_dummy_page(self):
        self.driver.get('https://www.google.com/')

    def save_cookies(self):
        pickle.dump(self.driver.get_cookies(), open(self.cookies_path(), 'wb'))

    def user_session_dir(self):
        return os.getenv('USER_SESSION_DIR', '/app/cache/')

    def user_download_dir(self):
        return os.getenv('USER_DOWNLOAD_DIR', '/app/cache/')

    def cookies_path(self):
        return str(PurePath(self.user_session_dir(), 'cookies.pkl'))

    def screen_shot_img_path(self):
        return str(PurePath(self.user_download_dir()))

    def screen_shot_html_path(self):
        return str(PurePath(self.user_download_dir()))

    def chromedriver_path(self):
        return os.getenv('PATH_CHROME_DRIVER', '/usr/lib/chromium/chromedriver')

    def binary_location(self):
        return os.getenv('PATH_CHROME_BIN', '/usr/bin/chromium-browser')

    def quit(self):
        if (self.driver):
            self.save_cookies()
            self.driver.quit()
            self.service.stop()


class Waiter:
    def waiting(self):
        time.sleep(random.uniform(1, 2))
        return True


class NoWaiter:
    def waiting(self):
        return False


def get(no_wait=False, logger=None):
    if (not logger):
        logger = get_logger('selenium')
    if (no_wait):
        waiter = NoWaiter()
    else:
        waiter = Waiter()
    return SuperDriver(logger=logger).make(waiter)


class TestSuperDriver(unittest.TestCase):
    def setUp(self):
        os.environ.pop('USER_SESSION_DIR', None)
        os.environ.pop('USER_DOWNLOAD_DIR', None)
        self.driver = get(logger=get_test_logger())

    def testウェイトなし(self):
        self.driver = get({'no_wait': True})
        self.assertEqual(False, self.driver.waiter.waiting())

    def testロードなしで終了(self):
        self.driver.quit()

    def testデフォルトのキャッシュ用パス(self):
        self.assertEqual('/app/cache/cookies.pkl', self.driver.cookies_path())
        self.assertEqual('/app/cache', self.driver.screen_shot_img_path())
        self.assertEqual('/app/cache', self.driver.screen_shot_html_path())

    def test環境変数でキャッシュ用パス置き換え(self):
        os.environ['USER_SESSION_DIR'] = '/mnt/efs/'
        os.environ['USER_DOWNLOAD_DIR'] = '/mnt/efs2/'
        self.assertEqual('/mnt/efs/cookies.pkl', self.driver.cookies_path())
        self.assertEqual('/mnt/efs2', self.driver.screen_shot_html_path())

    def testスラッシュ忘れへの対応(self):
        os.environ['USER_SESSION_DIR'] = '/mnt/efs'
        os.environ['USER_DOWNLOAD_DIR'] = '/mnt/efs2'
        self.assertEqual('/mnt/efs/cookies.pkl', self.driver.cookies_path())
        self.assertEqual('/mnt/efs2', self.driver.screen_shot_html_path())

    def testchromeへのパスのデフォルト(self):
        if os.getenv('PATH_CHROME_DRIVER'):
            del os.environ['PATH_CHROME_DRIVER']
        if os.getenv('PATH_CHROME_BIN'):
            del os.environ['PATH_CHROME_BIN']
        self.assertEqual('/usr/lib/chromium/chromedriver',
                         self.driver.chromedriver_path())
        self.assertEqual('/usr/bin/chromium-browser',
                         self.driver.binary_location())

    def test環境変数でchromeパス置き換え(self):
        os.environ['PATH_CHROME_DRIVER'] = '/var/task/bin/chromedriver'
        os.environ['PATH_CHROME_BIN'] = '/var/task/bin/chromium-browser'
        self.assertEqual('/var/task/bin/chromedriver',
                         self.driver.chromedriver_path())
        self.assertEqual('/var/task/bin/chromium-browser',
                         self.driver.binary_location())

    def test_プロキシ設定がない(self):
        if os.getenv('PROXY_HOST'):
            del os.environ['PROXY_HOST']
        self.assertEqual({}, self.driver.createSeleniumWireOptions())

    def test_プロキシ設定がある(self):
        if os.getenv('PROXY_USER'):
            del os.environ['PROXY_USER']
        os.environ['PROXY_HOST'] = 'example.com'
        os.environ['PROXY_PORT'] = '3128'
        equal = {
            'proxy': {
                'https': f'http://example.com:3128',
            }
        }
        self.assertEqual(equal, self.driver.createSeleniumWireOptions())

    def test_認証つきプロキシ設定がある(self):
        os.environ['PROXY_HOST'] = 'test.example.com'
        os.environ['PROXY_PORT'] = '13128'
        os.environ['PROXY_USER'] = 'john'
        os.environ['PROXY_PASSWORD'] = 'ABCDefg1234'
        equal = {
            'proxy': {
                'https': f'http://john:ABCDefg1234@test.example.com:13128',
            }
        }
        self.assertEqual(equal, self.driver.createSeleniumWireOptions())


if __name__ == '__main__':
    unittest.main()
