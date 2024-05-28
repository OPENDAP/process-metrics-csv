#!python3

# Extract URLs from CSV files downloaded from the NGAP metrics system

import pandas as pd
import json


def extract_url(json_string):
  data = json.loads(json_string)
  return data.get("hyrax_app_message").split("url: ")[1].split(")")[0]


def clean_url(url):
  return url.split("attempt: ")[0]


import pandas as pd

# Clean date (choose one method)
# Method 1: Using str.replace
# df["date_part"] = df["column_name"].str.split(" ").str[0].str.replace(",", "")

# Method 2: Using list comprehension
def clean_date(date_string):
  return "".join([char for char in date_string if char != ","])


def print_urls(csv_file: str):
    df = pd.read_csv(csv_file, delimiter=",", quotechar='"')

    #tmp = df["@timestamp"].str.split(" ")

    #df["timestamp"] = pd.to_datetime(df["@timestamp"].str.split(" ").str[0] + " " + df["@timestamp"].str.split(" ").str[1])

    #df["date_part"] = df["@timestamp"].str.split().apply(lambda x: clean_date(x[0]))
    #print(df["date_part"])

    # Build datetime string and convert
    #df["timestamp"] = pd.to_datetime(df["date_part"] + " " + df["@timestamp"].str.split().str[4])

    df["url"] = df["message"].apply(extract_url)

    df["url"] = df["url"].apply(clean_url)

    print(df[["@timestamp", "url"]].to_string())


# Here's how to format the output:
# for index, row in df.iterrows():
#   print(f"Timestamp: {row['timestamp']}, URL: {row['url']}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_urls('~/Downloads/Hyrax-504-Errors.csv')
