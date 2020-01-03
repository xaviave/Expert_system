from copy import copy


def get_result(queries, facts):
    ret = ""
    for i, q in enumerate(queries):
        ret += f"{q} is {'True' if facts[q] == 1 else 'False'}{', ' if i < len(queries) - 1 else ''}"
    return ret


def launch_engine(facts, queries, rules_list):
    for q in queries:
        tmp_facts = copy(facts)
        for r in rules_list:
            if q in r.result_facts:
                facts = r.graph(tmp_facts, q)
                break
    print(f"The queries are : {queries}\nThe result {'are' if len(queries) > 1 else 'is'}: {get_result(queries, facts)}")
