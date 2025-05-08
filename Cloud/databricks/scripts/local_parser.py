import csv
import argparse
import re

def parse_line(line):
    """
    Parse a single log line into its components.
    Returns a dict with keys:
    - month:   Syslog month (e.g., "Feb")
    - day:     Syslog day (e.g., "1")
    - time:    Syslog time (e.g., "12:50:02")
    - host:    Hostname (e.g., "wardcs")
    - process: Process name (e.g., "logger")
    - log_date:  ISO date from the message (e.g., "2015-02-01")
    - log_time:  Time from the message (e.g., "12:50:02")
    - message:   The remainder of the message text
    """
    parts = line.strip().split(maxsplit=4)
    if len(parts) < 5:
        return None

    month, day, timestr, host, rest = parts
    # Split "process:" and the remainder
    process_field, message = rest.split(None, 1)
    process = process_field.rstrip(':')

    # Attempt to extract an ISO timestamp at start of message
    msg_parts = message.split(maxsplit=2)
    if len(msg_parts) >= 3 and re.match(r'\d{4}-\d{2}-\d{2}', msg_parts[0]):
        log_date, log_time, msg_text = msg_parts
    else:
        log_date = ''
        log_time = ''
        msg_text = message

    return {
        'month': month,
        'day': day,
        'time': timestr,
        'host': host,
        'process': process,
        'log_date': log_date,
        'log_time': log_time,
        'message': msg_text
    }

def main():
    parser = argparse.ArgumentParser(description="Parse a log file and export to CSV.")
    parser.add_argument('input_file', help="Path to the input log file")
    parser.add_argument('output_file', help="Path to the output CSV file")
    args = parser.parse_args()

    fieldnames = ['month', 'day', 'time', 'host', 'process', 'log_date', 'log_time', 'message']

    with open(args.input_file, 'r') as infile, \
         open(args.output_file, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for line in infile:
            row = parse_line(line)
            if row:
                writer.writerow(row)

if __name__ == '__main__':
    main()

