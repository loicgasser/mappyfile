"""
https://dzone.com/articles/a-brief-tutorial-on-parsing-restructuredtext-rest
https://github.com/eliben/code-for-blog/blob/master/2017/parsing-rst/rst-link-check.py

Either parse C code or rst. Easier to do latter
"""
import glob, os, codecs

import docutils.frontend
import docutils.nodes
import docutils.parsers.rst
import docutils.utils

from mappyfile.tokens import COMPOSITE_NAMES, ATTRIBUTE_NAMES, SINGLETON_COMPOSITE_NAMES

def clean_values(v):

    if v.startswith("[") and v.endswith("]"):
        v = v[1:-1]
        vals = v.split("|")
        vals = [v.lower() for v in vals]
        return vals
    else:
        return ""

def clean_term(node):
    """
    Processing options

    E.g. PROCESSING "ITEMS=attribute_x,attribute_y,attribute_z"

    CLUSTER_GET_ALL_SHAPES=ON 
    CLUSTER_KEEP_LOCATIONS=ON 
    CLUSTER_USE_MAP_UNITS=ON 
    ITEMS
    """
    text = node.astext()

    # remove and :ref: directives (there is probably a way to do this with docutils)
    text = text.replace(":ref:`", "")
    text = text.replace("`", "")

    parts = text.split(" ")

    if len(parts) == 1:
        key = "processing"
        values = parts[0]
    else:
        key = parts[0].lower()
        values = ' '.join(parts[1:])

    values = clean_values(values)

    #print values

    return key, values

class TermVisitor(docutils.nodes.GenericNodeVisitor):
        
    def visit_term(self, node):
        key, values = clean_term(node)
        #print key, values
        self.kwds_dict[key] = values
              
    def default_visit(self, node):
        # Pass all other nodes through.
        pass

def read_doc(fn, kwds):
    #fn = r"C:\Code\mapserver_docs\en\mapfile\style.txt"
    with codecs.open(fn, encoding="utf-8")  as fileobj:
        txt = fileobj.read()
    
    txt = unicode(txt)

    # Parse the file into a document with the rst parser.
    default_settings = docutils.frontend.OptionParser(
        components=(docutils.parsers.rst.Parser,)).get_default_values()

    default_settings.report_level = 'quiet' # level 4
    document = docutils.utils.new_document(fileobj.name, default_settings)

    parser = docutils.parsers.rst.Parser()
    parser.parse(txt, document)

    # Visit the parsed document with our link-checking visitor.
    visitor = TermVisitor(document)
    visitor.kwds_dict = kwds
    document.walk(visitor)

def read_all_docs(fld):
    rst_files = glob.glob(fld + '/*.txt')

    mapfile_dict = {}

    for fn in rst_files: #[:2]:
        


        class_name = os.path.splitext(os.path.basename(fn))[0].lower()
        print "--------%s----------" % class_name

        kwds = {}
        mapfile_dict[class_name] = kwds

        read_doc(fn, kwds)

    all_keys = mapfile_dict.keys()

    for k, v in mapfile_dict.items():
        for kwd, vals in v.items():
            all_keys.append(kwd)

            for a in vals:
                all_keys.append(a)

            #print "%s: %s" % (k, kwd)

    mappyfile_keywords = COMPOSITE_NAMES.union(ATTRIBUTE_NAMES).union(SINGLETON_COMPOSITE_NAMES)

    print "Missing from docs:"
    print list(set(mappyfile_keywords) - set(all_keys))
    print("---")
    print "Missing from mappyfile:"
    print list(set(all_keys) - set(mappyfile_keywords))
    #print set(mappyfile_keywords).symmetric_difference(set(all_keys))         

    # add COLORRANGE   to STYLE

fld = r"C:\Code\mapserver_docs\en\mapfile"
read_all_docs(fld)