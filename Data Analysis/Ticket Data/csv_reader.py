import csv
import json
import sys


"""
This script is used to convert a csv file to a json file.

Parameters:
    csv_file: the csv file to be converted
    json_file: the json file to be created

    Example:
        csv_to_json("./Data/converted_csv.csv", "./Data/converted_csv.json")

"""


def csv_to_json(csv_file, json_file):

    """
    This function is used to convert a csv file to a json file.

    Attributes:
        csv_file: the csv file to be converted
        json_file: the json file to be created
    
    Parameters:
        json_data: the json data to be written to the json file
        maxInt: the maximum integer value for the csv field size limit
        read_file: the csv file to be read
"""

    json_data = []
    maxInt = sys.maxsize

    while True:
        # decrease the maxInt value by factor 10
        # as long as the OverflowError occurs.

        try:
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt/10)
    
    read_file = csv.DictReader(open(csv_file))
    for row in read_file:
        json_data.append(row)

    with open(json_file, 'w', encoding='utf-8') as jsonf:
        jsonString = json.dumps(json_data, indent=4)
        jsonf.write(jsonString)


def run():
    cherwell_source = './Data/Source/Cherwell_Data.csv'
    cherwell_output = './Data/Source/converted_csv.json'
    workday_source = './Data/Source/Workday_Export.csv'
    workday_output = './Data/Source/Workday_Export.json'
    csv_to_json(cherwell_source, cherwell_output)
    csv_to_json(workday_source, workday_output)


if __name__ == '__main__':
    run()
