"""
main.py: Driver for loading the grammar and generating parse trees using CYK
"""
from cnfgrammar import CNFGrammar
import re

if __name__ == '__main__':
    cnf_filename = str(input('Enter path to CNF file: '))
    grammar = CNFGrammar.load(cnf_filename)

    # also display pretty-print with tabbing
    pp_tabs = input('Do you want textual parse trees to be displayed? y/n: ')\
                  .lower() == 'y'

    while True:
        sentence = str(input('Enter a sentence for parsing (or "quit"): '))
        if sentence == 'quit':
            break

        # pretty-print parse trees
        parse_trees = grammar.cyk_parse_pp(sentence.split(' '))
        if len(parse_trees) == 0:
            print('NO VALID PARSES')
        for i, tree in enumerate(parse_trees):
            print(f'Valid parse #{i+1}:')
            # less-pretty-printed with brackets
            # print(tree.replace('\n', '').replace('\t', '').replace('][', '] ['))
            tree_brackets = re.sub(r'\]\s+', '] ', tree)
            tree_brackets = re.sub(r'\s+\[', ' [', tree_brackets)
            tree_brackets = re.sub(r'\] (?=\])', ']', tree_brackets)
            print(tree_brackets)

            # pretty-printed with tabbing
            if pp_tabs:
                print(tree.rstrip('\n'))

        print(f'Number of valid parses: {len(parse_trees)}')
