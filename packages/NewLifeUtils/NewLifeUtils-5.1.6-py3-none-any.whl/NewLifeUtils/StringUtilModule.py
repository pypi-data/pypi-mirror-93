import re


def remove_csi(text):
    return (
        re.sub(
            r"\\x1[bB]\[[\d;]*[a-zA-Z]",
            "",
            text.encode("unicode_escape").decode(),
        )
        .encode()
        .decode("unicode_escape")
    )


def screate(string, size=10, insert="r", filler_symbol=" "):
    calcstreeng = remove_csi(string)

    spaces = str(filler_symbol) * (size - len(calcstreeng))
    if insert == "r":
        return string + spaces
    if insert == "l":
        return spaces + string


def sslice(text, chunk_size):
    text = str(text)
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]


def parse_args(readed):
    # [\'][a-zA-ZА-Яа-я\d\s[\]{}()\\\.\":;,-]*[\']|\b[a-zA-Z\d]+
    # [\"\'][a-zA-ZА-Яа-яЁё\d\s[\]{}()@\\\.:;,-]*[\"\']|[a-zA-ZA-ZА-Яа-яЁё\d\.[\]{}()@\\\.:;,-]+
    # [\"][a-zA-ZА-Яа-яЁё\d\s[\]{}()@\\\.:;,\'-]*[\"]|[a-zA-ZA-ZА-Яа-яЁё\d\.[\]{}()@\\\.:;,\'-]+
    # [\"][a-zA-ZА-Яа-яЁё\d\s[\]{}()@\\\.:;,\'-/]*[\"]|[a-zA-ZA-ZА-Яа-яЁё\d\.[\]{}()@\\\.:;,\'-/]+
    # [\"][a-zA-ZА-Яа-яЁё\d\s[\]{}()@#_=%?\*\\\.:;,\'-/]*[\"]|[a-zA-ZA-ZА-Яа-яЁё\d\.[\]{}()@\\\.:;,\'-/]+
    # [\"][a-zA-ZA-ZА-Яа-яЁё\d.[\]{}()@\\:;,\'\-\/!?#$%^&*_+№\d]*[\"]|[a-zA-ZA-ZА-Яа-яЁё\d.[\]{}()@\\:;,\'\-\/!?#$%^&*_+№]+
    # [\"][a-zA-ZA-ZА-Яа-яЁё\d.[\]{}()<>@\\:;,\'\-\/!?#$%^&*_+№\d]*[\"]|[a-zA-ZA-ZА-Яа-яЁё\d.[\]{}()@\\:;,\'\-\/!?#$%^&*_+№<>]+ (NOW)

    res = re.findall(
        r"[\"][a-zA-ZA-ZА-Яа-яЁё\d.[\]{}()<>@\\:;,\'\-\/!?#$%^&*_+№\d]*[\"]|[a-zA-ZA-ZА-Яа-яЁё\d.[\]{}()@\\:;,\'\-\/!?#$%^&*_+№<>]+",
        readed,
        re.MULTILINE,
    )
    res2 = []
    for item in res:
        res2.append(re.sub(r"\B'|\b'", "", item))
    res = [x for x in res2 if x != ""]
    if len(res) == 0:
        return {"command": "", "param": [], "paramCount": 0, "split": []}
    if len(res) == 1:
        return {"command": res[0], "param": [], "paramCount": 0, "split": [res[0]]}
    else:
        return {
            "command": res[0],
            "param": res[1:],
            "paramCount": len(res[1:]),
            "split": res,
        }
