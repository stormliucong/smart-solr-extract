import pysolr
from utils import *
import configparser
import pandas as pd
from highlight import *

def get_solr_instance(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    solrhost = config['SOLR']['solrhost']
    solr_usr = config['SOLR']['username']
    solr_pwd = config['SOLR']['password']

    qt = "select"
    solr = pysolr.Solr(solrhost, search_handler="/"+qt, always_commit=True, timeout=100, auth=(solr_usr,solr_pwd))
    return solr

def search_solr(lab_keywords, EMPI_string, config_file):
    # define query and query solr
    solr = get_solr_instance(config_file = config_file)
    q = '''
    (MRN.string: "{EMPI_string}") AND (TEXT.string: "{lab_keywords}")
    '''.format(EMPI_string = EMPI_string, lab_keywords = lab_keywords)

    results = solr.search(q, **{
                        'fl' : ["EMPI.string","PRIMARY_TIME.long","TITLE.string","id"],
                        'rows': 10000,
                        'hl': 'true',
                        'hl.fragsize': 0,
                        'hl.snippets': 1,
                        'hl.fl': 'TEXT.string'
                    })

    return results

def parse_solr_meta(docs:dict):
    patientDf = pd.DataFrame.from_records(docs,columns={'PRIMARY_TIME.long','EMPI.string','TITLE.string','id'})
    # filter out None
    patientDf = patientDf.dropna()
    # filter screened files start with 's'
    patientDf['TITLE'] = patientDf['TITLE.string'].apply(lambda x: x[0])
    patientDf[~patientDf['TITLE'].str.startswith('s')]
    # convert time to timestamp
    patientDf['PRIMARY_TIME'] = patientDf['PRIMARY_TIME.long'].apply(lambda x: convert_timestamp(x[0]))
    # convert EMPI to float
    patientDf['EMPI'] = patientDf['EMPI.string'].apply(lambda x: convert_float(x[0]))
    return(patientDf[['EMPI','PRIMARY_TIME','TITLE','id']])

def parse_solr_highlighting(highlights: dict, tag = '<em>', keyword = 'Pre:'):
    parsed_list_by_doc = []
    for id in highlights:
        for snippet in highlights[id]['TEXT.string']:
            tag_position = [0] + list(find_all(snippet, tag)) + [9999]
            i = 0
            while i < (len(tag_position) - 2):
                pre_flag, date, value = annotate_highlight(snippet, tag, keyword, tag_position, i)            
                parsed_list_by_doc.append({
                    "id": id,
                    "snippet": snippet,
                    "tag_pos": i + 1,
                    "pre_flag": pre_flag,
                    "date" : date,
                    "value" : value
                })
                i = i + 1
    highlight_parsed_df = pd.DataFrame(parsed_list_by_doc)    
    return highlight_parsed_df