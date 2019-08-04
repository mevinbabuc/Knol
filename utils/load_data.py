import pandas as pd
import json

from .mappings import MASTER_MAPPING

# best buy

df = pd.read_json('./data/electronics/20190801_20190801_1_bestbuy-us_product.gz', lines=True, compression='gzip')
df = df[df.category == 'Computers & Tablets'][df.subcategory == 'Tablets']
df = df[MASTER_MAPPING['best_buy']['detail']]

# df['json_attributes'] = df.apply(lambda x: json.loads(x), axis=1)

import pandas as pd
import os
import json
import csv
ROOT = './data/electronics/'

def get_template():
    return {
        "source": "",
        "title": "",
        "url": "",
        "images": "",
        "description": "",
        "available_price": "",
        "brand": "",
        "category": "",
        "subcategory": "",
        "attributes": {},
        "stock": "",
        "thumbnail": ""
    }

def list_directories(d):
    return list(filter(lambda x: os.path.isfile(os.path.join(d, x)), os.listdir(d)))

allowed_categories = ['Men', 'Women']

with open("abc.json", "w+") as wrt:

    df = pd.read_json('./data/electronics/20190801_20190801_1_bestbuy-us_product.gz', lines=True, compression='gzip')
    df = df[df.category == 'Computers & Tablets'][df.subcategory == 'Tablets']
    df = df[MASTER_MAPPING['best_buy']['detail']]

    for row in df.iterrows():
        row = row[1]
        category = row.category
        subcategory = row.subcategory
        transformed_row = get_template()
        for each_key in transformed_row:
            if each_key == 'attributes':
                _d = json.loads(row.specification)
                attrs = {each[0]: each[1] for each in _d}
                transformed_row['attributes'] = attrs

            elif each_key in row:
                transformed_row[each_key] = row[each_key]
        wrt.write(json.dumps(transformed_row)+"\n")
        break
    print("Processing Done")
