import re


def convert(op, content, rep):
    op = op.upper()
    tmp = content.splitlines()
    tmp = list(filter(None, tmp))
    temp = tmp
    for i in range(len(tmp)):
        if op == "EMAIL":
            temp[i] = re.sub(r'([\w\.-]+)@([\w\.-]+)(\.[\w\.]+)', rep, temp[i]).strip()
        elif op == "URL":
            temp[i] = re.sub(r'(http|ftp|https):\S+', rep, temp[i]).strip()
        elif op == "NUMBER":
            temp[i] = re.sub('[0-9]+-[0-9]+-[0-9]+(-[0-9]+)?', rep, temp[i]).strip()
        elif op == "BRACKET":
            temp[i] = re.sub(r'[<{(【「〖\[].*[>)}】」〗\]]', rep, temp[i]).strip()

    return list(filter(None, temp))
