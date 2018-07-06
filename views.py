from flask import Blueprint, jsonify, request
from extensions import db
from models import build_brain


bp = Blueprint('bp', __name__)


@bp.route('/')
def index():
    raw_query = request.args.get('q', None)
    query = raw_query.replace(',', '')
    tokens = ','.join(["'{0}'".format(each) for each in query.split()])
    response_data = {
        'q': raw_query,
        'query_parts': [],
        't': []
    }

    # Find Intent
    cursor = db.graph.run((
        "match (you) <-- (parent:Neuron)"
        "where you.name in [{0}] or you.synonym in [{0}] ".format(tokens) +
        "set you.score = you.score + 1 "
        "return you.name"
    )).data()
    response_data['intent'] = cursor[0]['you.name']

    response_data['query_parts'] = [each.strip() for each in query.split('and')]
    for each_query in response_data['query_parts']:
        response_item = {
            'item': {},
            'type': ''
        }

        tokens = ','.join(["'{0}'".format(each) for each in each_query.split()])

        # Find Items
        cursor = db.graph.run((
            "match (you) <-- (parent:Item)"
            "where you.name in [{0}] or you.synonym in [{0}] ".format(tokens) +
            "set you.score = you.score + 1 "
            "return you.name"
        )).data()
        response_item['item']['name'] = cursor[0]['you.name']

        # Find Properties
        cursor = db.graph.run((
            "match (you) <-[:NEXT]- (parent:Property)"
            "where you.name in [{0}] or you.synonym in [{0}] ".format(tokens) +
            "set you.score = you.score + 1 "
            "return you.name, parent.name"
        )).data()
        properties = {}
        for each in cursor:
            if each['parent.name'] not in properties:
                properties[each['parent.name']] = [each['you.name']]
            else:
                properties[each['parent.name']].append(each['you.name'])

        # Insert default properties
        cursor = db.graph.run((
            "match (you) <-[:NEXT]- (parent:Property)"
            "where you.score > 1 "
            "return distinct parent.name, you.name, you.score "
            "order by you.score desc"
        )).data()
        response_item['item']['property'] = properties

        preferences = dict()
        for each in cursor:
            if each['parent.name'] not in properties:
                preferences[each['parent.name']] = [each['you.name']]

        response_item['item']['preferences'] = preferences

        # Find item category
        cursor = db.graph.run((
            "match (you) <-[:NEXT*1..]- (parent:Item)"
            "where you.name in [{0}] or you.synonym in [{0}] ".format(tokens) +
            "set you.score = you.score + 1 "
            "return parent.name, you.name"
        )).data()
        response_item['type'] = cursor[0]['parent.name']
        response_data['t'].append(response_item)

    return jsonify(response_data)


@bp.route('/build')
def build():

    # db.graph.run("MATCH (n) DETACH DELETE n")

    n = build_brain()

    return jsonify({'status': n})
