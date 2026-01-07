import argparse
import time
import os
import traceback
from datetime import datetime
from instagrapi import Client

# --- Configuration ---
USERNAME = ''
PASSWORD = ''
TWO_FACTOR = ''
SESSION_FILE = "session.json"


def get_client():
    cl = Client()
    if os.path.exists(SESSION_FILE):
        cl.load_settings(SESSION_FILE)
        try:
            cl.get_timeline_feed()  # Test if session is still valid
        except:
            cl.login(USERNAME, PASSWORD, verification_code=TWO_FACTOR)
            cl.dump_settings(SESSION_FILE)
    else:
        cl.login(USERNAME, PASSWORD, verification_code=TWO_FACTOR)
        cl.dump_settings(SESSION_FILE)
    return cl


def calculate_values(target_dt, mode):
    now = datetime.now()
    if mode == 'c':
        diff = target_dt - now
    else:
        diff = now - target_dt

    seconds = diff.total_seconds()

    # Logic for time units
    return {
        'd': int(seconds // 86400),
        'h': int(seconds // 3600),
        'm': int(seconds // 60),
        'w': int(seconds // 604800),
        'mo': int(seconds // 2592000)  # Approx 30 days
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=['c', 'ds'], help="c for countdown, ds for days since")
    parser.add_argument("date", help="Format: DD/MM/YYYY")
    parser.add_argument("time", help="Format: HH:MM")
    parser.add_argument("message", help="Message with placeholders like {d}, {h}, {m}, {w}, {mo}")

    args = parser.parse_args()
    target_str = f"{args.date} {args.time}"
    target_dt = datetime.strptime(target_str, "%d/%m/%Y %H:%M")

    cl = get_client()

    while True:
        try:
            vals = calculate_values(target_dt, args.mode)

            # Format the user's message using the dictionary
            # .format(**vals) maps {d} to vals['d'], etc.
            # eval(args.message)
            formatted_note = args.message.format(**vals)

            # Instagram Notes have a 60-character limit
            final_note = formatted_note[:60]

            print(f"Updating Note: {final_note}")
            cl.create_note(final_note, audience=0)

            time.sleep(60)

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()
            time.sleep(60)


if __name__ == "__main__":
    main()