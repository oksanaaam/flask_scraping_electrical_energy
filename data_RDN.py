import time
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from config import app, db
from models import MarketData

URL = "https://www.oree.com.ua/index.php/control/results_mo/DAM"


def collect_market_data() -> None:
    with app.app_context():
        db.create_all()

        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)

        driver.get(URL)

        button = driver.find_element(
            By.XPATH, '//div[contains(text(), "Погодинні результати на РДН")]'
        )
        button.click()

        time.sleep(3)

        html = driver.page_source

        driver.quit()

        soup = BeautifulSoup(html, "html.parser")

        date_str = soup.find("input", {"id": "date_pxs"}).get("value")
        date = datetime.strptime(date_str, "%d.%m.%Y").date()

        table = soup.find("table", class_="site-table")
        if table:
            rows = table.find_all("tr")
            market_data_list = []
            for row in rows[1:]:
                cells = row.find_all("td")
                if len(cells) >= 7:
                    hour = int(cells[1].text.strip())
                    price = float(cells[2].text.strip())
                    volume = float(cells[3].text.strip())

                    market_data = MarketData(
                        date=date, hour=hour, price=price, volume=volume
                    )

                    market_data_list.append(market_data)

            db.session.add_all(market_data_list)
            db.session.commit()
        else:
            print("Unable to find table on the page")
