#include <bits/stdc++.h>

using namespace std;

#define maxn 10005

int n,k;
int l[maxn];
double input[maxn];

bool judge(int x){
    int ans=0;
    for(int i=0;i<n;i++){
        ans+=l[i]/x;
    }
    return ans>=k;
}

int main(){
    scanf("%d%d",&n,&k);
    int max_l=0;
    for(int i=0;i<n;i++){
        scanf("%lf",&input[i]);
        l[i]=input[i]*100;
        max_l=max(l[i],max_l);
    }
    sort(l,l+n);
    int left=0,right=max_l;
    int max_ans=0;
    int mid=0;

        while(left<=right){
            int ans=0;
            mid=(left+right)/2;
            if(mid==0){
                printf("0.00");
                break;
            }
            for(int i=0;i<n;i++){
                ans+=l[i]/mid;
            }
            if(ans<k)//绳子少了，说明绳子要短一点
                right=mid-1;
            else if(ans>k)//绳子多了，说明绳子要长一点
                left=mid+1;
            else if(ans==k){
                //如果可以切成k段，那就记录当前mid值
                max_ans=max(max_ans,mid);
                left=mid+1;
            }

        }

        if(max_ans==0&&mid){
            printf("%.2lf",l[n-k]/100.0);
        }
        else if(max_ans!=0&&mid){
            printf("%.2lf",max_ans/100.0);
        }



}
