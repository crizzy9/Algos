
def lcs(seq1, seq2):
    m = len(seq1)
    n = len(seq2)

    L = [[0]*(n+1) for _ in range(m+1)]

    for i in range(m+1):
        for j in range(n+1):
            if i == 0 or j == 0:
                continue
            elif seq1[i-1] == seq2[j-1]:
                L[i][j] = L[i-1][j-1] + 1
            else:
                L[i][j] = max(L[i-1][j], L[i][j-1])
    return L[m][n]

str1 = "AGGTAB"
str2 = "GXTXAYB"

print(lcs(str1, str2))
print(lcs("ndnakshdqhnkancxnpojqhoiweyhnsakjcbzmnbkhqoh", "qouoieyatgbaskjfbmavdnqoiwunpbowiauhasd"))

