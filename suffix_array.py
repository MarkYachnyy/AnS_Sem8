import math


def counting_sort(A, k):
    n = len(A)
    C = [0 for _ in range(k)]
    B = [0 for _ in range(n)]
    for j in range(n):
        C[A[j]] += 1
    for i in range(1, k):
        C[i] += C[i - 1]
    for j in reversed(range(n)):
        B[C[A[j]] - 1] = A[j]
        C[A[j]] = C[A[j]] - 1

    return B


def str_to_int(S, A):
    char_pos = {}
    for i in range(len(A)):
        char_pos[A[i]] = i
    res = []
    for c in S:
        res.append(char_pos[c] + 1)
    return res


def radix_sort(A, kDig, skip_dig=0):
    n = len(A)
    B = [i for i in range(n)]
    nDig = len(A[0])
    for k in range(skip_dig, nDig):
        C = [0 for _ in range(kDig)]
        for j in range(n):
            C[A[B[j]][-(k + 1)]] += 1
        for i in range(1, kDig):
            C[i] += C[i - 1]
        B_temp = [0 for _ in range(n)]
        for j in reversed(range(n)):
            B_temp[C[A[B[j]][-(k + 1)]] - 1] = B[j]
            C[A[B[j]][-(k + 1)]] -= 1
        B = B_temp

    return B


def suffix_array(S, A):
    S_int = str_to_int(S, A) + [0]
    n = len(S_int)
    nA = len(A) + 1
    P = radix_sort([[s] for s in S_int], nA)
    C = [0 for _ in range(n)]
    # Нулевая фаза
    curr_c = 0
    for i in range(1, n):
        if S_int[P[i]] > S_int[P[i - 1]]:
            curr_c += 1
        C[P[i]] = curr_c
    for k in range(1, int(math.ceil(math.log2(n)))):
        P = [(p - 2 ** (k - 1)) % n for p in P]
        pairs = [(C[i], C[(i + 2 ** (k-1)) % n]) for i in range(n)]
        pairs2 = [None for _ in range(n)]
        for i in range(n):
            pairs2[i] = (C[P[i]], C[(P[i] + 2 ** (k - 1)) % n])
        P2 = radix_sort(pairs2, n, skip_dig=1)
        P = [P[P2[i]] for i in range(n)]
        curr_c = 0
        for i in range(1, n):
            if pairs[P[i]] > pairs[P[i - 1]]:
                curr_c += 1
            C[P[i]] = curr_c

    suffs = [S[-1]]
    for i in range(2, n):
        suffs.insert(0, S[-i]+suffs[0])
    return [suffs[P[i]] for i in range(1, n)]



print('ACBABAC-1')
print(suffix_array('ACBABAC', 'ABC'))