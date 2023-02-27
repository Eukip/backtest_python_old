//
// Created by tema on 24.6.22.
//
#include <iostream>
#include <map>
#include <vector>
using namespace std;
#include <bits/stdc++.h>
#include <string>
#include <chrono>
// #include <pybind11/pybind11.h>

// namespace py = pybind11;


int infixToPostfix(const string& infix)
{
    using chrono::high_resolution_clock;
    using chrono::duration_cast;
    using chrono::duration;
    using chrono::milliseconds;
    auto t1 = high_resolution_clock::now();

    string result;
    stack<char> st;
    stack<int> st_calc;

    map<char, int> precedence = {
            {'(', 1},
            {'&', 2},
            {'|', 3}
    };
    for (char c : infix) {
        if (isdigit(c))
            result += c;
        else {
            if (c == ' ')
            result = result;
            else if ( c == '(')
                st.push(c);
            else if ( c == ')'){
                while (st.top() != '('){
                    result += st.top();
                    st.pop();
                }
                st.pop();
            }

            else {
                while (!st.empty() &&
                precedence[st.top()] >= precedence[c]) {
                    result += st.top();
                    st.pop();
                }
                st.push(c);

            }
        }
        }
    while (!st.empty()) {
        result += st.top();
        st.pop();
        }
    int a;
    int b;
    int res = 0;
    for (char i : result){
        if (isdigit(i))
            st_calc.push((int)i);
        else if (st_calc.size() > 2){
            a = st_calc.top();
            b = st_calc.top();
            st_calc.pop();
            st_calc.pop();
            if (i == '&'){
                res = a & b;
                st_calc.push(res);
            }
            else if (i == '|'){
                res = a || b;
                st_calc.push(res);
            }
        }


    }
    res = st_calc.top();
    auto t2 = high_resolution_clock::now();
    auto ms_int = duration_cast<milliseconds>(t2 - t1);
    duration<double, milli> ms_double = t2 - t1;
    cout << ms_int.count() << "ms\n";
    cout << ms_double.count() << "ms\n";
    cout << (bool)res << endl;
    return res;


}

int main()
{
    const string exp = "(1 | 1) & (1 | 1) | (1 | 1) & 1";
    return infixToPostfix(exp);
    // return 0;
}


// PYBIND11_MODULE(module_name, handle){
//     handle.doc() = "Module docs";
//     handle.def("infixToPostfix", &infixToPostfix);
//     handle.def("main_test", &main);
// }