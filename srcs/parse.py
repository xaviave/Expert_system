import re
import sys
import argparse

from srcs.Node import Node
from termcolor import colored
from srcs.CalculBool import CalculBool


def __get_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="Enter the propositionnal file", type=str)
    parser.add_argument("-v", "--verbosity", help="Increase output verbosity")
    parser.add_argument("-i", "--interactive", help="Allow ")
    args = parser.parse_args()
    print(f"{colored(args, 'red')}\n")
    return args


def __clean_file(file: str) -> list:
    s_file = [s for s in file.split('\n') if s.split()]
    command_list: list = []
    for i, s in enumerate(s_file):
        if len(s) < 2:
            raise Exception(f"Line must have 2 charateres, here: {len(s)} '{s}'")
        elif s.find('#') == -1 and s.find('=') == -1 and s.find('?') == -1:
            raise Exception(f"Bad char in this line: '{s}'")
        if s.find('#') and s[:s.find('#')]:
            command_list.append(s[:s.find('#')].strip() if s.find('#') > 0 else s.strip())
    return command_list


def __get_stdin() -> list:
    file: str = ""
    for line in sys.stdin:
        file += line
    return __clean_file(file)


def __get_file(name="") -> list:
    try:
        with open(name, 'r') as file:
            file = file.read()
            return __clean_file(file)
    except FileNotFoundError:
        raise Exception(f"File doesn't exist or is not on this directory: {name[:(name.find('/') + 1)] if name.find('/') else './'}")


def __check_char(command_list: list):
    t: list = []
    auth_char = re.compile(r"[A-Z()>=+!|^?\s]+")
    for c in command_list:
        if not re.fullmatch(auth_char, c):
            raise Exception(f"Bad character in this line: {c}, characters allowed are : [A-Z()<>=+!|^?\\s]")
        if (c.count('=') == 1) == (c.count('?') == 1):
            raise Exception(f"Need just one '=' or '?', line: {c}")


def __get_facts_name(command_list: list) -> dict:
    tmp = []
    letters = re.compile("[A-Z]")
    for c in command_list:
        tmp = tmp + letters.findall(c)
    facts: dict = {f: 0 for f in list(set(tmp))}
    return facts


def __check_rules(command_list: list):
    i = 0
    rules_list: list = []
    for i, c in enumerate(command_list):
        c = re.sub(r"\s", "", c)
        if '=>' in c:
            rules_list.append(Node(0, c.split('=>'), c))
        else:
            return rules_list, command_list[i:]
    raise Exception("Errors: No fact's init and No queries")


def __check_facts(command_list: list, facts: dict) -> list:
    if len(command_list[0]) < 2:
        return command_list[1]
    if not command_list[0].count('='):
        raise Exception(f"This line : '{command_list[0]}' is a query, not a fact's init (query is always after fact's init)" if command_list[0].count('?') else f"Fact's init is not correctly formatted: {command_list[0]}")
    if re.findall(r"[()<>+!|^?]]*", command_list[0]):
        raise Exception(f"Bad character in the line {command_list[0]}, characters allowed are : [=A-Z]")
    for tmp in list(command_list[0][1:]):
        facts[tmp] = 1
    return command_list[1:]


def __check_queries(command_list: list, facts: dict):
    if not len(command_list) or command_list[0] == '?':
        print("No queries, nothing to show")
        raise SystemExit(0)
    if re.findall(r"\?[A-Z]*", command_list[0]) != [command_list[0]]:
        raise Exception(f"The query is not correctly formatted: {command_list[0]}")
    queries = list(command_list[0][1:])
    return queries, command_list[1:]


def __check_command_list(command_list: list):
    lst: list = list(command_list)
    __check_char(command_list)
    rules_list, lst = __check_rules(command_list)
    facts = __get_facts_name(command_list)
    lst = __check_facts(lst, facts)
    queries, lst = __check_queries(lst, facts)
    if len(lst):
        print(f"Facts and queries are init so all these lines a ignored: {lst}")
    return facts, queries, rules_list


def __opti_nodes(rules_list) -> list:
    same_rules = {}
    del_nodes = []
    for i, rules in enumerate(rules_list):
        if len(rules.only_facts) > 1:
            try:
                same_rules[rules.only_facts].append(rules)
            except Exception:
                same_rules[rules.only_facts] = [rules]
    for key, items in same_rules.items():
        for i, rules in enumerate(rules_list):
            if len(items) > 1 and rules == items[0]:
                rules_list[i].merge_node(items[1:])
                del_nodes += items[1:]
    rules_list = [x for x in rules_list if x not in del_nodes]
    return rules_list


def __link_nodes(rules_list: list):
    for rule in rules_list:
        for r in rules_list:
            if rule.node_id != r.node_id:
                link = set(rule.facts) & set(r.result_facts)
                if link:
                    rule.addr.append(r)


def parse():
    args = __get_arg()
    command_list = __get_file(args.file) if args.file else __get_stdin()
    facts, queries, rules_list = __check_command_list(command_list)
    if not all([len(facts), len(queries), len(rules_list)]):
        raise Exception("Missing Facts, queries or rules")
    rules_list = __opti_nodes(rules_list)
    for i, r in enumerate(rules_list):
        r.node_id = i
    print("TO DO:\n\t- create the cache\n\t- add facts in the op_func calculus\n\t- wait list in backward chaining")
    __link_nodes(rules_list)
    return facts, queries, rules_list
