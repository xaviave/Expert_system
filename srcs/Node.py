import re

from srcs.CalculBool import CalculBool


class Node:
    node_id: int = 0
    addr: list  # Liste des adresses des objs comportant un fait lié a facts
    cache: list  # list[3][dict] sauvegarde des derniers faits
    save_form: str  # formula w/o parsing
    op: int  # 0 -> 'implies' | 1 -> 'if and only if'
    rules: CalculBool
    results: CalculBool
    facts: list  # fait impliqué par les regles de objet
    rule_facts: list
    result_facts: list
    only_facts: list

    @staticmethod
    def __create_obj(rule, id_):
        return CalculBool(rule, id_)

    @staticmethod
    def __find_parentheses(s):
        stack = []
        parentheses_locs = {}
        for i, c in enumerate(s):
            if c == '(':
                stack.append(i)
            elif c == ')':
                try:
                    parentheses_locs[stack.pop()] = i + 1
                except IndexError:
                    raise IndexError(f"Too many close parentheses at index {i}")
        if stack:
            raise IndexError(f"No matching close parenthesis to open parenthesis at index {stack.pop()}")
        return parentheses_locs

    def __priorities_handler(self, rule: list):
        """
        create some priority with 1. '+' 2. '|' 3. '^'

        :param rule: list of CalculBool and value to treat with priorities
        :return: start and end coord of the part of the rule list to handle
        """
        if '+' in rule:
            op = rule.index('+')
        elif '|' in rule:
            op = rule.index('|')
        elif '^' in rule:
            op = rule.index('^')
        else:
            raise Exception(f"This line is bad formatted {self.save_form}")
        start = op - 1
        end = op + 2
        if start > 0 and rule[start - 1] == '!':
            start -= 1
        if end < len(rule) - 1 and rule[end - 1] == '!':
            end += 1
        if end > len(rule) or start < 0:
            raise Exception(f"This line is bad formatted {self.save_form}")
        return start, end

    def __parse_rule(self, form: list, id_):
        if len(form) == 1:
            return CalculBool(form, id_)
        par = self.__find_parentheses(form)
        j = 0
        fill = 0
        rule = form
        form = []
        if par:
            i = min(par, key=par.get) + 1
            j = par[min(par, key=par.get)] - 1
            for x in range(fill, i - 1):
                form.append(rule[x])
            form.append(self.__parse_rule(rule[i:j], id_ + 1))
            j += 1
        else:
            if len(rule) in range(2, 3) and rule[0] == '!' and rule[1].istitle():
                return self.__create_obj(rule, id_)
            start, end = self.__priorities_handler(rule)
            for x in range(fill, start):
                form.append(rule[x])
            if end == len(rule) - 1:
                form.append(self.__create_obj(rule[start:], id_))
                j = len(rule)
            else:
                form.append(self.__create_obj(rule[start:end], id_))
                j = end
        if j != len(rule):
            for x in range(j, len(rule)):
                form.append(rule[x])
            form = self.__parse_rule(form, id_ + 1)
            if isinstance(form, CalculBool):
                return form
        return form[0] if len(form) == 1 else self.__parse_rule(form, id_ + 1)

    def init_obj(self, rules):
        if len(rules) != 2:
            raise Exception(f"The rules is not correctly formatted: {self.save_form}")
        if not all(rules):
            raise Exception(
                f"The rules is not correctly formatted: {self.save_form}, need at least one arg in each side of the operator")
        self.rules = self.__parse_rule(list(rules[0].strip()), 0)
        self.results = self.__parse_rule(list(rules[1].strip()), 0)

    def __str__(self):
        return f"Node_id: {self.node_id} = {self.rules}{' => ' if not self.op else ' <=> '}{self.results}"

    def get_results_list(self, result):
        if len(result) > 2:
            self.only_facts = []
        else:
            self.only_facts = self.results.return_facts()

    def get_all_facts(self, rules):
        self.facts = list(set(re.findall(r"[A-Z]", self.save_form)))
        self.rule_facts = list(set(re.findall(r"[A-Z]", rules[0])))
        self.result_facts = list(set(re.findall(r"[A-Z]", rules[1])))

    def __init__(self, op, rules, c):
        self.save_form = c
        self.op = op
        self.init_obj(rules)
        self.addr = []
        self.get_all_facts(rules)
        self.get_results_list(rules[1])

    def merge_node(self, new_rules: list):
        for i, n_rule in enumerate(new_rules):
            formula = [self.rules, '|']
            if self.only_facts[1] == 1:
                formula.insert(0, '!')
            if n_rule.only_facts[1] == 1:
                formula.append('!')
            formula.append(n_rule.rules)
            self.rules = CalculBool(formula, -i)

    def return_addr_id(self):
        return [i.node_id for i in self.addr]

    def graph(self, facts, query):
        from termcolor import colored
        """
            Enter in the first addr if needed else just calcul the Boolean with the facts
        """
        print(colored(f"start graph, query = {query} | {self}", 'red'))
        if query not in self.result_facts:
            print(f"Enter apply result, facts = {facts}, result = {self.rules.get_result(facts)}")
            self.results.apply_result(facts, self.results, self.rules.get_result(facts))
            print(colored(f"end of graph no query | {self}\n", 'green'))
            return facts
        tmp_query = facts[query]
        print(f"len = {len(self.addr)} | self = {self}")
        #if len(self.addr) <= 1:
        for a in self.addr:
            print(f"a = {a} | self = {self}")
            for second_query in a.rule_facts:
                facts = a.graph(facts, second_query)
            result = self.rules.get_result(facts)
            facts = self.results.apply_result(facts, self.results, result)
            if facts[query] != tmp_query:
                print(colored(f"check if paradoxes here | {self}", 'yellow'))
                return facts
        print(colored(f"end of graph | {self}\n", 'blue'))
        return facts
