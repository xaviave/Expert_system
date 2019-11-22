from srcs.Obj import Obj


def test_class_calcul_bool():
    test_dict = {"[A + B] => [C + H]": Obj(0, ["A+B", "(C+H)"], "A+B=>(C+H)"),
                 "[[D ^ C] | [[T + !T] + ![A + B]]] => [A]": Obj(0, ["(D^C)|T+!T+!(A+B)", "A"], "(D^C)|T+!T+!(A+B)=>A")}
    for i, test in enumerate(test_dict):
        res_obj = "".join([t.__str__() for t in test_dict[test].rule] + ([' => '] if not test_dict[test].op else [' <=> ']) + [t.__str__() for t in test_dict[test].result])
        if res_obj != test:
            print(f"Test {i}: KO | ( test : '{test_dict[test].save} -> {res_obj}')")
        else:
            print(f"Test {i}: OK")


test_class_calcul_bool()
