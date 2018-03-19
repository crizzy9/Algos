def common_ancestor(pairs, ind1, ind2):
    ans1 = get_all_ancestors(pairs, ind1)
    ans2 = get_all_ancestors(pairs, ind2)
    print(ans1, ans2)


def get_all_ancestors(pairs, ind):
    inds = set()
    inds.add(ind)
    while True:
        ans = set()
        for pair in pairs:
            if pair[1] in inds:
                ans.add(pair[0])
        if not ans:
            break
        inds.union(ans)

    return inds


    oldans = set(ans)
    for pair in pairs:
        if ind == pair[1]:
            ans.add(pair[0])
    # if no new anscestors added break
    print(ans)
    if oldans != ans:
        for a in ans:
            get_all_ancestors(pairs, ans, a)

parent_child_pairs = [
    (1, 3), (2, 3), (3, 6), (5, 6),
    (5, 7), (4, 5), (4, 8), (8, 9)
]

common_ancestor(parent_child_pairs, 6, 9)

