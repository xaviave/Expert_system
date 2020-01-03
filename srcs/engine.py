from copy import copy


def get_result(queries, facts):
    ret = ""
    print(facts)
    for i, q in enumerate(queries):
        print(q, facts[q])
        ret += f"{q} is {'True' if facts[q] == 1 else 'False'}{', ' if i < len(queries) - 1 else ''}"
    return ret


def check_nodes(rules_list, facts, tmp_facts, queries):
    """
        check if facts are the same
        check the nodes caches
        check if every queries are found
    """
    return True


def launch_engine(facts, queries, rules_list):
    print("TO DO:\n\t- create the cache]\n\t- find paradoxe")

    for q in queries:
        print(f"\nlaunch_engine for {q}")
        tmp_facts = copy(facts)
        for r in rules_list:
            if q in r.result_facts:
                facts = r.graph(tmp_facts, q)
                break
        """
        if check_nodes(rules_list, facts, tmp_facts, queries):
            facts = tmp_facts
            break
            """
    print(f"Queries: {queries}\nThe result {'are' if len(queries) > 1 else 'is'} {get_result(queries, facts)}")
    pass
