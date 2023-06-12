from data_RDN import collect_market_data
import schedule
import time


def run_collect_market_data():
    collect_market_data()


schedule.every().day.at("12:30").do(run_collect_market_data)


if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
