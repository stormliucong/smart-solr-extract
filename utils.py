import math
import datetime

def convert_float(x):
    if math.isnan(x):
        return None
    else:
        return '{:.0f}'.format(x)

def convert_timestamp(x):
        try:
            return datetime.datetime.fromtimestamp(x/1000).date()
        except:
            return None

def find_all(a_str, sub='<em>'):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches

