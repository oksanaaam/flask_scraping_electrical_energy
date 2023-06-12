import time
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from config import app, db
from models import MarketData


def collect_market_data():
    with app.app_context():
        db.create_all()

        url = "https://www.oree.com.ua/index.php/control/results_mo/DAM"

        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)

        driver.get(url)

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
            for row in rows[1:]:
                cells = row.find_all("td")
                if len(cells) >= 7:
                    hour = int(cells[1].text.strip())
                    price = float(cells[2].text.strip())
                    volume = float(cells[3].text.strip())

                    market_data = MarketData(
                        date=date, hour=hour, price=price, volume=volume
                    )

                    db.session.add(market_data)
                    db.session.commit()
        else:
            print("Unable to find table on the page")
