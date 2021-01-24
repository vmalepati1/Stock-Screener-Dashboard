import math

def beautify_ratio(ratio):
    if ratio is not None:
        str_result = str(round(ratio, 2))

        if str_result == 'nan' or str_result == 'inf' or str_result == '-inf':
            return 'NA'
        return str_result
    else:
        return 'NA'

def beautify_percentage(percentage):
    if percentage is not None:

        str_result = str(round(100*percentage, 2))

        if str_result == 'nan' or str_result == 'inf' or str_result == '-inf':
            return 'NA'
        return str_result + '%'
    else:
        return 'NA'

def beautify_financials(list_of_amounts):
    return ["{:,}".format(int(round(dollars / 1000))) for dollars in list_of_amounts]
