from wallets import WALLETS_5, TOP_25
from consensus import get_top_consensus
from emailer import send_email


def format_report(five, top25):
    lines = []

    lines.append("SMART MONEY DAILY REPORT\n")

    lines.append("🔥 NEW SINCE YESTERDAY\n")
    lines.append("No changes tracked in this version.\n")

    lines.append("⭐⭐⭐⭐⭐ 5-WALLET CONSENSUS\n")

    for m in five[:10]:
        if m["strength"] >= 80:
            lines.append(f"{m['market']} → {m['direction']} ({m['yes_count']}/5 wallets)")

    lines.append("\n⭐⭐⭐⭐ TOP 25 CONSENSUS\n")

    for m in top25[:15]:
        if m["strength"] >= 60:
            lines.append(f"{m['market']} → {m['direction']} ({m['yes_count']}/25 wallets)")

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
