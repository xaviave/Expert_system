from termcolor import colored


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
            if len(rule) == 2:
                return ''
            elif tmp == 0:
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
            if self.op == '':
                return ''
            if rule.count('!') == 2:
                self.not_[1] = 1
                return rule[4]
            if '!' in rule:
                self.not_[1] = 1 if rule[2] == '!' else 0
                return rule[3]
            else:
                return rule[2] if len(rule) != 1 else 0

    @staticmethod
    def __check_fact(rule, fact):
        if fact == '':
            return
        elif isinstance(fact, CalculBool):
            return

        if isinstance(fact, str):
            if not str(fact).istitle():
                raise Exception(f"Line Bad formated: {rule}")
            return
        else:
            raise Exception(f"Line Bad formated: {rule}")

    def __init__(self, rule, id_):
        op_list = {'^': self.__or, '|': self.__xor, '+': self.__and, '': self.__pass}
        self.not_ = [0, 0]
        self.id = id_
        self.fact = self.__get_fact(True, rule)  # key of the fact dict
        self.op = self.__get_op(rule)
        self.op_func = op_list[self.op]
        self.fact2 = self.__get_fact(False, rule)  # rule[2] if len(rule) != 1 else 0
        self.__check_fact(rule, self.fact)
        self.__check_fact(rule, self.fact2)

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

    def __get_result_fact(self, facts):
        if isinstance(self.fact, CalculBool):
            fact = self.fact.get_result(facts)
        else:
            fact = facts[self.fact]
        return fact

    def __get_result_fact2(self, facts):
        if isinstance(self.fact2, CalculBool):
            fact2 = self.fact2.get_result(facts)
        else:
            fact2 = facts[self.fact2]
        return fact2

    def get_result(self, facts):
        fact = self.__get_result_fact(facts)
        fact2 = self.__get_result_fact2(facts)
        if self.not_[0] == 1:
            fact = self.__inverse(fact)
        if self.not_[1] == 1:
            fact2 = self.__inverse(fact2)
        print(f"op = {self.op}, fact {self.fact} = {fact}, fact2 {self.fact2} = {fact2}, func = {self.op_func(fact, fact2)}")
        return self.op_func(fact, fact2)

    def apply_result(self, facts, result_facts, result):
        if result == 0:
            facts[''] = -1
            return facts
        if isinstance(result_facts.fact, CalculBool):
            facts = result_facts.apply_result(facts, result_facts.fact,
                                              result if not result_facts.not_[0] else self.__inverse(result))
        else:
            facts[result_facts.fact] = result if not result_facts.not_[0] else self.__inverse(result)
        if isinstance(result_facts.fact2, CalculBool):
            facts = result_facts.apply_result(facts, result_facts.fact2,
                                              result if not result_facts.not_[1] else self.__inverse(result))
        else:
            facts[result_facts.fact2] = result if not result_facts.not_[1] else self.__inverse(result)
        facts[''] = -1
        return facts

    def return_facts(self):
        return f"{self.fact}{self.not_[0]}"

    def __str__(self):
        if self.op:
            return f"[{'!' if self.not_[0] else ''}{self.fact} {self.op} {'!' if self.not_[1] else ''}{self.fact2}]"
        else:
            return f"[{'!' if self.not_[0] else ''}{self.fact}]"
