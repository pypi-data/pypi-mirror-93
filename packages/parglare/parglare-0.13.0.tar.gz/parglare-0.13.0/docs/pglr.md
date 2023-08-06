# The `pglr` command

`pglr` CLI command is available when parglare is installed. This command is used
to debug the grammar, visualize the LR automata and make a visual trace of the
GLR parsing.

To get the help on the command run:

```nohighlight
$ pglr
Usage: pglr [OPTIONS] COMMAND [ARGS]...

  Command line interface for working with parglare grammars.

Options:
  --debug                     Debug/trace output.
  --no-colors                 Disable output coloring.
  --prefer-shifts             Prefer shifts over reductions.
  --prefer-shifts-over-empty  Prefer shifts over empty reductions.
  --help                      Show this message and exit.

Commands:
  compile
  trace
  viz
```


## Compiling the grammar

`compile` command is used for checking the grammar, reporting conflicts and
producing LR table `.pgt` files. It is not mandatory to compile the grammar as
parglare will calculate table during parser construction if `.pgt` file doesn't
exist or is not newer than all of the grammar files. But it is recommended to
use this command during development to investigate possible conflicts and
calculate table in advance.

To get help on the command run:

```nohighlight
$ pglr compile --help
Usage: pglr compile [OPTIONS] GRAMMAR_FILE

Options:
  --help  Show this message and exit.

To compile and check your grammar run:

    $ pglr compile <grammar_file>
```

where `<grammar_file>` is the path to your grammar file.

If there is no error in the grammar you will get `Grammar OK.` message. In case
of LR conflicts you will get a detailed information on all Shift/Reduce and
Reduce/Reduce conflicts which makes much easier to see the exact cause of
ambiguity and to use [disambiguation rules](./disambiguation.md) to resolve the
conflicts or to go with GLR if the grammar is not LR(1).

In case of error you will get error message with the information what is the
error and where it is in the grammar.

For example:

```nohighlight
$ pglr compile calc.pg
Error in the grammar file.
Error in file "calc.pg" at position 4,16 => "/' E  left*, 2}\n | E ".
Expected: { or | or ; or Name or RegExTerm or StrTerm
```

!!! tip
    Be sure to deploy `.pgt` file to production as you will avoid unnecessary
    table calculation on the first run. Furthermore, if parglare can't write to
    `.pgt` file due to permission it will resort to calculating LR table
    whenever started.


## Getting detailed information about the grammar

If there is a conflict in the LR table, by default, you get the information about
the state in which conflict occurs, lookaheads and actions.

To get the full information about the grammar you can run `pglr` command in the
debug mode.

```nohighlight
$ pglr --debug compile calc.pg

*** GRAMMAR ***
Terminals:
number STOP + - ^ EMPTY ) \d+(\.\d+)? ( / *
NonTerminals:
S' E
Productions:
0: S' = E STOP
1: E = E + E
2: E = E - E
3: E = E * E
4: E = E / E
5: E = E ^ E
6: E = ( E )
7: E = number


*** STATES ***

State 0
        0: S' = . E STOP   {}
        1: E = . E + E   {STOP, -, +, ^, ), /, *}
        2: E = . E - E   {STOP, -, +, ^, ), /, *}
        3: E = . E * E   {STOP, -, +, ^, ), /, *}
        4: E = . E / E   {STOP, -, +, ^, ), /, *}
        5: E = . E ^ E   {STOP, -, +, ^, ), /, *}
        6: E = . ( E )   {STOP, -, +, ^, ), /, *}
        7: E = . number   {STOP, -, +, ^, ), /, *}



    GOTO:
      E->1

    ACTIONS:
      (->SHIFT:2, number->SHIFT:3

...

```

This will give enumerated all the productions of your grammars and all the
states. For each state you get the LR items with lookahead, elements of GOTO
table and elements of ACTIONS table. In the previous example state 0 will have a
transition to state 1 when `E` is reduced, transition to state 2 if `(` can
be shifted and transition to state 3 if `number` can be shifted.

!!! tip

    You can use `--debug` option with any `pglr` command to put the parser
    in the debug mode and get a detailed output.


## Visualizing LR automata

To visualize your automata with all the states and possible transitions run the
command:

```nohighlight
$ pglr viz calc.pg
Grammar OK.
Generating 'calc.pg.dot' file for the grammar PDA.
Use dot viewer (e.g. xdot) or convert to pdf by running 'dot -Tpdf -O calc.pg.dot'
```

As given in the output you will get a `dot` file which represents LR automata
visualization. You can see this diagram using dot viewers (e.g.
[xdot](https://github.com/jrfonseca/xdot.py)) or you can transform it to other
file formats using the `dot` tool (you'll have to install Graphviz software for
that).

This is an example of LR automata visualization for the `calc` grammar from the
quick intro (click on the image to enlarge):

[![Calc LR automata](./images/calc.pg.dot.png)](./images/calc.pg.dot.png)



## Tracing GLR parsing

GLR parser uses a graph-like stack (_Graph-Structured Stack - GSS_) and to
understand what's going on during GLR operation GLR parser and `pglr` command
provide a way to trace the GSS.

To get a help on the `trace` command run:

```nohighlight
$ pglr trace --help
Usage: pglr trace [OPTIONS] GRAMMAR_FILE

Options:
  -f, --input-file PATH  Input file for tracing
  -i, --input TEXT       Input string for tracing
  --help                 Show this message and exit.
```

You either give your input using file (`-f`) or using string provided in the
command (`-i`), but not both.

To run the GLR trace for the calc grammar and some input:

```bash
$ pglr trace calc.pg -i "2 + 3 * 5"
```

The `-i` switch tells the command to treat the last parameter as the input
string to parse.


!!! tip

    Since the GSS can be quite large and complex for larger inputs the advice is
    to use a minimal input that will exibit the intended behaviour for a
    visualization to be usable.


The `trace` sub-command implies `--debug` switch so the parser will run in the
debug mode and will produce the detailed output on the grammar, LR automata and
the parsing process.

Additionally, a `dot` file will be created, with the name `parglare_trace.dot`
if input is given on command line or `<input_file_name>_trace.dot` if input is
given as a file. The `dot` file can be visualized using dot viewers or
transformed to other file formats using the `dot` tool.

For the command above, GLR trace visualization will be (click on the image to
enlarge):

[![Calc GLR trace](./images/calc_trace.dot.png)](./images/calc_trace.dot.png)

Dotted red arrows represent each step in the parsing process. They are numbered
consecutively. After the ordinal number is the action (either **S**-Shift or
**R**-reduce). For shift action a grammar symbol and the shifted value is given.
For reduction a production is given and the resulting head will have a parent
node closer to the beginning.

Black solid arrows are the links to the parent node in the GSS.

There are also dotted orange arrows (not shown in this example) that shows dropped
empty reductions. Dropping happens when parser has found a better solution (i.e. a
solution with fewer empty reductions).


!!! tip

    To produce GLR parser visual trace from code your must [put the parser in
    debug mode](./debugging.md) by setting `debug` to `True` and enable visual
    tracing by setting `debug_trace` to `True`.
