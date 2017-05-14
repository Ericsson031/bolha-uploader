from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import re
from dicttoxml import dicttoxml
import time
import hashlib
from urllib import urlretrieve


class BolhaUploader:

    user="Eric55on"
    public_user = "Eric55on"
    password="mojenovotestnogeslo"
    my_ads = dict()

    def __init__(self):
        self.browser = webdriver.Firefox(executable_path='/home/erik/Downloads/geckodriver')

        #shortcut to css selector function
        self.browser.css = self.browser.find_element_by_css_selector
        self.browser.css_all = self.browser.find_elements_by_css_selector

        self.browser.implicitly_wait(20)
        self.browser.wait = self._wait

    def exit(self):
        self.browser.quit()

    def _wait(self, selector):
        # wait for clickability before every click
        wait = WebDriverWait(self.browser, 20)
        element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        return self.browser.css(selector)

    def logOut(self):
        self.browser.get("https://login.bolha.com/odjava.php")

    def logIn(self):
        self.browser.get('https://login.bolha.com/')
        self.browser.css("#username_").send_keys(self.user)
        self.browser.css("#password_").send_keys(self.password)
        self.browser.css("#signin_submit").click()

    def publishAd(self, naslov, opis, cena, slike):
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

        self.browser.css("[name='aSlikeUpload[0]']").send_keys(slike)

        # vrsta ponudbe: fiksna cena
        Select(self.browser.css("#cTip")).select_by_value('O')

        #next page
        self.browser.css("[name='btnCheck']").click()
        self.browser.wait(".bill_sum_price")

        #next page
        self.browser.css("#next").click()

    def getPublishedAds(self):
        self.browser.get("https://moja.bolha.com/oglasi")
        ad_links = []

        # getting the links to all my ad pages
        self.browser.wait(".ad .title")

        #todo add pagination!!!!
        for ad in self.browser.css_all(".ad .title a"):
            ad_links.append(ad.get_attribute("href"))


        for link in ad_links:
            self.browser.get(link)
            self.browser.wait(".ad .content")

            price = self.browser.css(".ad .price span").text
            price = re.sub("[^0-9,]", "", price)
            naslov = self.browser.css(".ad h1").text
            slika_url = self.browser.css(".imgHolder .gal").get_attribute("href")
            ad = {
                "id": self.browser.css(".save").get_attribute("data-id"),
                "naslov": naslov,
                "opis": self.browser.css(".ad .content").text,
                "cena":price,
                "slika_url": slika_url,
                "slika_file": self._hashFilename(naslov, slika_url),
            }
            self.my_ads[ad["id"]] = ad

    def _hashFilename(self, naslov, url):
        hash = hashlib.md5(naslov.encode("ascii",errors="ignore")).hexdigest()
        file_type = url.split(".")[-1]
        folder = "images/"
        return folder + hash + "." + file_type

    def checkIfTop(self):
        #todo do we have to be on 1st place or is 2, 3 ,4 ,5 ok?
        self.browser.get("http://www.bolha.com/gradnja/tla/keramika/")
        # open the firt ad in the category
        self.browser.css(".ad h3 a").click()

        # check if it belongs to our user
        print self.browser.wait("#sellerInfo").text
        return self.public_user in self.browser.wait("#sellerInfo").text

    def exportToXML(self):
        open("ads.xml", "w").write(dicttoxml(self.my_ads))

    def deleteAllAds(self):
        self.browser.get("https://moja.bolha.com/oglasi")
        for checkbox in self.browser.css_all(".ad input"):
            checkbox.click()
        self.browser.css("#removeActiveBulk").click()
        self.browser.wait(".dialog_Confirm").click()
        time.sleep(3)

    def uploadAds(self):
        # It will take my_ads variable and create appropriate ads
        for key, ad in self.my_ads.iteritems():
            self.publishAd(ad["naslov"], ad["opis"], ad["cena"],self._hashFilename(ad["naslov"], ad["slika_url"]))

    def downladImages(self):
        for key, ad in self.my_ads.iteritems():
            urlretrieve(ad["slika_url"], ad["slika_file"])


uploader = BolhaUploader()
uploader.logOut()
uploader.logIn()
#uploader.publishAd("Zelene ploscice", "Pri renoviranju kopalnice nam je ostalo cca 4m^2 20x20cm ploscic zelene barve",90, "/home/erik/Desktop/bolha-uploader/ploscice.jpg")
#time.sleep(10)
#print uploader.checkIfTop()
uploader.getPublishedAds()
uploader.downladImages()
uploader.exportToXML()
#uploader.deleteAllAds()
uploader.uploadAds()
#uploader.objaviCSV()
#uploader.publishAd("bele ploscice", "ostanek belih ploscic 20x30cm",90, "/home/erik/Desktop/bolha-uploader/ploscice.jpg")
#uploader.publishAd("bele ploscice", "ostanek belih ploscic 20x30cm",90, "/home/erik/Desktop/bolha-uploader/ploscice.jpg")
uploader.exit()