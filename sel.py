import time
from saaparse import parse_FMI, parse_Windy, parse_Foreca, parse_Wind_guru

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


def hae_Wind_guru(driver, tulos):
    driver.get("https://www.windguru.cz/widget-fcst-iframe.php?s=743066&m=100&uid=wg_fwdg_743066_100_1613903582313&wj"
               "=msd&tj=c&waj=m&odh=9&doh=18&fhours=24&hrsm=3&vt=forecasts&lng=fi&idbs=1&p=WINDSPD,GUST,SMER,TMPE,"
               "FLHGT,CDC,TCDC,APCP1s")
    WebDriverWait(driver, 20).until(
        # ec.visibility_of_element_located((By.CSS_SELECTOR, 'tr.td-windCombined'))
        ec.visibility_of_all_elements_located((By.CSS_SELECTOR, "#wgtab-obal-tabid_0"))
    )
    document_content = driver.page_source
    parse_Wind_guru(document_content, tulos)


def hae_Foreca(driver, tulos):
    driver.get("https://www.foreca.fi/Finland/Joutsa/Leivonmaki/details")
    WebDriverWait(driver, 20).until(
        # ec.visibility_of_element_located((By.CSS_SELECTOR, 'tr.td-windCombined'))
        ec.visibility_of_all_elements_located((By.CSS_SELECTOR, "#hourly_wrap"))
    )
    document_content = driver.page_source
    parse_Foreca(document_content, tulos)


def hae_FMI(driver, tulos):
    driver.get("https://www.ilmatieteenlaitos.fi/saa/joutsa/leivonm%C3%A4ki?forecast=short")
    WebDriverWait(driver, 20).until(
        # ec.visibility_of_element_located((By.CSS_SELECTOR, 'tr.td-windCombined'))
        ec.visibility_of_all_elements_located((By.CSS_SELECTOR, '#day-header-0'))
    )
    document_content = driver.page_source
    parse_FMI(document_content, tulos)


def hae_Windy(driver, tulos):
    driver.get('https://www.windy.com/61.890/26.197/wind?61.608,26.197,8,m:fojagSO')
    # Odota, että tietty elementti tulee näkyviin

    WebDriverWait(driver, 20).until(
        ec.visibility_of_all_elements_located((By.CSS_SELECTOR,
                                               'span.legend-right.metric-clickable'))
    )

    time.sleep(1)
    # Etsi elementti ja klikkaa sitä
    element = driver.find_element(By.CSS_SELECTOR,
                                  'span.legend-right.metric-clickable')
    element.click()
    element.click()

    # allow_button = WebDriverWait(driver, 10).until(
    #     ec.visibility_of_element_located((By.XPATH,
    #                                      "//div[@class='button size-xl' and text()='Allow anonymous analytics']"))
    # )
    # allow_button.click()
    time.sleep(1)

    driver.save_screenshot("sele.png")

    document_content = driver.page_source
    parse_Windy(document_content, tulos)


def main():
    tulos = [["" for _ in range(17)] for _ in range(4)]

    chrome_options = Options()
    chrome_options.add_argument("--lang=fi")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--use-fake-ui-for-media-stream")
    # chrome_options.add_argument("--blink-settings=timezoneId=Europe/Helsinki")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=500,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 " +
                                "(Windows NT 10.0; Win64; x64) " +
                                "AppleWebKit/537.36 (KHTML, like Gecko) " +
                                "Chrome/91.0.4472.124 Safari/537.36")

    # Aseta WebDriverin polku
    service = Service('chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    hae_FMI(driver, tulos)
    hae_Foreca(driver, tulos)
    hae_Wind_guru(driver, tulos)
    hae_Windy(driver, tulos)

    for rivi in tulos:
        print("\t".join(rivi))

    # Pidä selain auki, kunnes painat Enter-näppäintä
    # input("Paina Enter sulkeaksesi selaimen...")
    # Sulje selain
    driver.close()
    # driver.quit()


if __name__ == "__main__":
    main()
