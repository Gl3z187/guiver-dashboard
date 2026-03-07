from flask import Flask, render_template, request, redirect, url_for
from database import init_db, get_all_trades, add_trade, delete_trade
from metrics import calculate_summary, performance_by_group, winrate_by_pair

app = Flask(__name__)
init_db()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/resumen")
def index():
    trades = get_all_trades()
    summary = calculate_summary(trades)
    return render_template("index.html", trades=trades, summary=summary)


@app.route("/trades", methods=["GET", "POST"])
def trades():
    if request.method == "POST":
        open_date = request.form["open_date"]
        close_date = request.form["close_date"]
        pair = request.form["pair"]
        direction = request.form["direction"]
        narrative = request.form["narrative"]
        setup_type = request.form["setup_type"]
        result_r = float(request.form["result_r"])
        notes = request.form["notes"]
        reflection = request.form["reflection"]

        add_trade(
            open_date,
            close_date,
            pair,
            direction,
            narrative,
            setup_type,
            result_r,
            notes,
            reflection
        )
        return redirect(url_for("trades"))

    all_trades = get_all_trades()
    return render_template("trades.html", trades=all_trades)


@app.route("/delete/<int:trade_id>")
def delete(trade_id):
    delete_trade(trade_id)
    return redirect(url_for("trades"))


@app.route("/estadisticas")
def performance():
    trades = get_all_trades()
    by_setup = performance_by_group(trades, "setup_type")
    pair_winrates = winrate_by_pair(trades)

    return render_template(
        "performance.html",
        by_setup=by_setup,
        pair_winrates=pair_winrates
    )

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)