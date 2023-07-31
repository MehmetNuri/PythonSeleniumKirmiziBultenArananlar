import time

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
from selenium.webdriver.chrome.options import Options

chromedriver_autoinstaller.install()
options = Options()
options.add_argument("--disable-extensions")
options.add_argument("--headless")
aranan_list = list()

kategori_list = ["red-level", "blue-level", "green-level", "orange-level", "grey-level"]


def process_data(kategori, driver):
    load_more = driver.find_element(By.XPATH, "//a[@id='dahaFazlaYukleBtn']")
    while True:
        driver.execute_script("arguments[0].scrollIntoView();", load_more)
        time.sleep(0.4)
        driver.execute_script("arguments[0].click();", load_more)
        if load_more.get_attribute("style") == "display: none;":
            break

    content = driver.find_elements(By.XPATH, "//div[@class='deactivated-list-card " + kategori + "']")
    for c in content:
        aranan = dict()

        if len(c.text) > 0:
            text_arr = c.text.split("\n")
            ad_soyad = text_arr[0]
            dogum_yeri_tarihi = text_arr[1].split("-")
            orgut = text_arr[2]
            aranan.update({"adSoyad": ad_soyad})
            aranan.update({"dogumYeri": dogum_yeri_tarihi[0]})
            aranan.update({"dogumTarihi": dogum_yeri_tarihi[1]})
            aranan.update({"orgut": orgut})

            if kategori == "red-level":
                aranan.update({"kategori": "KIRMIZI"})
            elif kategori == "orange-level":
                aranan.update({"kategori": "TURUNCU"})
            elif kategori == "blue-level":
                aranan.update({"kategori": "MAVİ"})
            elif kategori == "green-level":
                aranan.update({"kategori": "YEŞİL"})
            elif kategori == "grey-level":
                aranan.update({"kategori": "GRİ"})

            if c.find_element(By.CLASS_NAME, "deactivated-list-card-img ") is not None:
                if len(c.find_element(By.CLASS_NAME, "deactivated-list-card-img ").get_attribute("style")) > 0:
                    resim = c.find_element(By.CLASS_NAME, "deactivated-list-card-img ").get_attribute("style")
                    resim = "https://www.terorarananlar.pol.tr" + resim.split(":")[1].split('"')[1]
                    aranan.update({"resim": resim})

            aranan_list.append(aranan)


for kategori in kategori_list:
    button = None

    if kategori == "red-level":
        driver = webdriver.Chrome(options=options)
        driver.get("https://www.terorarananlar.pol.tr/tarananlar")
        button = driver.find_element(By.CLASS_NAME, "wanted-red-button")
        driver.execute_script("arguments[0].click();", button)
        time.sleep(0.4)
        process_data(kategori, driver)
        driver.close()

    if kategori == "blue-level":
        driver = webdriver.Chrome(options=options)
        driver.get("https://www.terorarananlar.pol.tr/tarananlar")
        time.sleep(0.4)
        button = driver.find_element(By.CLASS_NAME, "wanted-blue-button")
        driver.execute_script("arguments[0].click();", button)
        time.sleep(0.4)
        process_data(kategori, driver)
        driver.close()
    if kategori == "orange-level":
        driver = webdriver.Chrome(options=options)
        driver.get("https://www.terorarananlar.pol.tr/tarananlar")
        time.sleep(0.4)
        button = driver.find_element(By.CLASS_NAME, "wanted-orange-button")
        driver.execute_script("arguments[0].click();", button)
        time.sleep(0.4)
        process_data(kategori, driver)
        driver.close()

    if kategori == "green-level":
        driver = webdriver.Chrome(options=options)
        driver.get("https://www.terorarananlar.pol.tr/tarananlar")
        time.sleep(0.4)
        button = driver.find_element(By.CLASS_NAME, "wanted-green-button")
        driver.execute_script("arguments[0].click();", button)
        process_data(kategori, driver)
        driver.close()

    if kategori == "grey-level":
        driver = webdriver.Chrome(options=options)
        driver.get("https://www.terorarananlar.pol.tr/tarananlar")
        time.sleep(0.4)
        button = driver.find_element(By.CLASS_NAME, "wanted-grey-button")
        driver.execute_script("arguments[0].click();", button)
        process_data(kategori, driver)
        driver.close()

with open('arananlar.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['AD SOYAD', 'DOĞUM YERİ', 'DOĞUM YILI', 'ÖRGÜT', 'KATEGORİ', 'RESİM URL'])
    for i in aranan_list:
        record = dict(i)
        writer.writerow([record.get("adSoyad"), record.get("dogumYeri"), record.get("dogumTarihi"), record.get("orgut"),
                         record.get('kategori'), record.get('resim')])
