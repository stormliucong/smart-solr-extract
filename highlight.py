from utils import *
import dateparser
from dateparser.search import search_dates
import re

def annotate_highlight(snippet, tag, keyword, tag_position, i):
        # search for pre_tag
        pre_tag_snippet = snippet[tag_position[i]: tag_position[i+1]]
        pre_flag = annotate_trigger(pre_tag_snippet, keyword = keyword)
        
        # search for date
        date_search_snippet = snippet[0: tag_position[i+1]]
        date = annotate_date(date_search_snippet)
        
        # search for value
        post_tag_snippet = snippet[tag_position[i+1]: tag_position[i+2]]
        value = annotate_value(post_tag_snippet)
    
        return pre_flag, date, value


def annotate_date(date_search_snippet, latest = True, regex_pattern = "\s+\d+\/\d+\/\d+"):
     
    if regex_pattern is not None:
        regex_pattern = ".*?(" + regex_pattern + ").*?"
        m = re.findall(regex_pattern, date_search_snippet)
        if m != []:
            parsed_date = [search_dates(matched_string) for matched_string in m]
        else:
            return None
    else:
        parsed_date = search_dates(date_search_snippet)
    
    if parsed_date is not None:
        if latest == True:
            return parsed_date[-1][-1][-1].strftime("%m/%d/%Y")
        else:
            return parsed_date[0][0][-1].strftime("%m/%d/%Y")
    else:
        return None

def annotate_trigger(pre_tag_snippet, keyword = 'Pre:'):
    if keyword in pre_tag_snippet:
        return True
    else:
        return False

def annotate_value(post_tag_snippet, regex_pattern = ".{0,6}(\d+\.\d+)L*[\,|\;|\s]+\(*(\d+%)*.*?\)*"):
    regex_pattern = ".+?<\/em>" + regex_pattern + ".*"
    m = re.findall(regex_pattern, post_tag_snippet)
    if m == []:
        return ()
    else:
        return m[0] # return closet matched values.