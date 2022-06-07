
res_list = []

NO_OF_CHARS = 256


def badCharHeuristic(string, size):

    badChar = [-1] * NO_OF_CHARS

    for i in range(size):
        badChar[ord(string[i])] = i

    return badChar


def search(txt, pat):
    res_list = []
    if (txt == "" or pat == ""):
        print("Empty fields", "Fill out the fields")

    m = len(pat)
    n = len(txt)

    badChar = badCharHeuristic(pat, m)

    s = 0

    while (s <= n - m):
        j = m - 1

        while j >= 0 and pat[j] == txt[s + j]:
            j -= 1

        if j < 0:

            res_list.append(s+1)

            s += (m - badChar[ord(txt[s + m])] if s + m < n else 1)
        else:

            s += max(1, j - badChar[ord(txt[s + j])])

    return res_list
