def calculate_summary(trades):
    if not trades:
        return {
            "num_trades": 0,
            "total_r": 0,
            "win_rate": 0,
            "avg_win": 0,
            "avg_loss": 0,
            "profit_factor": 0
        }

    results = [t["result_r"] for t in trades]

    wins = [r for r in results if r > 0]
    losses = [r for r in results if r < 0]

    num_trades = len(results)
    total_r = sum(results)
    win_rate = (len(wins) / num_trades * 100) if num_trades > 0 else 0
    avg_win = sum(wins) / len(wins) if wins else 0
    avg_loss = sum(losses) / len(losses) if losses else 0

    gross_profit = sum(wins) if wins else 0
    gross_loss = abs(sum(losses)) if losses else 0
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0

    return {
        "num_trades": num_trades,
        "total_r": round(total_r, 2),
        "win_rate": round(win_rate, 2),
        "avg_win": round(avg_win, 2),
        "avg_loss": round(avg_loss, 2),
        "profit_factor": round(profit_factor, 2)
    }


def performance_by_group(trades, key):
    groups = {}

    for trade in trades:
        group_value = trade[key]
        if group_value not in groups:
            groups[group_value] = {"count": 0, "total_r": 0}

        groups[group_value]["count"] += 1
        groups[group_value]["total_r"] += trade["result_r"]

    result = []
    for name, values in groups.items():
        avg_r = values["total_r"] / values["count"] if values["count"] else 0
        result.append({
            "name": name,
            "count": values["count"],
            "total_r": round(values["total_r"], 2),
            "avg_r": round(avg_r, 2)
        })

    result.sort(key=lambda x: x["total_r"], reverse=True)
    return result


def winrate_by_pair(trades):
    groups = {}

    for trade in trades:
        pair = trade["pair"]
        if pair not in groups:
            groups[pair] = {"trades": 0, "wins": 0, "total_r": 0}

        groups[pair]["trades"] += 1
        groups[pair]["total_r"] += trade["result_r"]

        if trade["result_r"] > 0:
            groups[pair]["wins"] += 1

    result = []
    for pair, values in groups.items():
        trades_count = values["trades"]
        wins = values["wins"]
        winrate = (wins / trades_count * 100) if trades_count > 0 else 0

        result.append({
            "pair": pair,
            "trades": trades_count,
            "wins": wins,
            "winrate": round(winrate, 2),
            "total_r": round(values["total_r"], 2)
        })

    result.sort(key=lambda x: x["winrate"], reverse=True)
    return result