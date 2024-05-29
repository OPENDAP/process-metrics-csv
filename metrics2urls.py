#!/usr/bin/env python3

# Extract URLs from CSV files downloaded from the NGAP metrics system

import pandas as pd
import json


def extract_url(json_string):
    data = json.loads(json_string)
    return data.get("hyrax_app_message").split("url: ")[1].split(")")[0]


def clean_url(url):
    return url.split("attempt: ")[0]


def print_urls(csv_file: str, only_urls: bool):
    df = pd.read_csv(csv_file, delimiter=",", quotechar='"')

    tmp = df["@timestamp"].str.split("@")

    df["timestamp"] = pd.to_datetime(tmp.str[0] + " " + tmp.str[1])

    df["url"] = df["message"].apply(extract_url)

    df["url"] = df["url"].apply(clean_url)

    # Here's how to format the output:
    if only_urls:
        for index, row in df.iterrows():
            print(f"{row['url']}")
    else:
        for index, row in df.iterrows():
            print(f"Timestamp: {row['timestamp']}, URL: {row['url']}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Process CSV files downloaded from the NGAP Global metrics system. "
                                                 "The files are assumed to have two columns, the (weird) date and the"
                                                 "OPeNDAP Application Message, which is a JSON document with a dog pile"
                                                 "of information.")
    parser.add_argument("-u", "--urls", help="Only print the URLs", action="store_true")
    # When name_or_flags does not have a leading - or --, it is an optional positional argument
    parser.add_argument("file", help="Parse this CSV file (each line is: <date>, <JSON>)", type=str)
    args = parser.parse_args()
    if args.file is None:
        print(args)
        exit(1)

    print_urls(args.file, args.urls)


if __name__ == '__main__':
    main()
