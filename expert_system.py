from srcs.parse import parse


if __name__ == "__main__":
    tokens_list = parse()
    #print("Reunir les objs en une formules si ils donnent le meme fait\nex:\tB => A\nD ^ C => A\n --> (B) + D ^ C => A")
