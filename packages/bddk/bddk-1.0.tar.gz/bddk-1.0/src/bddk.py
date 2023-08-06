import os
import platform
import tarfile
import time
import urllib.request
import warnings

import io
import pandas as pd
import requests
import openpyxl
import zipfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
try:
    import xlrd
except ModuleNotFoundError:
    pass

def get_download_path():
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'Downloads')


if platform.system() == "Windows":
    uzanti = ".exe"
elif platform.system() == "Linux":
    uzanti = ""
elif platform.system() == "Darwin":
    uzanti = ""


def firefox():
    if platform.system() == "Windows":
        if not os.path.isfile(os.path.join(get_download_path(), "geckodriver" + uzanti)):
            r = requests.get(
                "https://github.com/mozilla/geckodriver/releases/download/v0.28.0/geckodriver-v0.28.0-win64.zip")
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall(get_download_path())
    elif platform.system() == "Linux":
        if not os.path.isfile(os.path.join(get_download_path(), "geckodriver" + uzanti)):
            thetarfile = "https://github.com/mozilla/geckodriver/releases/download/v0.28.0/geckodriver-v0.28.0-linux64.tar.gz"
            ftpstream = urllib.request.urlopen(thetarfile)
            thetarfile = tarfile.open(fileobj=ftpstream, mode="r|gz")
            thetarfile.extractall(get_download_path())
    elif platform.system() == "Darwin":
        if not os.path.isfile(os.path.join(get_download_path(), "geckodriver" + uzanti)):
            thetarfile = "https://github.com/mozilla/geckodriver/releases/download/v0.28.0/geckodriver-v0.28.0-macos.tar.gz"
            ftpstream = urllib.request.urlopen(thetarfile)
            thetarfile = tarfile.open(fileobj=ftpstream, mode="r|gz")
            thetarfile.extractall(get_download_path())

    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.dir", get_download_path())
    profile.set_preference("browser.helperApps.alwaysAsk.force", False)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.manager.showAlertOnComplete", False)
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/ms-excel')
    options = webdriver.FirefoxOptions()
    options.set_preference("dom.webnotifications.serviceworker.enabled", False)
    options.set_preference("dom.webnotifications.enabled", False)
    options.add_argument('--headless')
    driver_path = os.path.join(get_download_path(), "geckodriver" + uzanti)
    driver = webdriver.Firefox(executable_path=driver_path, firefox_profile=profile, options=options)
    return driver


def chrome():
    if not os.path.isfile(os.path.join(get_download_path(), "chromedriver" + uzanti)):
        if platform.system() == "Windows":
            r = requests.get("https://chromedriver.storage.googleapis.com/87.0.4280.88/chromedriver_win32.zip")
        elif platform.system() == "Linux":
            r = requests.get("https://chromedriver.storage.googleapis.com/87.0.4280.88/chromedriver_linux64.zip")
        elif platform.system() == "Darwin":
            r = requests.get("https://chromedriver.storage.googleapis.com/87.0.4280.88/chromedriver_mac64.zip")
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(get_download_path())

    if platform.system() == "Linux":
        os.chmod(os.path.join(get_download_path(), "chromedriver" + uzanti), 0o755)
    if platform.system() == "Darwin":
        os.chmod(os.path.join(get_download_path(), "chromedriver" + uzanti), 0o755)

    chromeoptions = webdriver.ChromeOptions()
    prefs = {'download.prompt_for_download': False,
             'download.default_directory': get_download_path(),
             'download.directory_upgrage': True,
             'profile.default_content_settings.popups': 0,
             }
    chromeoptions.add_experimental_option('prefs', prefs)
    chromeoptions.headless = True
    driver_path = os.path.join(get_download_path(), "chromedriver" + uzanti)
    driver = webdriver.Chrome(executable_path=driver_path, chrome_options=chromeoptions)
    return driver


def get_kalem(kalems=None, browser="firefox"):
    if browser == "firefox":
        driver = firefox()
    if browser == "chrome":
        driver = chrome()
    driver.get("https://www.bddk.org.tr/BultenAylik/tr/Home/Gelismis")
    driver.find_element_by_id("ddlTabloKalem_chosen").click()
    html_list = driver.find_element_by_id("ddlTabloKalem_chosen")
    items = html_list.find_elements_by_tag_name("li")
    if kalems is None:
        for item in items:
            print(item.text)
    else:
        for item in items:
            if kalems.lower() in item.text.lower():
                print(item.text)
    driver.quit()


def get_taraf(browser="firefox"):
    if browser == "firefox":
        driver = firefox()
    if browser == "chrome":
        driver = chrome()
    driver.get("https://www.bddk.org.tr/BultenAylik/tr/Home/Gelismis")
    driver.find_element_by_id("ddlTaraf_chosen").click()
    html_list = driver.find_element_by_id("ddlTaraf_chosen")
    items = html_list.find_elements_by_tag_name("li")
    for item in items:
        print(item.text)
    driver.quit()


def get_rapor(kalem, basyil, basay, bityil, bitay, per, para="TL", taraf=None, zaman=120, browser="firefox"):
    if browser == "firefox":
        driver = firefox()
    if browser == "chrome":
        driver = chrome()
    print("Yukleniyor...")
    driver.get("https://www.bddk.org.tr/BultenAylik/tr/Home/Gelismis")

    # Rapor temizleme
    if os.path.isfile(os.path.join(get_download_path(), 'Rapor.xlsx')):
        os.remove(os.path.join(get_download_path(), 'Rapor.xlsx'))

    # Baslangic yil
    driver.find_element_by_id("ddlBaslangicYil_chosen").click()
    html_list = driver.find_element_by_id("ddlBaslangicYil_chosen")
    items = html_list.find_elements_by_tag_name("li")
    text = []
    for item in items:
        text.append(item.text)
    items[text.index(str(basyil))].click()

    # Bitis yil
    driver.find_element_by_id("ddlBitisYil_chosen").click()
    html_list = driver.find_element_by_id("ddlBitisYil_chosen")
    items = html_list.find_elements_by_tag_name("li")
    text = []
    for item in items:
        text.append(item.text)
    items[text.index(str(bityil))].click()

    # Baslangic ay
    driver.find_element_by_id("ddlBaslangicAy_chosen").click()
    html_list = driver.find_element_by_id("ddlBaslangicAy_chosen")
    items = html_list.find_elements_by_tag_name("li")
    text = []
    for item in items:
        text.append(item.text)
    items[text.index(str(basay))].click()

    # Bitis ay
    driver.find_element_by_id("ddlBitisAy_chosen").click()
    html_list = driver.find_element_by_id("ddlBitisAy_chosen")
    items = html_list.find_elements_by_tag_name("li")
    text = []
    for item in items:
        text.append(item.text)
    items[text.index(str(bitay))].click()

    # Periyot
    driver.find_element_by_id("ddlPeriyot_chosen").click()
    html_list = driver.find_element_by_id("ddlPeriyot_chosen")
    items = html_list.find_elements_by_tag_name("li")
    text = []
    for item in items:
        text.append(item.text)
    items[text.index(str(per))].click()

    # Para Birimi
    driver.find_element_by_id("ddlParaBirimi_chosen").click()
    html_list = driver.find_element_by_id("ddlParaBirimi_chosen")
    items = html_list.find_elements_by_tag_name("li")
    text = []
    for item in items:
        text.append(item.text)
    items[text.index(str(para))].click()

    # Kalem
    for i, kal in enumerate(kalem):
        driver.find_element_by_id("ddlTabloKalem_chosen").click()
        html_list = driver.find_element_by_id("ddlTabloKalem_chosen")
        items = html_list.find_elements_by_tag_name("li")
        if kal == kalem[0]:
            text = []
            for item in items:
                text.append(item.text)
        items[text.index(str(kal))+i].click()

    # taraf
    if taraf is not None:
        for j, tar in enumerate(taraf):
            driver.find_element_by_id("ddlTaraf_chosen").click()
            html_list = driver.find_element_by_id("ddlTaraf_chosen")
            items = html_list.find_elements_by_tag_name("li")
            if tar == taraf[0]:
                text = []
                for item in items:
                    text.append(item.text)
            items[text.index(str(tar))+j].click()

    # rapor
    driver.find_element_by_id("btnRaporOlustur").click()

    # Excel
    WebDriverWait(driver, zaman).until(EC.element_to_be_clickable((By.ID, "btnExcel")))
    driver.find_element_by_id("btnExcel").click()

    # csv
    warnings.filterwarnings("ignore", category=UserWarning)
    enginexlrd = 0
    try:
        if xlrd.__version__ < "2.0":
            enginexlrd = 1
    except NameError:
        pass
    ilk_zaman = 0
    if enginexlrd == 0:
        while ilk_zaman < zaman:
            time.sleep(1)
            if os.path.isfile(os.path.join(get_download_path(), 'Rapor.xlsx')):
                sonuc = pd.read_excel(os.path.join(get_download_path(), 'Rapor.xlsx'), engine="openpyxl")
                break
            ilk_zaman += ilk_zaman
    elif enginexlrd == 1:
        while ilk_zaman < zaman:
            time.sleep(1)
            if os.path.isfile(os.path.join(get_download_path(), 'Rapor.xlsx')):
                sonuc = pd.read_excel(os.path.join(get_download_path(), 'Rapor.xlsx'))
                break
            ilk_zaman += ilk_zaman
    print("Veri alindi.")
    driver.quit()
    os.remove(os.path.join(get_download_path(), 'Rapor.xlsx'))
    return sonuc
