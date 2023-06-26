from config import app
from flask import jsonify, request
from datetime import datetime, timedelta
from models import MarketData


@app.route("/market_data", methods=["GET"])
def get_market_data() -> tuple:
    date_str = request.args.get("date")
    if not date_str:
        return jsonify({"error": "Date parameter is missing"}), 400

    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        next_day = date + timedelta(days=1)
        market_data = MarketData.query.filter(
            MarketData.date >= date, MarketData.date < next_day
        ).all()
        data = [
            {
                "date": data.date.strftime("%Y-%m-%d %H:%M:%S").split()[0],
                "hour": data.hour,
                "price": data.price,
                "volume": data.volume,
            }
            for data in market_data
        ]
        return jsonify(data), 200
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400


if __name__ == "__main__":
    app.run()
