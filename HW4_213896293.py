import os
import random

ROWS = [
    "1234567890",
    "QWERTYUIOP",
    "ASDFGHJKL;",
    "ZXCVBNM,./",
    "          ",
]
""" בניית מטריצה והשמה לכל תו לדוגמה s" = (2, 1)" """
POS = {ch: (r, c) for r, row in enumerate(ROWS) for c, ch in enumerate(row) if ch != " "}
POS[" "] = (4, 4)
ARROWS = ("←", "→", "↑", "↓")
REPEAT_MARK = "•"
CASE_MARK = "/"

"""בונה רצף חיצים ממקש src למקש dst """
def _delta(src, dst, direction):
    (r1, c1), (r2, c2) = POS[src], POS[dst]
    dc, dr = c2 - c1, r2 - r1
    hor = (ARROWS[1] * dc) if dc > 0 else (ARROWS[0] * (-dc))
    ver = (ARROWS[3] * dr) if dr > 0 else (ARROWS[2] * (-dr))
    if direction == "H":
        return hor + ver
    else:
        return ver + hor


def encode(text, start_key, repeat_mark=REPEAT_MARK, seed = None):
    if seed is not None:
        random.seed(seed)

    direction = random.choice(("H", "V"))
    cur = start_key.upper()
    if cur not in POS:
        print("start key" + start_key + " not valid, start key initialized to 'A' ")
        cur = "A"
    out = []
    for ch in text:
        is_upper = ch.isalpha() and ch.isupper()
        if ch == "\n":
            out.append("\n")
        t = " " if ch == " " else ch.upper()
        if t in POS:
            if is_upper:
                out.append(CASE_MARK)
            if t == cur and t != " ":
                out.append(repeat_mark)
            else:
                move = _delta(cur, t, direction)
                out.append(move)
                if t != " ":
                    cur = t
    return " ".join(out), direction


def decode(cipher, start_key, repeat_mark=REPEAT_MARK):
    cur = start_key.upper()
    plain = []
    tokens = cipher.split()
    upper_next = False

    for tok in tokens:
        if tok == CASE_MARK:
            upper_next = True

        elif tok == repeat_mark:
            ch = cur
            if ch.isalpha():
                plain.append(ch.upper() if upper_next else ch.lower())
                upper_next = False
            else:
                plain.append(ch)
        else:
            dc = tok.count(ARROWS[1]) - tok.count(ARROWS[0])
            dr = tok.count(ARROWS[3]) - tok.count(ARROWS[2])
            r1, c1 = POS[cur]
            r2, c2 = r1 + dr, c1 + dc

            if (r2, c2) == POS[" "]:
                plain.append(" ")
            else:
                ch = ROWS[r2][c2]
                if ch.isalpha():
                    plain.append(ch.upper() if upper_next else ch.lower())
                    upper_next = False
                else:
                    plain.append(ch)
                cur = ch
    return "".join(plain)

def encode_file(input_path, start_key, seed=None):
    try:
        with open(input_path) as f:
            text = f.read()
    except FileNotFoundError:
        print(input_path + " not found")
        return None, None
    cipher, direction = encode(text, start_key=start_key, seed=seed)
    base, ext = os.path.splitext(input_path)
    output_path = base + "_ciphered" + ext

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(cipher)
    print(f"Encoded '{input_path}' -> '{output_path}' (direction={direction})")
    return output_path, direction

def decode_file(input_path, start_key):
    try:
        with open(input_path) as f:
            cipher = f.read()
    except FileNotFoundError:
        print(input_path + " not found")
        return None
    plain = decode(cipher, start_key=start_key)
    base, ext = os.path.splitext(input_path)
    output_path = base.split('_')[0] + "_deciphered" + ext

    with open(output_path, "w") as f:
        f.write(plain)
    print(f"Decoded '{input_path}' -> '{output_path}'")
    return output_path

# encode_file("test/harryPotter.txt", "p")
# decode_file("test/harryPotter_ciphered.txt", "p")
