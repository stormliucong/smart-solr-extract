
import pandas as pd
from utils import *
from solr import *
from highlight import *
import csv

def main():
    pass


if __name__ == "__main__":
    config_file = 'test_solr.cfg'
    results = search_solr(lab_keywords = 'FVC', EMPI_string = "12345678910", config_file = config_file)
    highlight_df = parse_solr_highlighting(results.highlighting) 
    meta_df = parse_solr_meta(results.docs)
    fvc_value_parsed_df = meta_df.merge(highlight_df)
    fvc_value_parsed_df.to_csv("fvc_parsed_example.csv", index=None, quoting=csv.QUOTE_NONNUMERIC)
