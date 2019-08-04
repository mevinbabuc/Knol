import string
from flask import Blueprint, jsonify, request
from flask_cors import CORS
from extensions import db
from models import build_brain

from utils import stop_words


bp = Blueprint('bp', __name__)
CORS(bp)


def tokenize(input):
    """
    Takes input as a string of sequences and
    returns tokens along with their actual start and end index from
    the original input sentence
    """
    def get_new_buffer():
        return {
            'start': None,
            'end': None,
            'surface_text': None,
        }
    buffer = get_new_buffer()
    output = []
    for idx, current in enumerate(input):
        # Buffering start or continuing
        if current.isalpha() or current.isdigit():
            # Buffering start
            if not buffer['surface_text']:
                buffer['start'] = idx
                buffer['surface_text'] = ''
            buffer['surface_text'] += current
        elif current == "'":
            # if buffer is activate and
            # two or more consecutive aprostophe then clear the buffer else continue
            if idx > 1 and input[idx - 1] == "'" and buffer['surface_text']:
                buffer['end'] = buffer['start'] + len(buffer['surface_text']) - 1
                output.append(buffer)
                buffer = get_new_buffer()
            else:
                continue
        # Buffering end (no text or number) and there is some data in buffer
        elif buffer['surface_text']:
            buffer['end'] = idx - 1
            output.append(buffer)
            buffer = get_new_buffer()
    # some buffer is left
    if buffer['surface_text']:
        buffer['end'] = buffer['start'] + len(buffer['surface_text']) - 1
        output.append(buffer)
    return output



@bp.route('/')
def index():
    raw_query = request.args.get('q', None)
    query = raw_query.replace(',', '')
    tokens = [e['surface_text'].lower() for e in tokenize(query)]


    response_data = {
        'q': raw_query,
        'query_parts': [],
        't': []
    }


    response_data['query_parts'] = [each.strip() for each in query.split('and')]
    for each_query in response_data['query_parts']:
        response_item = {
            'item': {},
            'r_type': ''
        }

        tokens = ','.join(["'{0}'".format(each) for each in each_query.split()])

        # Find Items
        cursor = db.graph.run((
            "match (you) <-- (parent:Item)"
            "where you.name in [{0}] or you.synonym in [{0}] ".format(tokens) +
            "set you.score = you.score + 1"
            "return you.name, you.config"
        )).data()

        try:
            response_item['item']['name'] = cursor[0]['you.name']
            response_item['item']['config'] = cursor[0]['you.config']
        except Exception as e:
            response_item['item']['name'] = None

        # Find Properties
        cursor = db.graph.run((
            "match (you) <-[:NEXT]- (parent:Property)"
            "where you.name in [{0}] or you.synonym in [{0}] ".format(tokens) +
            "set you.score = you.score + 1 "
            "return you.name, parent.name, you.synonym, you.config"
        )).data()
        properties = {}
        translate_dict = dict()
        for each in cursor:
            if each['parent.name'] not in properties:
                properties[each['parent.name']] = [each['you.name']]
            else:
                properties[each['parent.name']].append(each['you.name'])

            translate_dict[each['you.name']] = each['you.synonym'] if 'you.synonym' in each else None

        # Insert default properties
        cursor = db.graph.run((
            "match (you) <-[:NEXT]- (parent:Property)"
            "where you.score > 1 "
            "return distinct parent.name, you.name, you.score, you.synonym "
            "order by you.score desc"
        )).data()
        response_item['item']['property'] = properties

        preferences = dict()
        for each in cursor:
            if each['parent.name'] not in properties:
                preferences[each['parent.name']] = [each['you.name']]
                translate_dict[each['you.name']] = each['you.synonym'] if 'you.synonym' in each else None

        response_item['item']['preferences'] = preferences

        # Find item category
        cursor = db.graph.run((
            "match (you) <-[:NEXT*1..]- (parent:Item)"
            "where you.name in [{0}] or you.synonym in [{0}] ".format(tokens) +
            "set you.score = you.score + 1 "
            "return parent.name, you.name"
        )).data()

        response_item['translate'] = translate_dict
        try:
            response_item['type'] = cursor[0]['parent.name']
        except Exception as e:
            response_item['type'] = None

        response_data['t'].append(response_item)

    return jsonify(response_data)


@bp.route('/build')
def build():

    db.graph.run("MATCH (n) DETACH DELETE n")
    db.graph.run("MATCH (n) DELETE n")

    n = build_brain()

    return jsonify({'status': n})
