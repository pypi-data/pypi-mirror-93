def build(arr, oper):
    def combine(a, b, oper):
        if oper == 'sum':
            return a + b
        elif oper == 'xor':
            return a ^ b
        elif oper == 'and':
            return a & b
        elif oper == 'or':
            return a | b
        elif oper == 'max':
            return max(a, b)
        elif oper == 'min':
            return min(a, b)
    n = len(arr)
    segt = [None] * (4 * n)
    def buildUtil(arr, v, l, r, segt, oper):
        if l == r:
            segt[v] = arr[l]
        else:
            mid = (l + r) // 2
            buildUtil(arr, 2 * v + 1, l, mid, segt, oper)
            buildUtil(arr, 2 * v + 2, mid + 1, r, segt, oper)
            segt[v] = combine(segt[2 * v + 1], segt[2 * v + 2], oper)
    buildUtil(arr, 0, 0, n - 1, segt, oper)
    return segt

def query(arr, l, r, segt, oper):
    def combine(a, b, oper, segt):
        if oper == 'sum':
            return a + b
        elif oper == 'xor':
            return a ^ b
        elif oper == 'and':
            return a & b
        elif oper == 'or':
            return a | b
        elif oper == 'max':
            return max(a, b)
        elif oper == 'min':
            return min(a, b)
    n = len(arr)
    def queryUtil(arr, v, sr, er, l, r, segt, oper):
        if l > er or r < sr:
            return 0
        if l <= sr and r >= er:
            return segt[v]
        mid = (sr + er) // 2
        ans1 = queryUtil(arr, 2 * v + 1, sr, mid, l, r, segt, oper)
        ans2 = queryUtil(arr, 2 * v + 2, mid + 1, er, l, r, segt, oper)
        return ans1 + ans2
    return queryUtil(arr, 0, 0, n - 1, l, r, segt, oper)

def update(arr, ind, val, segt, oper):
    def combine(a, b, oper, segt):
        if oper == 'sum':
            return a + b
        elif oper == 'xor':
            return a ^ b
        elif oper == 'and':
            return a & b
        elif oper == 'or':
            return a | b
        elif oper == 'max':
            return max(a, b)
        elif oper == 'min':
            return min(a, b)
    n = len(arr)
    def updateUtil(arr, v, ind, val, l, r, segt, oper):
        if l == r:
            segt[v] = val
            return
        mid = (l + r) // 2
        if ind <= mid:
            updateUtil(arr, 2 * v + 1, ind, val, l, mid, segt, oper)
        else:
            updateUtil(arr, 2 * v + 2, ind, val, mid + 1, r, segt, oper)
        segt[v] = combine(segt[2 * v + 1], segt[2 * v + 2], oper, segt)
    updateUtil(arr, 0, ind, val, 0, n - 1, segt, oper)
