def BP(S):
    n = len(S)
    bp = [0 for _ in range(n)]
    for i in range(1, n):
        bp_right = bp[i - 1]
        while bp_right and S[i] != S[bp_right]:
            bp_right = bp[bp_right - 1]
        if S[i] == S[bp_right]:
            bp[i] = bp_right + 1
        else:
            bp[i] = 0
    return bp


# Исполнений цикла while не более чем n => линейная сложность


def BPM(bp):
    n = len(bp)
    bpm = [0 for _ in range(n)]
    bpm[n - 1] = bp[n - 1]
    for i in range(1, n - 1):
        if bp[i] and bp[i] + 1 == bp[i + 1]:
            bpm[i] = bpm[bp[i] - 1]
        else:
            bpm[i] = bp[i]
    return bpm


def KMP(P, T):
    bpm = BPM(BP(P))
    m = len(P)
    n = len(T)
    k = 0
    for i in range(n):
        while k and P[k] != T[i]:
            k = bpm[k - 1]
        if P[k] == T[i]:
            k += 1
        if k == m:
            print(f"Вхождение с позиции {i - k + 1}")
            k = bpm[k - 1]


T = 'ABAABABAABAAB'

res = BPM(BP(T))
res2 = BP(T)
print(' '.join([a for a in T]))
print(' '.join([str(a) for a in res2]))
print(' '.join([str(a) for a in res]))
