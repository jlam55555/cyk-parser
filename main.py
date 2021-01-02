"""
main.py: Driver for loading the grammar and generating parse trees using CYK
"""
from cnfgrammar import CNFGrammar

if __name__ == '__main__':
    cnf_filename = str(input('Enter path to CNF file: '))
    grammar = CNFGrammar.load(cnf_filename)

    while True:
        sentence = str(input('Enter a sentence for parsing (or "quit"): '))
        if sentence == 'quit':
            break

        # pretty-print parse trees
        parse_trees = grammar.cyk_parse_pp(sentence.split(' '))
        if len(parse_trees) == 0:
            print('No valid parses')
        for i, tree in enumerate(parse_trees):
            print(f'Parse {i+1}:\n{tree}')
