# This script parses an SBOL file and produces a Provenance Graph for it using Graphviz
# This is specifically for the PROV-O model that SBOL uses
# USAGE: Simply pass an SBOL file as an argument when running this script

from graphviz import Digraph

dot = Digraph('digraph')

node_format = {
                'label' : None,
                'fontname' : 'Bitstream Vera Sans',
                'fontsize' : '8',
                'shape': 'record'
}

edge_format = {
                'fontname' : 'Bitstream Vera Sans',
                'fontsize' : 8,
}

node_format['label'] = label="{Animal|+ name : string\\l + age : int\\l |+ die() : void\\l}"
dot.node('Foo', **node_format)
dot.node('Bar', **node_format)
dot.edge('Foo', 'Bar')
print(dot)
dot.render('foo', view=True) # Create the graph image
