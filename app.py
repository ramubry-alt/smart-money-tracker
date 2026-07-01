from wallets import WALLETS_5, TOP_25
from consensus import get_top_consensus
from emailer import send_email


def format_report(five, top25):
    lines = []

    lines.append("SMART MONEY DAILY REPORT\n")

    lines.append("⭐⭐⭐⭐⭐ 5-WALLET CONSENSUS\n")

    for m in five[:10]:
        if m["strength"] == 100:
            lines.append(f"{m['market']} → {m['direction']} ({m['total_size']}$)")

    lines.append("\n⭐⭐⭐⭐ TOP 25 CONSENSUS\n")

    for m in top25[:15]:
        if m["strength"] >= 70:
            lines.append(f"{m['market']} → {m['direction']} ({m['strength']}%)")

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
if __name__ == "__main__":
    print("Running Smart Money Tracker...")

    result = get_top_consensus()

    print("Consensus result:")
    print(result)
