import argparse
from fetchers import fetch_apod, fetch_mars
from dashboard import serve

parser = argparse.ArgumentParser(description="NASA Space News & Astronomy Tracker")
sub = parser.add_subparsers(dest="cmd")

sub.add_parser("fetch-apod", help="Fetch NASA APOD")
sub.add_parser("fetch-mars", help="Fetch latest Mars rover photos")
sub.add_parser("serve", help="Serve Flask gallery")

args = parser.parse_args()

if args.cmd == "fetch-apod":
    fetch_apod()
elif args.cmd == "fetch-mars":
    fetch_mars()
elif args.cmd == "serve":
    serve()
else:
    parser.print_help()
