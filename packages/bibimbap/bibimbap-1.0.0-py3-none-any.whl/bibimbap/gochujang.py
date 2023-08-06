from selenium import webdriver
import time
from PIL import Image
from io import BytesIO
from bibigo import Analyse

class Gochujang:
    def __init__(self):
        self.gochujangs = []
        self.window_size = [1200,1900]
        self.xpath_to_element_to_capture = "/html"
        self.path_to_save = 'c:/Users/Seonghwan/Desktop/'
        self.webdriver = None
        
    def add_ganjang(self, Ganjang):
        self.gochujangs.append(Ganjang)

    def set_window_size(self, width, height):
        self.window_size[0]=width
        self.window_size[1]=height

    def set_xpath_to_element_to_capture(self, xpath):
        self.xpath_to_element_to_capture = xpath

    def set_path_to_save(self, path_to_save):
        self.path_to_save = path_to_save

    def set_webdriver(self, webdriver):
        self.webdriver = webdriver
        
    def capture_screens(self):
        if self.gochujangs:
            for ganjang in self.gochujangs:
                self.screenshot(ganjang.STAGING_URL, f'{ganjang.BASE_NAME}_screen_staging.png')
                self.screenshot(ganjang.PRODUCTION_URL, f'{ganjang.BASE_NAME}_screen_production.png')

                Analyse.analyze(self.path_to_save, ganjang.BASE_NAME)
        
    def screenshot(self, url, file_name):
        driver = webdriver.Firefox(executable_path=self.set_webdriver)
        
        
        ##########################################
        driver.get(url)

        driver.set_window_size(self.window_size[0],self.window_size[1])
        driver.get(url)
        driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight)")
        driver.implicitly_wait(2)
        time.sleep(2)

        element = driver.find_element_by_xpath(self.xpath_to_element_to_capture)
        location = element.location
        size = element.size
        png = driver.get_screenshot_as_png() # saves screenshot of entire page
       
        im = Image.open(BytesIO(png)) # uses PIL library to open image in memory

        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']


        im = im.crop((left, top, right, bottom)) # defines crop points
        im.save(f'{self.path_to_save}{file_name}')
        
        ###########################################
        driver.close()
        driver.quit()