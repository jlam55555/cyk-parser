# cyk-parser
CYK parser for grammars in a CNF format for ECE467 Project 2

### CYK description
This is a simple implementation of the [Cocke–Younger–Kasami (CYK) algorithm][1]
to generate parse trees for sentences. This algorithm requires a tokenized
sentence and a Chomsky Normal Form (CNF) grammar as input. A CNF grammar is a
Context-Free Grammar (CFG) with rules in one of the two following formats:
> A → x

> A → B C

where A, B, and C denote non-terminal symbols and x denotes a terminal symbol.
The algorithm uses dynamic programming to generate all valid parse (binary)
trees that match the grammar.

Note that this algorithm *does not* attempt to find the best parse tree (this
usually requires training an additional classifier to determine the best parse
option, which is beyond the scope of this project), or use the original CFG (in
addition to the CNF) in order to express the parse tree in terms of the original
CFG (thus it may not be valid according to the original CFG, but it will be true
to the CNF).

### Files
- `sample_grammar.cfg` is a sample basic CFG mimicking the language of [the
    ATIS corpus][2]
- `sample_grammar.cnf` is the CFG form of `sample_grammar.cfg` generated with
    `cfg2cnf.py`
- `cfg2cnf.py` is a script to convert a CFG to a CNF (and ignores invalid rules)
- `cnfgrammar.py` declares a class that includes utilities for CNF grammars,
    e.g., loading it from a description file similar to `sample_grammar.cnf`,
    performing the CYK parsing, pretty-printing the result of the CYK parsing
- `main.py` is a driver with user prompts for loading CNF grammars and
    `cnfgrammar.py` and running the CYK algorithm

`sample_grammar.cfg`, `sample_grammar.cnf`, and `cfg2cnf.py` were provided in
the [project assignment][3] (converting CFGs to CNFs is not the object of this
assignment). I only wrote the `main.py` and `cnfgrammar.py` files for this
assignment (i.e., for performing the CYK parsing algorithm).

### Sample usage
`main.py` is a driver script to use the `CNFGrammar` class and CYK parse member
function.

(This was tested on Python 3.9. Requires *at least* 3.7 due to use of
`__future__.annotations` for recursive (lexical) type hinting.)

```bash
$ python3 main.py
Enter path to CNF file: grammars/sample_grammar.cnf
Do you want textual parse trees to be displayed? y/n: y
Enter a sentence for parsing (or "quit"): i book the flight from houston
Valid parse #1:
[S [NP i] [VP [Verb book] [NP [Det the] [Nominal [Nominal flight] [PP [Preposition from] [NP houston]]]]]] 
[S
	[NP i]
	[VP
		[Verb book]
		[NP
			[Det the]
			[Nominal
				[Nominal flight]
				[PP
					[Preposition from]
					[NP houston]
				]
			]
		]
	]
]
Valid parse #2:
[S [NP i] [VP [VP [Verb book] [NP [Det the] [Nominal flight]]] [PP [Preposition from] [NP houston]]]] 
[S
	[NP i]
	[VP
		[VP
			[Verb book]
			[NP
				[Det the]
				[Nominal flight]
			]
		]
		[PP
			[Preposition from]
			[NP houston]
		]
	]
]
Valid parse #3:
[S [NP i] [VP [_Dummy2 [Verb book] [NP [Det the] [Nominal flight]]] [PP [Preposition from] [NP houston]]]] 
[S
	[NP i]
	[VP
		[_Dummy2
			[Verb book]
			[NP
				[Det the]
				[Nominal flight]
			]
		]
		[PP
			[Preposition from]
			[NP houston]
		]
	]
]
Number of valid parses: 3
Enter a sentence for parsing (or "quit"): does the flight fly
Valid parse #1:
[S [_Dummy3 [Aux does] [NP [Det the] [Nominal flight]]] [VP fly]] 
[S
	[_Dummy3
		[Aux does]
		[NP
			[Det the]
			[Nominal flight]
		]
	]
	[VP fly]
]
Number of valid parses: 1
Enter a sentence for parsing (or "quit"): quit
```

[1]: https://en.wikipedia.org/wiki/CYK_algorithm
[2]: https://catalog.ldc.upenn.edu/docs/LDC93S4B/corpus.html
[3]: http://faculty.cooper.edu/sable2/courses/spring2021/ece467/NLP_Spring2021_Project2.docx