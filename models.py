from extensions import db


class Neuron(db.Model):

    intent = db.RelatedTo('Intent')

    @classmethod
    def create(cls):
        _neuron = cls()
        db.graph.create(_neuron)
        return _neuron

    def add_intent(self, intent):
        self.intent.add(intent)
        db.graph.push(self)
        return self


class Intent(db.Model):
    label = db.Label(name="intent")  # what type of intent it is

    item = db.RelatedTo('Item')
    name = db.Property()
    score = db.Property()

    @classmethod
    def create(cls, name):
        _intent = cls()
        _intent.name = name
        _intent.score = 0
        db.graph.create(_intent)
        return _intent

    def add_item(self, item):
        self.item.add(item)
        db.graph.push(self)
        return self


class Item(db.Model):
    label = db.Label(name="item")
    next = db.RelatedTo('Item')
    property = db.RelatedTo('Property')

    name = db.Property()
    score = db.Property()

    @classmethod
    def create(cls, name):
        _item = cls()
        _item.name = name
        _item.score = 0
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
    score = db.Property()

    @classmethod
    def create(cls, name):
        _property = cls()
        _property.name = name
        _property.score = 0
        db.graph.create(_property)
        return _property

    def add_property(self, property):
        self.next.add(property)
        db.graph.push(self)
        return self


def build_brain():

    # Create the Neuron
    neuron = Neuron.create()
    intent = Intent.create("buy")

    cloth = Item.create("cloth")
    jacket = Item.create("jacket")
    pant = Item.create("pant")

    cloth.add_item(jacket)
    cloth.add_item(pant)

    color_property = Property.create("color")
    red = Property.create("red")
    black = Property.create("black")
    blue = Property.create("blue")

    color_property.add_property(red)
    color_property.add_property(black)
    color_property.add_property(blue)

    material_property = Property.create("material")
    cotton = Property.create("cotton")
    polyster = Property.create("polyster")

    material_property.add_property(cotton)
    material_property.add_property(polyster)

    jacket.add_property(color_property)
    jacket.add_property(material_property)

    pant.add_property(color_property)
    pant.add_property(material_property)

    intent.add_item(cloth)
    neuron.add_intent(intent)
