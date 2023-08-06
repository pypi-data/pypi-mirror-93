import re


def convert(op, content, rep):
    op = op.upper()
    if str(type(content)) == "<class 'str'>":
        if op == "EMAIL":
            content = re.sub(r'([\w\.-]+)@([\w\.-]+)(\.[\w\.]+)', rep, content)
        elif op == "URL":
            content = re.sub(r'(http|ftp|https):\S+', rep, content)
        elif op == "ACCOUNT":
            if content.count('-') == 2:
                content = re.sub('[0-9]+-[0-9]+-[0-9]+', rep, content)
            elif content.count('-') == 3:
                content = re.sub('[0-9]+-[0-9]+-[0-9]+-[0-9]+', rep, content)
        elif op == "PHONE":
            content = re.sub(r'((\d{2}|\(\d{2}\)|\d{3}|\(\d{3}\))?(|-|\.)?(\d{3}|\d{4})(\s|-|\.)(\d{4}))',
                             rep, content)
        return content

    else:
        temp = content
        for i in range(len(content)):
            if op == "EMAIL":
                temp[i] = re.sub(r'([\w\.-]+)@([\w\.-]+)(\.[\w\.]+)', rep, temp[i]).strip()
            elif op == "URL":
                temp[i] = re.sub(r'(http|ftp|https):\S+', rep, temp[i]).strip()
            elif op == "ACCOUNT":
                if content[i].count('-') == 2:
                    temp[i] = re.sub('[0-9]+-[0-9]+-[0-9]+', rep, temp[i]).strip()
                elif content[i].count('-') == 3:
                    temp[i] = re.sub('[0-9]+-[0-9]+-[0-9]+-[0-9]+', rep, temp[i]).strip()
            elif op == "PHONE":
                temp[i] = re.sub(r'((\d{2}|\(\d{2}\)|\d{3}|\(\d{3}\))?(|-|\.)?(\d{3}|\d{4})(\s|-|\.)(\d{4}))',
                                 rep, temp[i]).strip()

        return list(filter(None, temp))
