from saaparse import parse_FMI, parse_Windy, parse_Foreca, parse_Wind_guru
from rasp import hae_rasp

from playwright.sync_api import sync_playwright


def hae_Wind_guru(browser, tulos):
    page = browser.new_page()
    page.goto("https://www.windguru.cz/widget-fcst-iframe.php?s=743066&m=100&uid=wg_fwdg_743066_100_1613903582313&wj"
              "=msd&tj=c&waj=m&odh=9&doh=18&fhours=24&hrsm=3&vt=forecasts&lng=fi&idbs=1&p=WINDSPD,GUST,SMER,TMPE,"
              "FLHGT,CDC,TCDC,APCP1s")
    page.wait_for_selector("#wgtab-obal-tabid_0") 
    document_content = page.content()  # Saa koko HTML-sisällön
    parse_Wind_guru(document_content, tulos)


def hae_Foreca(browser, tulos):
    page = browser.new_page()
    page.goto("https://www.foreca.fi/Finland/Joutsa/Leivonmaki/details")
    page.wait_for_selector("#hourly_wrap")
    document_content = page.content()  # Saa koko HTML-sisällön
    parse_Foreca(document_content, tulos)


def hae_FMI(browser, tulos):
    page = browser.new_page()
    page.set_viewport_size({"width": 375, "height": 667})
    page.goto("https://www.ilmatieteenlaitos.fi/saa/joutsa/leivonm%C3%A4ki?forecast=short")
    page.wait_for_selector("#day-header-0")
    document_content = page.content()  # Saa koko HTML-sisällön
    parse_FMI(document_content, tulos)


def hae_Windy(browser, tulos):
    """
    Haetaan Windyn tuulet
    :param browser: selain jolta tietoja haetaan
    :param tulos: taulukko jonne tulokset laitetaan
    """
    page = browser.new_page()
    page.goto("https://www.windy.com/61.890/26.197/wind?61.608,26.197,8,m:fojagSO")
    # page.wait_for_selector("#detail-data-table")
    page.wait_for_load_state('networkidle')  # Odottaa, kunnes kaikki verkon pyynnöt ovat valmiit
    # page.reload()
    # page.wait_for_load_state('networkidle')  # Odottaa, kunnes kaikki verkon pyynnöt ovat valmiit
    # element = page.locator('span[data-do="metric,wind"].legend-right.metric-clickable').nth(0)
    element = page.locator('span.legend-right.metric-clickable').nth(0)
    element.click(force=True)
    # page.wait_for_load_state('networkidle')  # Odottaa, kunnes kaikki verkon pyynnöt ovat valmiit
    element.click(force=True)
    # page.wait_for_load_state('networkidle')  # Odottaa, kunnes kaikki verkon pyynnöt ovat valmiit
    # page.wait_for_selector("tr.td-windCombined")
    # time.sleep(2)
    page.wait_for_timeout(1000)
    # page.locator(".td-hour").wait_for()
    page.locator(".tr--hour").wait_for()
    page.screenshot(path='saa.png')
    document_content = page.content()  # Saa koko HTML-sisällön
    parse_Windy(document_content, tulos)


def main():
    with sync_playwright() as p:
        tulos = [["" for _ in range(17)] for _ in range(4)]
        browser = p.chromium.launch(headless=True)
        # context = browser.new_context(timezone_id='Europe/Helsinki')  # Aseta haluamasi aikavyöhyke
        context = browser.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                                                 'AppleWebKit/537.36 (KHTML, like Gecko) ' +
                                                 'Chrome/91.0.4472.124 Safari/537.36')
        hae_Wind_guru(context, tulos)
        hae_Foreca(context, tulos)
        hae_FMI(context, tulos)
        hae_Windy(context, tulos)
        browser.close()
        hae_rasp(tulos)

    for rivi in tulos:
        print("\t".join(rivi))


if __name__ == "__main__":
    main()
