#!/usr/bin/env python3
# Produce LaTex qtree output from the parglare parse trees.

from parglare import Grammar, GLRParser, NodeNonTerm

INPUT = '1 + 2 * 3 + 4'

grammar = r'''
E: E '+' E
 | E '*' E
 | '(' E ')'
 | number;

terminals
number: /\d+/;
'''

g = Grammar.from_string(grammar)
parser = GLRParser(g, build_tree=True)

result = parser.parse(INPUT)


def tree_str(node, depth=0):
    indent = '  ' * depth
    if isinstance(node, NodeNonTerm):
        s = '\n{}[.{} {}\n{}]'.format(indent,
                                      node.production.symbol,
                                      ''.join([tree_str(n, depth+1)
                                               for n in node.children]),
                                      indent)
    else:
        s = '\n{}[.{} ]'.format(indent, node.value)
    return s


with open('qtree_out.txt', 'w') as f:
    f.write('\begin{{tabular}}{{{}}}\n'.format('c' * len(result)))
    trees = '&\n'.join(['\\Tree {}'.format(tree_str(tree)) for tree in result])
    f.write(trees)
