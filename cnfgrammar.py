"""
cnfgrammar.py: Defining the CNF grammar data structures and utilities, including
the CYK parser algorithm
"""

# __future__.annotations turns type annotations into a string so return type of
# CNFGrammar.load can validly be its own enclosing class
from __future__ import annotations

from collections import defaultdict
from typing import Dict, Tuple, List, Union

# useful type declarations
# forward (recursive) type definitions allowed by __future__.annotations
CNFGrammarRHS = Union[Tuple[str], Tuple[str, str]]
CNFGrammarLHS = List[str]
ParseTree = Union[Tuple[str, 'ParseTree', 'ParseTree'], Tuple[str, str]]


class CNFGrammar:
    """
    Wrapper around a dict containing a CNF grammar lookup table, as well as
    associated utilities (parsing a CNF description file, looking up definitions
    in the grammar, performing CYK using this grammar)

    Expects CNF to be valid and flattened (i.e., RHS only can consist of two
    non-terminals or a single terminal symbol).
    """

    def __init__(self, rules: Dict[CNFGrammarRHS, CNFGrammarLHS]):
        """
        Creation of CNF instance basically wraps a dictionary representing
        a lookup table of the grammar

        Tuple[str, ...] should technically be Union[Tuple[str], Tuple[str, str]]
        due to the mixing of singleton (one terminal) and two-tuple
        (two non-terminals) keys (i.e., the RHS of the CFG rules)
        """
        self._rules = rules

    def lookup(self, first: str, second: str = None) -> CNFGrammarLHS:
        """
        Looks up a rule (given the RHS) in the CNF grammar. Returns all matching
        LHS nonterminals.
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
                key = tuple(rule_components[2:])

                # ignore second rule component (arrow)
                # allow duplicates (i.e., same RHS for multiple LHS)
                if key not in rules:
                    rules[key] = []
                rules[key] += [rule_components[0]]

        return CNFGrammar(rules)

    def cyk_parse(self, words: List[str]) -> List[ParseTree]:
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
        dp = [[defaultdict(list) for _ in range(N)] for _ in range(N)]

        # cyk algorithm using dynamic programming
        for j, word in enumerate(words):

            # find non-terminals that derive this word
            for parse in set(self.lookup(word)):
                dp[j][j][parse].append(None)

            # find all parses for substring [i, j] for all splits k
            # (where the split is [i, k] and [k+1, j] b/c endpoints inclusive)
            [dp[i][j][parse].append((i, k, j, nt1, nt2))
             for i in range(j-1, -1, -1)
             for k in range(i, j)
             for nt1 in dp[i][k]
             for nt2 in dp[k+1][j]
             for parse in self.lookup(nt1, nt2)]

        # dfs to generate all valid parse trees
        def gen_pt_dfs(start: int, end: int, target_nt: str) -> List[ParseTree]:
            # if it lies on diagonal, it's a leaf node
            if start == end:
                return [(target_nt, words[start])]
            # else it's not a leaf node
            parse_trees = []
            for i, k, j, nt1, nt2 in dp[start][end][target_nt]:
                nt1_parse_trees = gen_pt_dfs(i, k, nt1)
                nt2_parse_trees = gen_pt_dfs(k+1, j, nt2)
                parse_trees += [(target_nt, nt1_pt, nt2_pt)
                                for nt1_pt in nt1_parse_trees
                                for nt2_pt in nt2_parse_trees]
            return parse_trees

        return gen_pt_dfs(0, N-1, 'S')

    def cyk_parse_pp(self, words: List[str]) -> List[str]:
        """
        Parses the sentence using CNFGrammar.cyk_parse and pretty-prints
        the result

        :param words:   sentence to parse
        :return:        arrays of pretty-printed trees
        """

        # use preorder dfs to print the tree with indenting
        def preorder_dfs(root: ParseTree, indent: int = 0) -> str:
            tab = '\t'
            if len(root) == 2:
                return f'{tab*indent}[{root[0]} {root[1]}]'
            else:
                return f'{tab*indent}[{root[0]}\n' \
                       f'{preorder_dfs(root[1], indent+1)}\n' \
                       f'{preorder_dfs(root[2], indent+1)}]'

        return [preorder_dfs(tree) for tree in self.cyk_parse(words)]
