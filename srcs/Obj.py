from termcolor import colored


#un graph avec composante connexe
class CalculBool:
    id: int  # id of the Obj
    not_: list
    fact: dict  # key = Fact | item = 1 if NOT
    op: str  # char of the operator => use in the print
    # op_func: pointer on the operator function
    fact2: dict  # key = Fact | item = 1 if NOT

    @staticmethod
    def __get_op(rule: list):
        """
        :param rule: list
        :return: the operator in the rule, determine the calculus function
        """
        if '!' in rule:
            tmp = rule.index('!')
            if tmp == 0:
                return rule[2]
            else:
                return rule[1]
        else:
            return rule[1] if len(rule) != 1 else ''

    def __get_fact(self, nu: bool, rule: list):
        """
        :param nu: False if first fact | True if second fact
        :param rule: list de len de 3 a 5 avec 2 fait un op et optionnellement 1 ou 2 !
        :return: the fact
        """
        if nu:
            if rule[0] == '!':
                self.not_[0] = 1
                return rule[1]
            else:
                return rule[0]
        else:
            if rule.count('!') == 2:
                self.not_[1] = 1
                return rule[4]
            if '!' in rule:
                self.not_[1] = 1
                return rule[3]
            else:
                return rule[2] if len(rule) != 1 else 0

    def __init__(self, rule, id_):
        op_list = {'^': self.__or, '|': self.__xor, '+': self.__and, '': self.__pass}
        self.not_ = [0, 0]
        self.id = id_
        self.fact = self.__get_fact(True, rule)  # key of the fact dict
        self.op = self.__get_op(rule)
        self.op_func = op_list[self.op]
        self.fact2 = self.__get_fact(False, rule)  # rule[2] if len(rule) != 1 else 0

    @staticmethod
    def __inverse(nu):
        if nu == 2:
            return 2
        else:
            return 0 if nu else 1

    @staticmethod
    def __pass(fact, fact2):
        # check if undefined
        return 1 if fact else 0

    @staticmethod
    def __or(fact, fact2):
        # check if undefined
        return 1 if fact or fact2 else 0

    @staticmethod
    def __xor(fact, fact2):
        # check if undefined
        if (fact and not fact2) or (not fact and fact2):
            return 1
        return 0

    @staticmethod
    def __and(fact, fact2):
        # check if undefined
        return 1 if fact == 1 and fact2 == 1 else 0

    def result(self, facts):
        fact = facts[self.fact]
        fact2 = facts[self.fact2]
        if self.not_[0] == 1:
            fact = self.__inverse(fact)
        if self.not_[1] == 1:
            fact2 = self.__inverse(fact2)
        return self.op_func(fact, fact2)

    def __str__(self):
        if self.op:
            return f"[{'!' if self.not_[0] else ''}{self.fact} {self.op} {'!' if self.not_[1] else ''}{self.fact2}]"
        else:
            return f"[{'!' if self.not_[0] else ''}{self.fact}]"


class Obj:
    op: int  # 0 -> 'implies' | 1 -> 'if and only if'
    rule: str
    result: str

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
            raise Exception(f"This line is bad formatted {self.save}")
        # error here when push if !
        """
        if rule[:op].count('!') > 1 or rule[op:].count('!') > 1:
            print(rule[:op].count('!'), rule[:op], rule[op:].count('!'), rule[op:])
            raise Exception(f"This line is bad formatted {self.save}, many following '!' isn't allowed")
        """
        start = op - 1
        end = op + 2
        if start > 0 and rule[start - 1] == '!':
            start -= 1
        if end < len(rule) - 1 and rule[end] == '!':
            end += 1
        print(rule)
        if end > len(rule) or start < 0:
            raise Exception(f"This line is bad formatted {self.save}")
        return start, end + 1

    def __parse_rule(self, form: list, id_):
        if len(form) == 1:
            return [CalculBool(form, id_)]
        par = self.__find_parentheses(form)
        j = 0
        fill = 0
        rule = form
        form = []
        if par:
            # ne prend que la premiere op de la parenthese, renvoyer dans _parse_rule -> 1.
            i = min(par, key=par.get) + 1
            j = par[min(par, key=par.get)] - 1
            for x in range(fill, i):
                form.append(rule[x])
            #  1. form.append(self.__create_obj(rule[i + 1:j], id_))
            print(rule[i:j])
            form.append(self.__parse_rule(rule[i:j], id_))
            fill = j
        else:
            if len(rule) == 3:
                form.append(self.__create_obj(rule, id_))
                return form
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
        print(f"form at the end {form} | {id_}")
        return form if len(form) == 1 else self.__parse_rule(form, id_ + 1)

    def __init__(self, op: int, rules: list, c: str):
        print(op, rules, c)
        self.save = c
        print(colored("NEED PARSING RULE & RESULT", 'red', attrs=['bold']), c)
        self.op = op
        if len(rules) != 2:
            raise Exception(f"The rules is not correctly formatted: {c}")
        if not all(rules):
            raise Exception(f"The rules is not correctly formatted: {c}, need at least one arg in each side of the operator")
        self.rule = self.__parse_rule(list(rules[0].strip()), 0)
        for s in self.rule:
            print(s)
        self.result = self.__parse_rule(list(rules[1].strip()), 0)
        for s in self.result:
            print(s)
        print("-------------------------------\n")

    def __str__(self):
        return f"{[s for s in self.rule]}{' => ' if not self.op else ' <=> '}{[s for s in self.result]}"

    def get_result(self):
        return "? je sais pas encore mais il faut une list de fait ['A', 'B']"
