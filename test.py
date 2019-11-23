from srcs.Node import Node


def good_test_class_calcul_bool():
    good_test_dict = {
        "[W] => [Z]": Node(0, ["W", "Z"], "W=>Z"),
        "[A + B] => [I]": Node(0, ["A+B", "I"], "A+B=>C"),
        "[[A] + [!B]] => [C]": Node(0, ["(A)+(!B)", "C"], "(A)+(!B)=>C"),
        "[A + B] => [C + H]": Node(0, ["A+B", "(C+H)"], "A+B=>(C+H)"),
        "[[D ^ C] | [[T + !T] + ![A + B]]] => [A]": Node(0, ["(D^C)|T+!T+!(A+B)", "A"], "(D^C)|T+!T+!(A+B)=>A"),
        "[[[[[A + B] + C] | D] | [B + D]] | [![C | D] + A]] => [G]": Node(0, ["((A+B+C|D)|B+D)|!(C|D)+A", "G"], "((A+B+C|D)|B+D)|!(C|D)+A=>G"),
                 }

    print("Good test:")
    for i, test in enumerate(good_test_dict):
        res_obj = str(good_test_dict[test].rules) + (' => ' if not good_test_dict[test].op else ' <=> ') + str(good_test_dict[test].results)
        if res_obj != test:
            print(f"\tTest {i}: KO | ( test : '{good_test_dict[test].save_form} -> {test} != {res_obj}')")
        else:
            print(f"\tTest {i}: OK")


def bad_test_class_calcul_bool():
    print("\nBad test:")
    try:
        Node(0, ["W", ""], "W=>")
    except Exception:
        print("\tTest 1: OK")
    else:
        print("\tTest 1: KO")

    try:
        Node(0, ["WX", "Z"], "WX=>Z")
    except Exception:
        print("\tTest 2: OK")
    else:
        print("\tTest 2: KO")

    try:
        Node(0, ["", ""], "")
    except Exception:
        print("\tTest 3: OK")
    else:
        print("\tTest 3: KO")

    try:
        Node(0, ["W+", "Z"], "W+=>Z")
    except Exception:
        print("\tTest 4: OK")
    else:
        print("\tTest 4: KO")

    try:
        Node(0, ["W", ""], "W=>Z")
    except Exception:
        print("\tTest 5: OK")
    else:
        print("\tTest 5: KO")

    try:
        Node(0, ["", "Z"], "W=>Z")
    except Exception:
        print("\tTest 6: OK")
    else:
        print("\tTest 6: KO")

    try:
        Node(0, ["W++A", "Z"], "W++A=>Z")
    except Exception:
        print("\tTest 7: OK")
    else:
        print("\tTest 7: KO")

    try:
        Node(0, ["(W", "Z"], "(W=>Z")
    except Exception:
        print("\tTest 8: OK")
    else:
        print("\tTest 8: KO")


if __name__ == "__main__":
    good_test_class_calcul_bool()
    bad_test_class_calcul_bool()
