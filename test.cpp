#include<bits/stdc++.h>
using namespace std;

/*
    キャンプ時の割り勘プログラム
    input 
        n : 人数
        a_i : その人が払った金額(vector)
    
    output
        二次元vector or log
    
    algorithm
        一番払っていない人が一番払っている人に払えるだけ払うということを繰り返し行う貪欲法
        (priority_queueで払った金額を管理)
*/

using P = pair<int, int>;

int main(void){
    //データを受け取ります
    int n;
    cin >> n;
    vector<int> a(n);
    for(int i=0; i<n; ++i) {
        cin >> a[i];
    }

    //総額計算
    int sum = 0;
    for(int x : a) {
        sum += x;
    }
    int ave = sum / n;

    //平均との大小でわけて、priority_queueに格納
    priority_queue<P> plus, minus;
    for(int i=0; i<n; ++i) {
        if(a[i] > ave) {
            int res = a[i] - ave;
            plus.push(make_pair(res, i));
        } else if(ave > a[i]) {
            int res = ave - a[i];
            minus.push(make_pair(res, i));
        }
    }

    //貪欲法の実施
    vector<vector<int>> ans(n, vector<int>(n));
    while(!plus.empty() && !minus.empty())
    {
        auto [loan, recipt] = plus.top();
        plus.pop();
        auto [debt, creditor] = minus.top();
        minus.pop();
        // printf("%d %d\n", loan, debt);
        int res = min(loan, debt);
        ans[creditor][recipt] += res;
        if(loan - res > 100) {
            //100円以上まだあるなら追加
            loan -= res;
            plus.push(make_pair(loan, recipt));
        }
        if(debt - res > 100) {
            debt -= res;
            minus.push(make_pair(debt, creditor));
        }
    }

    for(int i=0; i<n; ++i) {
        for(int j=0; j<n; ++j) {
            cout << ans[i][j] << " ";
        }
        cout << endl;
    }
    return 0;
}