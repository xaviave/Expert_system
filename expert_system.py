from srcs.parse import parse
from srcs.engine import launch_engine


if __name__ == "__main__":
    facts, queries, rules_list = parse()
    print(f"facts: {facts}\nqueries: {queries}")
    for rule in rules_list:
        print(rule)
    launch_engine(facts, queries, rules_list)
