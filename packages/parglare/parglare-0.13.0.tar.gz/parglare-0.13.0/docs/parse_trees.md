# Parse trees

During shift/reduce operations parser will call [actions](./actions.md). If
`build_tree` parser constructor parameter is set to `True` the default actions
for building parse tree nodes will be called. In the case of GLR parser multiple
trees can be built simultaneously (the parse forest).

The nodes of parse trees are instances of either `NodeTerm` for terminal nodes
(leafs of the tree) or `NodeNonTerm` for non-terminal nodes (intermediate
nodes).


Each node of the tree has following attributes:

- `start_position/end_position` - the start and end position in the input stream
  where the node starts/ends. It is given in absolute 0-based offset. To convert
  to line/column format for textual inputs you can use
  `parglare.pos_to_line_col(input_str, position)` function which returns tuple
  `(line, column)`. Of course, this call doesn't make any sense if you are
  parsing a non-textual content.

- `layout_content` - the
  [layout](./grammar_language.md#handling-whitespaces-and-comments-in-your-language)
  that preceeds the given tree node. The layout consists of
  whitespaces/comments.

- `symbol` (property) - a grammar symbol this node is created for.


Additionally, each `NodeTerm` has:

- `value` - the value (a part of input_str) which this terminal represents. It
  is equivalent to `input_str[start_position:end_position]`.

- `additional_data` - a list of additional information returned by a custom
  recognizer. This gets passed to terminal nodes actions if `call_actions` is
  called for the parse tree.

Additionally, each `NodeNonTerm` has:

- `children` - sub-nodes which are also of `NodeNonTerm`/`NodeTerm` type.
  `NodeNonTerm` is iterable. Iterating over it will iterate over its children.

- `production` - a grammar production whose reduction created this node.

Each node has a `tree_str()` method which will return a string representation of
the sub-tree starting from the given node. If called on a root node it will
return the string representation of the whole tree.

For example, parsing the input `1 + 2 * 3 - 1` with the expression grammar from
the quick start will look like this if printed
with `tree_str()`:

    E[0]
    E[0]
      E[0]
        number[0, 1]
      +[2, +]
      E[4]
        E[4]
          number[4, 2]
        *[6, *]
        E[8]
          number[8, 3]
    -[10, -]
    E[11]
      number[11, 1]


!!! tip

    You can use `tree_str()` on the root of the parse tree to get the string
    representation of the parse tree. This can be handy to compare multiple
    trees returned by GLR parser to analyze ambiguity.
    
    For example:
    
        # Here we have GLR parser which returns multiple parse trees due to ambiguity.
        # It is important to turn on tree building.
        parser = GLRParser(g, build_tree=True)
        trees = parser.parse_file('some_file')
        for idx, tree in enumerate(trees):
            with open(f'tree_{idx:03d}.txt', 'w') as f:
                f.write(tree.tree_str())
    
    Now you can run any diff tool on the produced outputs to see where are the ambiguities:
    
        $ meld tree_000.txt tree_001.txt
    
    
