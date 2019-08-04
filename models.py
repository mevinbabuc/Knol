from extensions import db
import pandas as pd
import json


class Neuron(db.Model):
    item = db.RelatedTo('Item')

    @classmethod
    def create(cls):
        _neuron = cls()
        db.graph.create(_neuron)
        return _neuron

    def add_item(self, item):
        self.item.add(item)
        db.graph.push(self)
        return self


class Item(db.Model):
    label = db.Label(name="item")
    next = db.RelatedTo('Item')
    property = db.RelatedTo('Property')

    name = db.Property()
    synonym = db.Property()
    config = db.Property()

    @classmethod
    def create(cls, name, synonym=None, config={}):
        _item = cls()
        _item.name = name
        _item.score = 0

        if synonym:
            _item.synonym = synonym

        if config:
            _item.config = config

        db.graph.create(_item)
        return _item

    def add_item(self, item):
        self.next.add(item)
        db.graph.push(self)
        return self

    def add_property(self, property):
        self.property.add(property)
        db.graph.push(self)
        return self


class Property(db.Model):
    label = db.Label(name="property")
    next = db.RelatedTo('Property')

    name = db.Property()
    synonym = db.Property()
    score = db.Property()

    @classmethod
    def create(cls, name, synonym=None):
        _property = cls()
        _property.name = name
        _property.score = 0
        if synonym:
            _property.synonym = synonym

        db.graph.create(_property)
        return _property

    def add_property(self, property):
        self.next.add(property)
        db.graph.push(self)
        return self

t = lambda x: x.lower().strip() if x and type(x) == str else ""


def build_brain():

    # Create the Neuron
    neuron = Neuron.create()
    fashion = Item.create("Electronics")
    neuron.add_item(fashion)

    df = pd.read_json('/app/data/bestbuy-us_product.json', lines=True)

    attributes_list = df['attributes']
    attr_name_id_mapping = {}
    attr_value_id_mapping = {}
    category = {}
    subcategory = {}
    brands = {}
    linking = {}

    for attributes in attributes_list:
        for attr_name, attr_value in attributes.items():
            at_n = t(attr_name) if attr_name else ""
            at_v = t(attr_value) if attr_value else ""

            if at_n not in attr_name_id_mapping:
                attr_name_id_mapping[at_n] = Property.create(at_n)

            if at_v not in attr_value_id_mapping:
                attr_value_id_mapping[at_v] = Property.create(at_v)

            relation_key = f"{at_n}_{at_v}"
            if relation_key not in linking:
                attr_name_id_mapping[at_n].add_property(attr_value_id_mapping[at_v])
                linking[relation_key] = True

    unique_categories = df.category.unique()
    for each_category in unique_categories:
        it = Item.create(t(each_category))
        category[t(each_category)] = it
        fashion.add_item(it)

    unique_subcategories = df.subcategory.unique()
    for each_subcategory in unique_subcategories:
        it = Item.create(t(each_subcategory))
        subcategory[t(each_subcategory)] = it

    brand_unique = df.brand.unique()
    for each_brand in brand_unique:
        it = Item.create(t(each_brand))
        brands[t(each_brand)] = it


    for each_row in df.iterrows():
        each_row = each_row[1]
        category_node = category[t(each_row.category)]
        subcategory_node = subcategory[t(each_row.subcategory)]
        brand_node = brands[t(each_row.brand)]

        # Connecting a category to a sub cateogry
        category_subcategory_relationship_key = f"{each_row.category}_{each_row.subcategory}"
        if category_subcategory_relationship_key not in linking:
            linking[category_subcategory_relationship_key] = True
            category_node.add_item(subcategory_node)

        # Connecting brand to a sub category
        subcategory_brand_relationship_key = f"{each_row.subcategory}_{each_row.brand}"
        if subcategory_brand_relationship_key not in linking:
            linking[subcategory_brand_relationship_key] = True
            subcategory_node.add_item(brand_node)

        # Product Node
        config = each_row.copy()
        attributes = config.pop('attributes')

        product_node = Item.create(t(each_row.title), config=json.dumps(config.to_dict()))
        brand_node.add_item(product_node)

        for each_attr_name in attributes:
            product_node.add_property(attr_name_id_mapping[t(each_attr_name)])

    # cloth = Item.create("cloth", "kapda")
    # jacket = Item.create("jacket")
    # pant = Item.create("pant", "patloon")
    #
    # cloth.add_item(jacket)
    # cloth.add_item(pant)
    #
    # color_property = Property.create("color", "rang")
    # red = Property.create("red", "lal")
    # black = Property.create("black", "kala")
    # blue = Property.create("blue", "neela")
    #
    # color_property.add_property(red)
    # color_property.add_property(black)
    # color_property.add_property(blue)
    #
    # material_property = Property.create("material")
    # cotton = Property.create("cotton", "rui")
    # polyster = Property.create("polyester")
    #
    # material_property.add_property(cotton)
    # material_property.add_property(polyster)
    #
    # jacket.add_property(color_property)
    # jacket.add_property(material_property)
    #
    # pant.add_property(color_property)
    # pant.add_property(material_property)
    #
    # intent.add_item(cloth)
    # neuron.add_intent(intent)
