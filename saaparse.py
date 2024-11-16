import re
from bs4 import BeautifulSoup


def parse_Wind_guru(document_content, tulos):
    soup = BeautifulSoup(document_content, 'html.parser')
    table = soup.find('table', class_='tabulka')
    kello = ["08h", "09h", "11h", "12h", "14h", "15h", "17h", "18h"]
    indesies = [-2 for _ in range(50)]
    if table:
        number_in_parentheses = re.compile(r'\((\d+)°\)')
        # Käydään taulukon rivit läpi
        rows = table.find_all('tr')

        time_row = rows[0]
        ws_row = rows[1]
        wg_row = rows[2]
        dir_row = rows[3]

        # Selvitä ajat
        cells = time_row.find_all(['td', 'th'])
        cols = 4

        for cn in range(len(cells)):
            cell = cells[cn]
            text = cell.get_text(strip=True)
            # print(text)
            paikka = -1
            for i, aika in enumerate(kello):
                if aika in text:
                    paikka = i // 2
                    indesies[cn] = paikka
                    break
            if paikka == 0 and cn > 0:
                cols = cn
                break

        # nopeudet
        cells = ws_row.find_all(['td'])
        for i in range(cols):
            tulos[indesies[i]][7] = cells[i].get_text(strip=True)

        # puuskat
        cells = wg_row.find_all(['td'])
        for i in range(cols):
            tulos[indesies[i]][8] = cells[i].get_text(strip=True)

        # suunnat
        cells = dir_row.find_all(['td'])
        for i in range(cols):
            # Etsi title-attribuutti span-elementistä
            span = cells[i].find('span', title=True)
            if not span:
                continue
            title_text = span['title']
            # Etsi numero suluissa title-tekstistä
            suunta_match = number_in_parentheses.search(title_text)
            if suunta_match:
                suunta = suunta_match.group(1)
                tulos[indesies[i]][0] = suunta
    else:
        print("Taulukkoa, jolla class='tabulka' ei löytynyt.")


def parse_Foreca(document_content, tulos):
    soup = BeautifulSoup(document_content, 'html.parser')
    rows = soup.find_all('div', class_='row_wrap')
    kello = ["09", "12", "15", "18"]
    for row in rows:
        # Etsi h, ws ja wg-arvot
        h = row.select_one('.h p').get_text(strip=True) if row.select_one('.h p') else None
        ws = row.select_one('.ws').get_text(strip=True) if row.select_one('.ws') else None
        wg = row.select_one('.wg').get_text(strip=True) if row.select_one('.wg') else None

        if not h:
            continue
        h = h.split(".")[0]  # Ota vain ennen pistettä oleva osa
        if wg:
            wg = wg.strip("()")  # Poista sulut
        try:
            index = kello.index(h)
            tulos[index][5] = ws
            tulos[index][6] = wg
        except ValueError:
            pass


def parse_FMI(document_content, tulos):
    soup = BeautifulSoup(document_content, 'html.parser')
    table = soup.find('table', class_='hourly-table')
    kello = ["09", "12", "15", "18"]
    if table:
        rows = table.find_all('tr')
        # rows = page.query_selector_all('tr')
        for row in rows:
            th_element = row.find(class_='hourly-table-hour')
            if not th_element:
                continue
            time_element = th_element.find('span')
            if not time_element:
                continue
            h = time_element.contents[0].split(':')[0]
            try:
                index = kello.index(h)
            except ValueError:
                continue

            wind_td = row.find(class_='wind')
            if not wind_td:
                continue
            wind_elements = row.find(class_='wind').contents[0].contents[2].contents
            if len(wind_elements) < 2:
                continue
            ws = wind_elements[0].contents[0].strip()  # Tuuliväriarvo (esim. "5")
            wg = wind_elements[2].contents[0].strip().replace('(', '').replace(')', '')
            # print(f'{time} Tuuli: {ws} {wg}')
            tulos[index][3] = ws
            tulos[index][4] = wg

    else:
        print("FMI: Taulukkoa, jolla class='hourly-table' ei löytynyt.")


def parse_Windy(document_content, tulos):
    soup = BeautifulSoup(document_content, 'html.parser')
    table = soup.find(id='detail-data-table')
    row = table.find('tr', class_='td-hour')
    times = row.find_all('td')
    indesies = [-2 for _ in range(50)]
    kello = ['8', '9', '11', '12', '14', '15', '17', '18']
    for i in range(len(times)):
        h = times[i].text
        if int(h) > 18:
            break
        try:
            index = kello.index(h) // 2
            indesies[i] = index
        except ValueError:
            indesies[i] = -1
            continue

    rows = table.find_all('tr', class_='td-windCombined')
    for cn in range(len(rows)):
        row = rows[cn]
        cells = row.find_all('td')
        for i in range(len(cells)):
            cell = cells[i]
            index = indesies[i]
            # print(i, index, cell.text)
            if index < -1:
                break
            if index < 0:
                continue
            mul = 1  # 0.514444
            ws = int(cell.contents[1].strip()) * mul
            wg = int(cell.find('small').text.strip()) * mul
            tulos[index][2 * cn + 9] = f"{ws:.0f}"
            tulos[index][2 * cn + 10] = f"{wg:.0f}"
    return
