from srcs.Obj import Obj


class Node:
    addr: list  # Liste des adresses des objs comportant un fait lié a facts
    cache: list  # list[3][dict] sauvegarde des derniers faits
    obj: Obj  # regles a appliquer
    facts: dict  # fait impliqué par les regles de objet

    def __init__(self, op, rules, c):
        addr = []
        obj = Obj(op, rules, c)
        facts = obj.get_result()
