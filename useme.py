#このコードをcolaboratoryにコピーして使ってください
import numpy as np
import heapq
from google.colab import auth
from oauth2client.client import GoogleCredentials
import gspread
import datetime

#認証の処理
auth.authenticate_user()
gc = gspread.authorize(GoogleCredentials.get_application_default())

#spreadsheetの取得、シートの指定
ss_url = ""     #####TODO spreadsheetのurlを入力してください####################################################
workbook = gc.open_by_url(ss_url)
worksheet = workbook.worksheet("シート3")   #####TODO 適宜シート名を変更してください################################

#人数の取得
n = worksheet.acell("A2").value
n = int(n)

#個人の出費の合計を計算
a = []
n = int(n)
idx = 3
for i in range(n):
    d = worksheet.col_values(idx)
    b = np.array(d[1:], dtype='int64')
    res = np.sum(b)
    a.append(res)
    idx = idx + 2

#総出費、平均の計算
a = np.array(a)
S = np.sum(a)
ave = int(S/n)
#a *= -1 #pythonのheapqはminimum_heapなので最大値を出力するために-1倍する

#貪欲法を行うための準備(heapqに値を格納)
plus = []
minus = []
for i in range(n):
    if a[i] - ave > 100:
        heapq.heappush(plus, [(a[i] - ave)*-1, i])
    elif ave - a[i] > 100:
        heapq.heappush(minus, [(ave - a[i])*-1, i])

#出力用の二次元配列の初期化
rtnarr = [[0]*n for i in range(n)]

#貪欲法の実行
while(len(plus) != 0 and len(minus) != 0):
    x = heapq.heappop(plus)
    y = heapq.heappop(minus)
    x[0] = x[0] * -1
    y[0] = y[0] * -1
    res = min(x[0], y[0])
    rtnarr[y[1]][x[1]] = rtnarr[y[1]][x[1]] + res
    if x[0] - res > 100:
        x[0] = x[0] - res
        x[0] = x[0] * -1
        heapq.heappush(plus, x)
    if y[0] - res > 100:
        y[0] = y[0] - res
        y[0] = y[0]*-1
        heapq.heappush(minus, y)

#出力用の名前配列の作成
name = []
col = 2
for _ in range(n):
    res = worksheet.cell(1, col).value
    name.append(res)
    col = col + 2

#出力用のシートの作成
d_today = datetime.date.today()
str_today = d_today.strftime('%Y/%m/%d')
output_sheet = 'output' + str_today   
workbook.add_worksheet(title=output_sheet, rows=100, cols=100)

#シートに入力(かなり力技)
#1行目に名前を出力
worksheet2 = workbook.worksheet(output_sheet)
celllst = worksheet2.range(1, 2, 1, 2+n)
for i in range(n):
    celllst[i].value = name[i]
worksheet2.update_cells(celllst)
#2行目以降　1列目に名前、　2列目以降にその人が払う金額を出力
for i in range(n):
    worksheet2.update_cell(i+2, 1, name[i])
    cell_list = worksheet2.range(i+2, 2, i+2, 2+n)
    for j in range(n):
        cell_list[j].value = str(rtnarr[i][j])
    worksheet2.update_cells(cell_list)

print('おわり！')