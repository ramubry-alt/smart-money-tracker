from datetime import datetime


def build_report(five, top25):
    lines = []

    today = datetime.now().strftime("%A, %B %d, %Y")

    lines.append("SMART MONEY INTELLIGENCE REPORT")
    lines.append(today)
    lines.append("")

    lines.append("════════════════════════════════════")
    lines.append("")
    lines.append("🔥 NEW SINCE YESTERDAY")
    lines.append("")
    lines.append("No changes tracked yet.")
    lines.append("")

    lines.append("════════════════════════════════════")
    lines.append("")
    lines.append("⭐⭐⭐⭐⭐ ELITE CONSENSUS (Top 5 Wallets)")
    lines.append("")

    for i, m in enumerate(five[:10], start=1):
        lines.append(f"{i}. {m['market']}")
        lines.append(f"   Pick: {m['direction']}")
        lines.append(
            f"   Agreement: {m['wallet_count']}/5 ({m['strength']}%)"
        )

        if "volume" in m:
            lines.append(f"   Volume: ${m['volume']:,.2f}")

        lines.append("")

    lines.append("════════════════════════════════════")
    lines.append("")
    lines.append("⭐⭐⭐⭐ BROADER CONSENSUS (Top 25 Wallets)")
    lines.append("")

    for i, m in enumerate(top25[:10], start=1):
        lines.append(f"{i}. {m['market']}")
        lines.append(f"   Pick: {m['direction']}")
        lines.append(
            f"   Agreement: {m['wallet_count']}/25 ({m['strength']}%)"
        )

        if "volume" in m:
            lines.append(f"   Volume: ${m['volume']:,.2f}")

        lines.append("")

    return "\n".join(lines)
