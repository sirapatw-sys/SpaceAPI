import argparse
from fetchers import fetch_apod, fetch_mars
from dashboard import serve

parser = argparse.ArgumentParser(description="NASA Space News & Astronomy Tracker")
sub = parser.add_subparsers(dest="cmd", required=True)

# fetch-apod
apod_parser = sub.add_parser("fetch-apod", help="Fetch NASA APOD")
apod_parser.add_argument("--date", type=str, help="วันที่ในรูปแบบ YYYY-MM-DD")

# fetch-mars
mars_parser = sub.add_parser("fetch-mars", help="Fetch latest Mars rover photos")
mars_parser.add_argument("--date", type=str, help="วันที่ในรูปแบบ YYYY-MM-DD")

# serve
sub.add_parser("serve", help="Serve Flask gallery")

args = parser.parse_args()

if args.cmd == "fetch-apod":
    fetch_apod(date=args.date)
elif args.cmd == "fetch-mars":
    fetch_mars(date=args.date)
elif args.cmd == "serve":
    serve()
