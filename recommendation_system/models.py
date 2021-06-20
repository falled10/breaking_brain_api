from py2neo.ogm import GraphObject, Property, RelatedFrom, RelatedTo


class Quiz(GraphObject):
    __primarykey__ = 'id'

    id = Property()

    title = Property()
    description = Property()
    is_free = Property()
    price = Property()
    created_at = Property()

    users = RelatedFrom("User", "PASSED")


class User(GraphObject):
    __primarykey__ = 'user_id'

    user_id = Property()
    passed = RelatedTo(Quiz)
