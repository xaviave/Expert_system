from srcs.Obj import CalculBool


class Node:
    addr: list  # Liste des adresses des objs comportant un fait lié a facts
    cache: list  # list[3][dict] sauvegarde des derniers faits
    save_form: str  # formula w/o parsing
    op: int  # 0 -> 'implies' | 1 -> 'if and only if'
    rules: CalculBool
    results: CalculBool
    facts: dict  # fait impliqué par les regles de objet

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

    def init_obj(self, op, rules):
        self.op = op
        if len(rules) != 2:
            raise Exception(f"The rules is not correctly formatted: {self.save_form}")
        if not all(rules):
            raise Exception(
                f"The rules is not correctly formatted: {self.save_form}, need at least one arg in each side of the operator")
        self.rules = self.__parse_rule(list(rules[0].strip()), 0)
        self.results = self.__parse_rule(list(rules[1].strip()), 0)

    def debug(self):
        print(f"{self.rules}{' => ' if not self.op else ' <=> '}{self.results}")

    def get_results_list(self):
        return "? je sais pas encore mais il faut une list de fait ['A', 'B']"

    def __init__(self, op, rules, c):
        self.save_form = c
        obj = self.init_obj(op, rules)
        self.debug()
        addr = []
        facts = self.get_results_list()
