import math

def beautify_ratio(ratio):
    if ratio is not None:
        return str(round(ratio, 2))
    else:
        return 'NA'

def beautify_percentage(percentage):
    if percentage is not None:
        return str(round(100*percentage, 2)) + '%'
    else:
        return 'NA'

def beautify_financials(list_of_amounts):
    return ["{:,}".format(int(round(dollars / 1000))) for dollars in list_of_amounts]
