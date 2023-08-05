class Query(object):
    def execute(self, items):
        raise NotImplementedError()


class ContainsQuery(Query):
    __slots__ = ['text']

    def __init__(self, text):
        self.text = text

    def execute(self, items):
        return list(filter(lambda x: self.text in x, items))


class OrderByQuery(Query):
    __slots__ = ['field', 'desc']

    def __init__(self, field=None, desc=False):
        self.field = field
        self.desc = desc

    def execute(self, items):
        if self.field:
            return sorted(items, key=lambda x: getattr(x, self.field, x.get(self.field)), reverse=self.desc)
        else:
            return sorted(items, reverse=self.desc)


class StartsQuery(Query):
    __slots__ = ['text']

    def __init__(self, text):
        self.text = text

    def execute(self, items):
        return list(filter(lambda x: x.startswith(self.text), items))


class EndsQuery(Query):
    __slots__ = ['text']

    def __init__(self, text):
        self.text = text

    def execute(self, items):
        return list(filter(lambda x: x.endswith(self.text), items))


class FilterQuery(Query):
    __slots__ = ['func']

    def __init__(self, func):
        self.func = func

    def execute(self, items):
        return list(filter(self.func, items))


class SelectQuery(Query):
    __slots__ = ['fields']

    def __init__(self, *fields):
        if not fields:
            raise TypeError('select() method must be taken at least 1 argument.')

        self.fields = list(fields)

    def execute(self, items):
        raise NotImplementedError()

    @classmethod
    def does_field_exist(cls, field, obj):
        return hasattr(obj, field) or (isinstance(obj, dict) and field in obj)

    def check_fields(self, item):
        for field in self.fields:
            if self.does_field_exist(field, item):
                return True

        return False

    @classmethod
    def get_field_value(cls, obj, field):
        value = getattr(obj, field, None) or (obj.get(field) if isinstance(obj, dict) else None)
        if not value:
            raise ValueError('{} field does not exist'.format(field))

        return value


class SelectDictQuery(SelectQuery):
    __slots__ = ['fields']

    def execute(self, items):
        return [{f: self.get_field_value(x, f) for f in self.fields} for x in filter(self.check_fields, items)]


class SelectListQueryFactory(object):
    @staticmethod
    def new(fields, flat):
        return SelectFlatListQuery(*fields) if flat else SelectListQuery(*fields)


class SelectListQuery(SelectQuery):
    __slots__ = ['fields']

    def execute(self, items):
        return [[self.get_field_value(x, f) for f in self.fields] for x in filter(self.check_fields, items)]


class SelectFlatListQuery(SelectQuery):
    __slots__ = ['fields']

    def __init__(self, *fields):
        super(SelectFlatListQuery, self).__init__(*fields)
        if len(self.fields) > 1:
            raise TypeError('Flat lists can be created with only one field.')

    def execute(self, items):
        return [self.get_field_value(x, self.fields[0]) for x in filter(self.check_fields, items)]


class TakeQuery(Query):
    __slots__ = ['count']

    def __init__(self, count):
        self.count = count

    def execute(self, items):
        return items[:self.count]


class SkipQuery(Query):
    __slots__ = ['count']

    def __init__(self, count):
        self.count = count

    def execute(self, items):
        return items[self.count:]


class MaxQuery(Query):
    __slots__ = ['field']

    def __init__(self, field=None):
        self.field = field

    def execute(self, items):
        return max(SelectFlatListQuery(self.field).execute(items)) if self.field else max(items)


class MinQuery(Query):
    __slots__ = ['field']

    def __init__(self, field=None):
        self.field = field

    def execute(self, items):
        return min(SelectFlatListQuery(self.field).execute(items)) if self.field else min(items)


class SumQuery(Query):
    __slots__ = ['field']

    def __init__(self, field=None):
        self.field = field

    def execute(self, items):
        return sum(SelectFlatListQuery(self.field).execute(items)) if self.field else sum(items)


class CountQuery(Query):
    __slots__ = ['field']

    def __init__(self, field=None):
        self.field = field

    def execute(self, items):
        if self.field:
            return len(SelectDictQuery(self.field).execute(items))
        else:
            return len(items)


class AvgQuery(Query):
    __slots__ = ['field']

    def __init__(self, field=None):
        self.field = field

    def execute(self, items):
        return SumQuery(self.field).execute(items) / CountQuery(self.field).execute(items)


class DistinctQuery(Query):
    __slots__ = ['field']

    def __init__(self, field=None):
        self.field = field

    def execute(self, items):
        return list(set(SelectFlatListQuery(self.field).execute(items))) if self.field else list(set(items))


class InQuery(Query):
    __slots__ = ['search_list']

    def __init__(self, search_list):
        self.search_list = search_list

    def execute(self, items):
        return list(filter(self._in, items))

    def _in(self, item):
        for search in self.search_list:
            if search == item:
                return True
        return False


class FirstQuery(Query):
    def execute(self, items):
        return items[0] if len(items) > 0 else None


class LastQuery(Query):
    def execute(self, items):
        return items[-1] if len(items) > 0 else None


class ExistsQuery(Query):
    def execute(self, items):
        return len(items) > 0


class SliceQuery(Query):
    __slots__ = ['start', 'end']

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def execute(self, items):
        return items[self.start:self.end]


class EvenQuery(Query):
    def execute(self, items):
        return items[::2]


class OddQuery(Query):
    def execute(self, items):
        return items[1::2]


class QueryRunner(object):
    __slots__ = ['queries']

    def __init__(self, queries):
        self.queries = queries
    
    def run(self, items):
        _items = items
        for query in self.queries:
            _items = query.execute(_items)
        
        return _items

