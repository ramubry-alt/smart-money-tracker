from wallets import WALLETS_5, TOP_25
from consensus import get_top_consensus
from emailer import send_email


def format_report(five, top25):
    lines = []

    lines.append("SMART MONEY DAILY REPORT\n")

    lines.append("🔥 NEW SINCE YESTERDAY\n")
    lines.append("No changes tracked in this version.\n")

    # Merge both lists and keep only the strongest version of each market
    unique = {}

    for signal in five + top25:
        market = signal["market"]

        if (
            market not in unique
            or signal["strength"] > unique[market]["strength"]
        ):
            unique[market] = signal

    all_signals = list(unique.values())
    all_signals.sort(key=lambda x: x["strength"], reverse=True)

    top5 = all_signals[:5]

    lines.append("⭐⭐⭐⭐⭐ TOP 5 CONVICTION SIGNALS\n")

    for m in top5:
        lines.append(
            f"{m['market']} → {m['direction']} ({m['strength']}%)"
        )

    return "\n".join(lines)


def main():
    five, top25 = get_top_consensus(WALLETS_5, TOP_25)

    report = format_report(five, top25)

    send_email(
        subject="Smart Money Daily Report",
        body=report
    )


if __name__ == "__main__":
    main()
