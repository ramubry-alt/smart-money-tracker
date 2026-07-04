from datetime import datetime


def build_report(five, top25):
    lines = []

    lines.append("SMART MONEY INTELLIGENCE REPORT")
    lines.append(datetime.now().strftime("%A, %B %d, %Y"))
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

    for i, m in enumerate(five, 1):
        lines.append(f"{i}. {m['market']}")
        lines.append(f"   Pick: {m['direction']}")
        lines.append(f"   Agreement: {m['strength']}%")
        lines.append(f"   Volume: ${m['volume']:,}")
        lines.append("")

    lines.append("════════════════════════════════════")
    lines.append("")
    lines.append("⭐⭐⭐⭐ BROADER CONSENSUS (Top 25 Wallets)")
    lines.append("")

    for i, m in enumerate(top25, 1):
        lines.append(f"{i}. {m['market']}")
        lines.append(f"   Pick: {m['direction']}")
        lines.append(f"   Agreement: {m['strength']}%")
        lines.append(f"   Volume: ${m['volume']:,}")
        lines.append("")

    return "\n".join(lines)
