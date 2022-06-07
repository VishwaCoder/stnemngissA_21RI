

def to_bin(n, width=32):

    s = bin(n).replace("0b", "")
    return (("%0" + str(width) + "d") % int(s))


def neg(x):

    return 0b11111111111111111111111111111111 - x


def shift_or(text, pattern):
    found_pos = []
    m = len(pattern)
    n = len(text)
    neg0 = neg(0)

    B = {}
    for i in range(m):
        B[pattern[i]] = (B.get(pattern[i], 0) | (1 << i))
    B = {k: neg(B[k]) for k in B}

    a = neg0
    hit = (1 << (m - 1))

    notf = 0
    for i in range(n):
        a = (((a << 1) & neg0) | B.get(text[i], neg0))

        if a & hit == 0:
            found_pos.append((i - m + 2))
            notf = 1

    if notf == 0:
        print("\n Pattern Not Found ")
    return found_pos
