from termcolor import colored


#un graph avec composante connexe
class CalculBool:
    def __init__(self, rule, id_):
        op_list = {'^': self.__or, '|': self.__xor, '+': self.__and, '': self.__pass}
        # traiter le rule si !
        print(rule)
        self.id_ = id_
        self.fact = rule[0]
        self.op = rule[1] if len(rule) != 1 else ''
        self.op_func = op_list[self.op]
        self.fact2 = rule[2] if len(rule) != 1 else 0

    def __pass(self):
        return 1 if self.fact else 0

    def __or(self):
        return 1 if self.fact or self.fact2 else 0

    def __xor(self):
        if (self.fact and not self.fact2) or (not self.fact and self.fact2):
            return 1
        return 0

    def __and(self):
        return 1 if self.fact == 1 and self.fact2 == 1 else 0

    def result(self):
        return self.op

    def __str__(self):
        return f"[{self.fact} {self.op} {self.fact2}: id = {self.id_} ]"


class Obj:
    op: int  # 0 -> 'implies' | 1 -> 'if and only if'
    rule: str
    result: str

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

    @staticmethod
    def __create_obj(rule, id_):
        return CalculBool(rule, id_)

    def __parse_rule(self, form: list, id_):
        rule = form
        if len(form) == 1:
            #print(form)
            return CalculBool(form, id_)
        par = self.__find_parentheses(form)

        print(f"{id_} {form}")
        fill = 0
        j = 0
        form = []
        if par:
            for i, j in par.items():
                for x in range(fill, i):
                    form.append(rule[x])
                form.append(self.__create_obj(rule[i + 1:j], id_))
                fill = j
        else:
            print(f"rule = {rule}")
            form.append(self.__create_obj(rule[0:3], id_))
            j = 3
        if j != len(rule):
            for x in range(j, len(rule)):
                form.append(rule[x])
            print(form)
            form = self.__parse_rule(form, id_ + 1)
            print(form)
        return form
        #  List, chaque maillon est soit un fait soit un operateur | 1 sur 2 | si pair == error
        #  FAUT TRAITER TOUT CA ET LE RANGER QQL PART

    def __init__(self, op: int, rules: list, c: str):
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
        print("-------------------------------\n")

    def __str__(self):
        return f"{self.rule} {'=>' if not self.op else '<=>'} {self.result}"

    def get_result(self):
        return "? je sais pas encore mais il faut une list de fait ['A', 'B']"
