#include<ctime>
#include<cstdio>
#include<cstdlib>
#include <cmath>

#define MAXN 100

char a[3]="YN";
int main(){
    srand((unsigned)time(NULL));
    int n,m;
    n=rand()%5;
    m=rand()%3+2*n;
    printf("%d %d\n",n,m);
}
