#
import pandas as pd
import os
import json
import csv

from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn

ROOT = '/Users/dhruvapatil/Downloads/fashion'

STOP_WORDS = {'got', 'vol', 'we', 'when', 'mean', 'himself', 'noted', 'with', 'ours', 'sufficiently', 'many', 'whereby',
              "i've", 'forth', 'take', 'you', 'ourselves', 'him', 'along', 'showed', 'formerly', 'effect', 'no', 'hi',
              'nor', 'thered', 'for', 'while', 'afterwards', 'make', 'section', 'ninety', 'beforehand', 'above',
              'recent', 'wed', 's', 'look', 'becoming', 'eg', 'whole', 'km', 'seemed', 'respectively', 'whereas',
              'obtained', 'j', 'specify', 'useful', 'date', 'except', 'anything', 'during', 'wherein', 'which', 'here',
              'thus', 'want', 'co', 'who', 'someone', 'never', 'possibly', "didn't", "that've", 'another', 'last',
              'suggest', 'went', 'ever', 'almost', 'toward', "hasn't", 'beyond', 'together', 'noone', 'sup', 'anyways',
              "they'll", "it'll", 'between', 'often', 'then', 'near', 'her', 'awfully', 'knows', 'x', "isn't", 'do',
              'arise', 'likely', 'away', 'using', 'been', 'usefully', 'quite', 'themselves', 'tries', 'out',
              'similarly', 'my', 'n', 'comes', 'un', 'very', 'resulted', 'selves', 'kept', 'howbeit', 'herein', 'from',
              'shes', 'theyre', 'onto', 'inward', 'invention', 'towards', 'nevertheless', 'added', 'rather', 'arent',
              'go', 'ed', 'up', 'ask', 'aside', 'and', "doesn't", 'q', "she'll", 'though', 'tell', 'however', 'me',
              'having', 'whether', 'took', 'specifically', 'thanx', 'various', 'us', 'instead', 'ref', 'nothing',
              'potentially', 'have', 'anyhow', 'everyone', "shouldn't", "haven't", 'already', 'somehow', 'always',
              'owing', 'research', 'truly', 'amongst', 'said', 'thou', 'each', 'promptly', 'since', 'anymore', 'back',
              'makes', 'non', 'within', 'itd', 'probably', 'soon', 'previously', 'see', 'gets', 'trying', 'ff',
              'sure\tt', 'world', 'begins', 'sometime', 'w', 'omitted', 'perhaps', 'means', 'beside', 'thousand',
              'would', 'behind', 'importance', 'may', 'inc', 'in', 'plus', 'possible', 'other', 'poorly', 'ones',
              'itself', 'regarding', 'e', 'willing', 'et-al', 'whatever', 'something', 'index', 'accordingly', 'ran',
              'resulting', 'might', 'sorry', 'she', "you'll", 'all', 'nine', 'had', 'd', 'happens', 'vs', 'least',
              'significantly', 'any', 'right', 'until', 'hereby', 'give', 'under', 'anybody', 'wish', 'only',
              'everywhere', 'than', 'doing', 'put', 'wherever', 'about', 'biol', 'by', 'unlikely', 'like', 'largely',
              'wasnt', 'their', 'stop', 'mrs', 'same', 'far', 'of', 'meantime', 'seen', 'immediately', 'tends', 'g',
              'heres', 'every', 'unlike', 'yourselves', 'maybe', 'unless', 'significant', 'z', 'ts', 'words', 'whod',
              'yes', 'l', 'til', 'per', 'alone', 'four', 'therefore', 'overall', 'particularly', 'apparently', 'adj',
              'next', 'what', "what'll", 'because', 'asking', 'yourself', 'slightly', 'off', 'name', 'more',
              'information', 'werent', 'across', 'whereupon', 'am', 'either', 'hid', 'saying', 'wouldnt', 'vols',
              'hither', 'f', 'or', 'rd', 'less', 'could', 'down', 'predominantly', 'particular', 'think', 'following',
              'our', 'yet', 'whim', 'pp', 'let', 'c', 'm', 'run', 'ending', 'become', 'needs', 'abst', 'self',
              'neither', 'keep\tkeeps', 'without', 'gone', 'gave', "i'll", 'found', 'even', 'specified', 'cause',
              'some', 'latter', 'old', 'whomever', 'nd', 'eighty', "there'll", 'has', 'etc', 'whoever', 'not',
              'successfully', 'made', 'there', 'throughout', 'seem', 'nonetheless', 'believe', 'around', 'so',
              'besides', 'youd', 'please', 'approximately', 'regardless', 'the', 'contains', 'u', 're', 'moreover',
              'whenever', 'else', 'five', 'says', 'regards', 'enough', 'thereto', 'whom', 'upon', 'com', 'nos',
              'should', 'mostly', 'your', 'nay', 'gives', 'those', 'nobody', "don't", 'lets', 'can', 'why', 'end',
              'edu', 'get', 'former', 'tried', 'nearly', 'similar', 'none', 'begin', 'ex', 'ought', 'how', 'if',
              'where', 'relatively', 'y', 'them', 'these', 'thru', 'thereupon', 'according', 'ok', 'six', 'beginning',
              'available', 'known', 'meanwhile', 'provides', 'throug', 'to', 'anyway', 'na', 'pages', 'liked', 'sub',
              'one', 'before', 'hundred', 'seeing', 'specifying', 'were', 'ca', 'into', 'must', 'really', "can't",
              'therein', 'actually', 'necessarily', 'million', 'refs', 'seems', 'id', 'looks', 'whither', 'most',
              'normally', 'wants', "'ve", 'he', 'widely', 'an', 'able', 'et', 'follows', 'page', "who'll", 'causes',
              'ltd', 'taking', 'thereby', 'different', 'ml', 'herself', 'among', 'a', 'ah', 'substantially', 'gotten',
              'thence', 'h', 'youre', 'need', 'thereafter', 'followed', "'ll", 'just', 'few', 'therere', 'sometimes',
              'due', 'furthermore', 'auth', 'wheres', 'recently', 'against', 'such', 'act', "that'll", 'his',
              'beginnings', 'goes', 'new', 'obviously', 'proud', 'did', 'sec', 'merely', 'being', 'over', 'via',
              'cannot', 'p', 'affects', 'hes', 'taken', 'much', 'contain', 'mr', 'briefly', 'yours', 'aren', 'be', 'o',
              'lately', 'was', 'que', 'important', 'is', 'strongly', 'thereof', 'although', 'oh', 'ord', 'does',
              'readily', 'unfortunately', 'on', 'affected', 'this', 'later', 'mainly', 'mg', 'announce', 'two',
              'affecting', 'zer', 'hence', 'whos', 'quickly', 'own', 'ie', 'saw', 'somethan', 'whereafter', 'seven',
              'come', 'namely', 'downwards', 'hereupon', 'thanks', 'several', 'part', "you've", 'certainly', 'getting',
              'below', 'certain', 'welcome', 'others', 'somebody', 'r', 'further', 'it', 'usually', 'www', 'miss',
              "they've", 'looking', 'say', 'thank', 'also', 'somewhere', 'fix', 'twice', 'mug', 'use', 'present',
              'eight', 'hers', 'viz', "there've", 'whence', 'especially', 'unto', 'became', 'k', 'couldnt', 'hed',
              'after', 'line', 'primarily', 'sent', 'usefulness', 'theres', 'whose', 'anywhere', 'giving', 'now',
              'theirs', 'theyd', 'results', 'lest', 'whats', 'shown', 'but', 'value', 'through', 'nowhere', 'little',
              'b', 'ups', 'kg', 'latterly', 'given', 'thoughh', 'at', 'know', 'came', 'showns', 'too', 'okay', 'th',
              'again', 'placed', 'tip', 'wont', 'once', "we've", 'home', 'still', 'uses', 'myself', 'containing',
              'immediate', "we'll", 'shall', 'somewhat', 'try', 'seeming', 'fifth', 'hardly', 'as', 'otherwise', 'v',
              'obtain', 'first', 'elsewhere', 'everybody', 'indeed', 'qv', 'show', 'thats', 'they', 'shows', 'used',
              'hereafter', 'done', 'way', 'both', 'brief', 'are', 'outside', 'becomes', 'accordance', 'everything',
              'anyone', 'its', 'necessary', 'shed', 'im', 'related', 'i', 'past', 'that'}


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


def T(s):
    return None if str(s) == 'nan' else str(s)


def list_directories(d):
    return list(filter(lambda x: os.path.isfile(os.path.join(d, x)), os.listdir(d)))


def custom_attributes_from_description(values):
    custom_attributes = {}
    custom_attributes_values = {*word_tokenize(values)} - STOP_WORDS
    for each_value in custom_attributes_values:
        syn = wn.synsets(each_value)
        if syn:
            parent = syn[0].hypernyms()
            if parent:
                custom_attributes[parent[0].lemma_names()[0]] = each_value
    return custom_attributes

allowed_categories = ['Men', 'Women']
with open("Fashion_data_new.json", "w+") as wrt:
    for each in list_directories(ROOT):
        FILE = f"{ROOT}/{each}"
        df = pd.read_json(FILE, lines=True, compression='gzip')
        if 'listing' in FILE or 'Store' in FILE or '20190801_20190801_1_zappos-us_product.gz' in FILE or '20190802_20190802_1_macys-us_product.gz':
            continue
        print("Processing: ", FILE)
        df = pd.read_json(FILE, lines=True, compression='gzip')
        df = df[df.category.isin(allowed_categories)]
        print(len(df))
        for row in df.iterrows():
            row = row[1]
            # category = row.category
            # subcategory = row.subcategory
            transformed_row = get_template()
            if T(row['description']):
                transformed_row['attributes'].update(custom_attributes_from_description(row['description']))
            if T(row['title']):
                transformed_row['attributes'].update(custom_attributes_from_description(row['title']))
            # print(transformed_row)
            for each_key in transformed_row:
                if each_key == 'attributes':
                    transformed_row['attributes']['color'] = T(row.color)
                    transformed_row['attributes']['size'] = T(row.size)
                elif each_key in row:
                    if each_key == "source":
                        print(row[each_key])
                    transformed_row[each_key] = row[each_key]
            wrt.write(json.dumps(transformed_row) + "\n")
        print("Processing Done for", FILE)
    print("Processing Completed for all files")
