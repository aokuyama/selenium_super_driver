import os
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

class SuperDriver:
    cookies_path = '/app/cache/cookies.pkl'
    screen_shot_img_path = '/app/cache/ss.png'
    screen_shot_html_path = '/app/cache/ss.html'
    chromedriver_path = '/usr/lib/chromium/chromedriver'
    binary_location = '/usr/bin/chromium-browser'

    def createOption(self):
        options = Options()
        options.binary_location = self.binary_location
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1200x600')
        options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36')
        return options

    def createService(self):
        service = Service(executable_path=self.chromedriver_path)
        service.start()
        return service

    def createDriver(self, service, options):
        return webdriver.Remote(
            service.service_url,
            desired_capabilities = options.to_capabilities()
        )

    def make(self):
        options = self.createOption()
        self.service = self.createService()
        self.driver = self.createDriver(self.service, options)
        self.load_cookies()
        return self
    
    def get(self, url):
        return self.driver.get(url)

    def find_element_by_id(self, id):
        return self.driver.find_element_by_id(id)

    def find_element_by_class_name(self, name):
        return self.driver.find_element_by_class_name(name)

    def find_element_by_name(self, name):
        return self.driver.find_element_by_name(name)

    def print_title(self):
        print(self.driver.title)
        return self

    def print_url(self):
        print(self.driver.current_url)
        return self

    def ss(self):
        self.screen_shot()
        self.screen_shot_html()
        return self

    def screen_shot(self):
        self.driver.save_screenshot(self.screen_shot_img_path)

    def screen_shot_html(self):
        html = self.driver.page_source
        with open(self.screen_shot_html_path, 'w', encoding='utf-8') as f:
            f.write(html)

    def load_cookies(self):
        if not os.path.isfile(self.cookies_path):
            return
        self.get_dummy_page()
        cookies = pickle.load(open(self.cookies_path, 'rb'))
        for cookie in cookies:
            self.driver.add_cookie(cookie)

    # どこでもいいのでページを開かないとクッキーを読み込めないため、仕方なく
    def get_dummy_page(self):
        self.driver.get('https://www.google.com/')

    def save_cookies(self):
        pickle.dump(self.driver.get_cookies() , open(self.cookies_path, 'wb'))

    def quit(self):
        self.save_cookies()
        self.driver.quit()
        self.service.stop()

def get():
    return SuperDriver().make()
