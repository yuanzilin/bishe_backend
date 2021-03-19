#include <bits/stdc++.h>

#define maxn 512
#define len 205

using namespace std;

typedef struct HP{
    int a[len];
    int hp_len;
}hp;


hp c[maxn][maxn];
int n,k;
int p,t;
int res;
hp cc,ans;

inline hp sum(hp aa,hp bb){
    memset(cc.a,0,sizeof cc.a);
    cc.hp_len=max(aa.hp_len,bb.hp_len);
    int x;
    for(int i=0;i<cc.hp_len;i++){
        cc.a[i]=aa.a[i]+bb.a[i]+x;
        x=cc.a[i]/10;
        cc.a[i]=cc.a[i]%10;
    }
    if(x)
        cc.a[cc.hp_len++]=x;
    return cc;
}

int main(){
    scanf("%d%d",&k,&n);
    p=n/k;//可以分成p个完整的部分
    res=n%k;//剩下的不完整部分有多长
    t=1<<k;
    c[0][0].a[0]=1;
    for(int i=1;i<t;i++){
        c[i][0].a[0]=c[i][i].a[0]=1;
        c[i][0].hp_len=c[i][i].hp_len=1;
    }
    for(int i=1;i<t;i++){
        for(int j=1;j<i;j++){
            c[i][j]=sum(c[i-1][j],c[i-1][j-1]);
        }
    }

    for(int i=2;i<=p;i++){
        if(i>t-1)
            break;
        ans=sum(ans,c[t-1][i]);
    }

    int pp=(1<<res)-1;
    for(int i=1;i<=pp;i++){
        if(p>t-1-i)
            break;
        ans=sum(ans,c[t-1-i][p]);
    }
    for(int i=ans.hp_len-1;i>=0;i--){
        printf("%d",ans.a[i]);
    }
}
