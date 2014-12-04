#include <string>
#include <iostream>
#include <vector>

using namespace std;
typedef string::size_type s_t;
typedef string::value_type v_t;
typedef vector<s_t>::size_type i_t;
string str;
vector<s_t> idx;
i_t minsup;

void printPattern(i_t offset,i_t count,v_t depth)
{
    cout << count << "\t"
         << str.substr(idx[offset], depth)
         << endl;
}

v_t getValue(i_t i, s_t depth)
{
    return str[idx[i] + depth];
}

void vectorSwap(i_t i, i_t j, i_t len)
{
    while(len-- > 0) {
        swap(idx[i], idx[j]);
        i++;
        j++;
    }
}

i_t selectPivot(i_t begin, i_t end)
{
    return begin + rand() % (end - begin);
}

void mine(i_t begin, i_t end, s_t depth, bool equal=false) {
    i_t count = end - begin; 
    if(count < minsup) {
	return;
    } else if (equal) {
	printPattern(begin, count, depth); 
    }
    i_t pivot = selectPivot(begin, end); 
    swap(idx[begin], idx[pivot]);
    v_t t = getValue(begin, depth);
    i_t a = begin+1, c = end-1;
    i_t b = a , d = c; v_t r;
    while(true) {
	while(b <= c && ((r=getValue(b, depth)-t) <= 0)) { 
	    if (r == 0) { 
		swap(idx[a], idx[b]); a++; 
            } 
 	    b++;
        }
        while(b <= c && ((r=getValue(c, depth)-t) >= 0)) {
	    if (r == 0) { swap(idx[c], idx[d]); d--; }
	c--; }
        if(b > c) { 
	    break;
        }
	swap(idx[b], idx[c]); b++;
	c--;
    }
    i_t range = min(a - begin, b - a); 
    vectorSwap(begin, b - range, range); 
    range = min(d - c, end - d - 1); 
    vectorSwap(b, end - range, range);
    range = b - a;
    mine(begin, begin + range, depth);
    if(t != '\0') {
        mine(begin+range, range+a+end-d-1, depth+1, true);
    }
    range = d - c;
    mine(end - range, end, depth);
}

int main(){
    cin>>str;
    //cout<<"hello"<<endl;
    for(s_t i = 0; i < str.size(); i++) {
       idx.push_back(i);
    }
    cout<<str<<endl;
    minsup = 2;
    mine(0, str.size(), 0);
}
