from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select





class BolhaUploader:

    user="Eric55on"
    password="mojenovotestnogeslo"

    def __init__(self):
        self.browser = webdriver.Firefox(executable_path='/home/erik/Downloads/geckodriver')

        #shortcut to css selector function
        self.browser.css = self.browser.find_element_by_css_selector

        self.browser.implicitly_wait(20)
        self.browser.wait = self._wait

    def exit(self):
        self.browser.dispose()

    def _wait(self, selector):
        # wait for clickability before every click
        wait = WebDriverWait(self.browser, 20)
        element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))

    def logOut(self):
        self.browser.get("https://login.bolha.com/odjava.php")

    def login(self):
        self.browser.get('https://login.bolha.com/')
        self.browser.css("#username_").send_keys(self.user)
        self.browser.css("#password_").send_keys(self.password)
        self.browser.css("#signin_submit").click()

    def objaviOglas(self, naslov, opis, cena, slike):
        #self.browser.get("http://www.bolha.com/")
        #self.browser.wait(".publishSmall")
        self.browser.get("http://objava-oglasa.bolha.com/izbor_kategorije.php")
        self.browser.css("[data-id='798']").click()
        self.browser.css("[data-id='1002']").click()
        self.browser.css("[data-id='1008']").click()

        self.browser.wait(".slick-active #next")
        self.browser.css(".slick-active #next").click()

        # podatki oglasa
        self.browser.css("#cNaziv").send_keys(naslov)
        self.browser.css("#nCenaStart").click()
        self.browser.css("#nCenaStart").send_keys(cena)
        self.browser.css("#nCenaStart").click()

        self.browser.css("#cOpis").click()
        self.browser.css("#cOpis").send_keys(opis)

        #todo slike!!!!!!!!
        self.browser.css("[name='aSlikeUpload[0]']").send_keys(slike)

        # vrsta ponudbe: fiksna cena
        Select(self.browser.css("#cTip")).select_by_value('O')

        #next page
        self.browser.css("[name='btnCheck']").click()
        self.browser.wait(".bill_sum_price")

        #next page
        self.browser.css("#next").click()


    def objaviCSV(self):
        pass


uploader = BolhaUploader()
uploader.logOut()
uploader.login()
uploader.objaviCSV()
uploader.objaviOglas("bele ploscice", "ostanek belih ploscic 20x30cm",90, "/home/erik/Desktop/bolha-uploader/ploscice.jpg")
uploader.objaviOglas("bele ploscice", "ostanek belih ploscic 20x30cm",90, "/home/erik/Desktop/bolha-uploader/ploscice.jpg")
uploader.exit()