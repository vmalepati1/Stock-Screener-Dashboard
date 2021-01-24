import csv
import pandas as pd

def load_rankings_cache(sector):
    rows = []
    
    with open('data/rankings/' + sector + '.csv', encoding='utf-8') as f:
        rows = [{k: v for k, v in row.items()}
            for row in csv.DictReader(f)]

    return rows
