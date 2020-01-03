from srcs.parse import parse
from srcs.engine import launch_engine


if __name__ == "__main__":
    facts, queries, rules_list = parse()
    launch_engine(facts, queries, rules_list)
