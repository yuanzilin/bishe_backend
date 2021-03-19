#include<ctime>
#include<cstdio>
#include<cstdlib>
#include <cmath>
#include<bits/stdc++.h>

using namespace std;

#define MAXN 100

char a[3]="YN";
int main(){
    srand((unsigned)time(NULL));
    int n,m;
    n=rand()%50+1;
    m=rand()%50+1;
    printf("%d %d\n",n,m);
    for(int i=0;i<n;i++){
    	int flag=0;
    	for(int j=0;j<m;j++){
    		if(flag==5){
    			printf("0 ");
    			flag=0;
			}
			else{
				int x=rand()%1000;
    			printf("%d ",x);
    			flag++;
			}
    		
		}
		printf("\n");	
	} 
}
