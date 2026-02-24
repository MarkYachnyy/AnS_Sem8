def BS(S):
    n = len(S)
    bs = [0 for _ in range(n)]
    for i in reversed(range(n - 1)):
        bs_left = bs[i + 1]
        while bs_left and S[i] != S[n - bs_left - 1]:
            bs_left = bs[n - bs_left]
        if S[i] == S[n - bs_left - 1]:
            bs[i] = bs_left + 1
        else:
            bs[i] = 0
    return bs


def BSM(bs):
    n = len(bs)
    bsm = [0 for _ in range(n)]
    bsm[0] = bs[0]
    for i in reversed(range(1, n - 1)):
        if bs[i] and bs[i] + 1 == bs[i - 1]:
            bsm[i] = bsm[n - bs[i]]
        else:
            bsm[i] = bs[i]
    return bsm


def NS(bs):
    m = len(bs)
    ns = [-1 for _ in range(m)]
    for j in range(m - 1):
        if bs[j]:
            k = m - bs[j] - 1
            ns[k] = j
    return ns


def BR(bs):
    m = len(bs)
    br = [0 for _ in range(m)]
    curr_border = bs[0]
    k = 0
    while curr_border:
        while k < m - curr_border:
            br[k] = curr_border
            k += 1
        curr_border = bs[k]
    while k < m:
        br[k] = 0
        k += 1
    return br


def PositionList(S, nA):
    m = len(S)
    pl = [None for _ in range(nA)]
    for k in reversed(range(m)):
        ich = S[k]
        if not pl[ich]:
            pl[ich] = []
        pl[ich].append(k)
    return pl


def BadCharShift(pl, char_bad, pos_bad):
    if pos_bad < 0:
        return 1
    n_pos = -1
    pos_list = pl[char_bad]
    if pos_list:
        n_len = len(pos_list)
        for k in range(n_len):
            if pos_list[k] < pos_bad:
                n_pos = pos_list[k]
                break
    return pos_bad - n_pos


def GoodSuffixShift(nsx, br, pos_bad, m):
    if pos_bad == m - 1:
        return 1
    if pos_bad < 0:
        return m - br[0]
    copy_pos = nsx[pos_bad]
    if copy_pos >= 0:
        shift = pos_bad - copy_pos + 1
    else:
        shift = m - br[pos_bad]
    return shift


def str_to_int(S, A):
    char_pos = {}
    for i in range(len(A)):
        char_pos[A[i]] = i
    res = []
    for c in S:
        res.append(char_pos[c])
    return res


def BM(P, T, A, h=True):
    P = str_to_int(P, A)
    T = str_to_int(T, A)
    nA = len(A)
    pl = PositionList(P, nA)
    m = len(P)
    n = len(T)
    bs = BS(P)
    br = BR(bs)
    if h:
        bs = BSM(bs)
    nsx = NS(bs)
    n_text_r = m
    while n_text_r <= n:
        k = m - 1
        i = n_text_r - 1
        while k >= 0:
            if P[k] != T[i]:
                break
            k -= 1
            i -= 1
        if k < 0:
            print(f"Вхождение с позиции {i + 1}")

        n_shift = max(BadCharShift(pl, T[i], k), GoodSuffixShift(nsx, br, k, m))
        n_text_r += n_shift


T = 'ABAABABAABAAB'

res = NS(BS(T))
BM(P='BAAB', T=T, A='AB')
print(' '.join([a for a in T]))
print(' '.join([str(a) for a in res]))
