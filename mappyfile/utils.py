from __future__ import unicode_literals
from mappyfile.parser import Parser
from mappyfile.transformer import MapfileToDict
from mappyfile.pprint import PrettyPrinter
import codecs


def load(fn, expand_includes=True):
    p = Parser(expand_includes=expand_includes)
    ast = p.parse_file(fn)
    m = MapfileToDict()
    d = m.transform(ast)
    return d


def loads(s, expand_includes=True):
    p = Parser(expand_includes=expand_includes)
    ast = p.parse(s)
    m = MapfileToDict()
    d = m.transform(ast)
    return d


def write(d, output_file, indent=4):
    map_string = _pprint(d, indent)
    _save(output_file, map_string)
    return output_file


def dumps(d):
    return _pprint(d)


def find(lst, key, value):
    """
    Find an item in a list of dicts using a key and a value
    """
    return next((item for item in lst if item[key.lower()] == value), None)


def findall(lst, key, value):
    possible_values = ("'%s'" % value, '"%s"' % value)
    return (item for item in lst if item[key.lower()] in possible_values)


def _save(output_file, map_string):
    with codecs.open(output_file, "w", encoding="utf-8") as f:
        f.write(map_string)


def _pprint(d, indent=4):
    pp = PrettyPrinter(indent=indent)
    return pp.pprint(d)
