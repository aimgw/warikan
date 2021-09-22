#test.cppのプログラムをpython3で書いてみた
import heapq
import numpy as np

n = int(input())    #入力受け取り
a = np.array(list(map(int, input().split())))     #払った金額のリストを入力
a *= -1


S = np.sum(a)
ave = int(S/n*-1)

plus = []
minus = []
for i in range(n):
    if a[i]*-1 - ave > 100:
        heapq.heappush(plus, [a[i]*-1 - ave, i])
    elif ave - a[i]*-1 > 100:
        heapq.heappush(minus, [ave - a[i]*-1, i])

rtnarr = [[0]*n for i in range(n)]

while(len(plus) != 0 and len(minus) != 0):
    x = heapq.heappop(plus)
    y = heapq.heappop(minus)
    res = min(x[0], y[0])
    rtnarr[y[1]][x[1]] = rtnarr[y[1]][x[1]] + res
    if x[0] - res > 100:
        x[0] = x[0] - 100
        heapq.heappush(plus, x)
    if y[0] - res > 100:
        y[0] = y[0] - res
        heapq.heappush(minus, y)

print(rtnarr)




