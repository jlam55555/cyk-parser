# __future__.annotations turns type annotations into a string so return type of
# CNFGrammar.load can validly be its own enclosing class
from __future__ import annotations
from collections.abc import Collection
from typing import Dict, Tuple


class CNFGrammar:
    """
    CNF grammar parser and storage (lookup) class

    Expects CNF to be valid and flattened (i.e., RHS only can consist of two
    non-terminals or a single terminal symbol).

    TODO: move cyk_parser into this class
    """

    def __init__(self, rules: Dict[Tuple[str, ...], Collection[str]]):
        """
        TODO: add this

        Tuple[str, ...] should technically be Union[Tuple[str], Tuple[str, str]]
        due to the mixing of singleton (one terminal) and two-tuple
        (two non-terminals) keys (i.e., the RHS of the CFG rules)
        """
        self._rules = rules

    def lookup(self, first: str, second: str = None) -> Collection[str]:
        """
        TODO: add this
        """
        if second is not None and (first, second) in self._rules:
            return self._rules[(first, second)]
        elif (first, ) in self._rules:
            return self._rules[(first, )]
        return []

    @staticmethod
    def load(cnf_file: str) -> CNFGrammar:
        """
        Loads a CNF grammar from a file. This assumes the file format is
        valid, the described grammar is valid (e.g., no repeating rules),
        so no error checking is done

        :param cnf_file:    path to CNF
        :return:            CNFGrammar object
        """
        rules = {}
        with open(cnf_file, 'r') as file_handle:
            for rule in file_handle.read().splitlines():
                rule_components = rule.split(' ')

                # hash the RHS of the rule and map it to the LHS
                # (turn RHS into a 1- or 2-tuple to make it hashable)
                # TODO: does this work without requiring a tuple?
                key = tuple(rule_components[2:])

                # ignore second rule component (arrow)
                # allow duplicates (i.e., same RHS for multiple LHS)
                if key not in rules:
                    rules[key] = []
                rules[key] += [rule_components[0]]

        return CNFGrammar(rules)

    def cyk_parse(self, words: Collection[str]) -> Collection[str]:
        """
        Parsing using the Cocke-Younger-Kasami DP algorithm

        :param words:   sentence to parse
        :return:        all valid parses of the sentence
        """
        N = len(words)

        # technically only need half of this, but make it the full rectangle
        # because the indexing is simpler to think about
        # dp[start, end] means the parses for words [start, end] (inclusive)
        # (different from the textbook, in which end is exclusive; this is
        # slightly more compact)
        # TODO: is it inefficient to create the sets here? but type hinting
        #       is annoying
        dp = [[set() for _ in range(N)] for _ in range(N)]

        for j, word in enumerate(words):

            # find non-terminals that derive this word
            # TODO: is this terminology correct?
            dp[j][j] = set(self.lookup(word))

            # find all parses for substring [i, j] for all splits k
            # (where the split is [i, k] and [k+1, j] b/c endpoints inclusive)
            for i in range(j-1, -1, -1):
                print(i, j)
                parses = []
                for k in range(i, j):
                    # FIXME: ew? might be a little cleaner with list comp.
                    for nt1 in dp[i][k]:
                        for nt2 in dp[k+1][j]:
                            parses += self.lookup(nt1, nt2)
                dp[i][j].update(parses)

                # TODO: need to keep links back to previous step
                #       currently is only a "recognizer," not a "parser"

        # TODO: remove
        print(dp)

        return list(dp[0][N-1])


if __name__ == '__main__':
    cnf_filename = str(input('Enter path to CNF file: '))
    grammar = CNFGrammar.load(cnf_filename)

    while True:
        sentence = str(input('Enter a sentence for parsing: '))
        print(grammar.cyk_parse(sentence.split(' ')))
