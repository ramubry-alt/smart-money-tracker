from wallets import WALLETS_5, TOP_25
from consensus import get_top_consensus
from report import build_report
from emailer import send_email


def main():

    five, top25 = get_top_consensus(
        WALLETS_5,
        TOP_25
    )

    report = build_report(five, top25)

    send_email(
        subject="Smart Money Intelligence Report",
        body=report
    )


if __name__ == "__main__":
    main()
