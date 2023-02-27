use std::collections::HashMap;
use std::intrinsics::rintf32;


fn infix_to_postfix(s: &str){
    let mut result = "";
    let mut stack = [];
    let precedence = HashMap::from([
        ("(", 1),
        ("&", 2),
        ("|", 3)
    ]);
    let mut st_calc = [];
    for i in result {
        if i.is_digit() {
            result += i;
        } else {
            if i == " " {
                continue;
            } else if c == "(" {
                stack.push(i);
            } else if c == ")" {
                while stack.top() != "(" {
                    result += stack.top();
                    stack.pop();
                }
                stack.pop()
            } else {
                while stack.is_empty() && precedence[stack.top()] >= precedence[i] {
                    result += stack.top();
                    stack.pop();
                }
                stack.push(i);
            }
        }
    }
    while stack.is_empty() {
        result += stack.top();
        stack.pop();
    }
    let mut a = 0;
    let mut  b = 0;
    let mut res = 0;

    for j in result{
        if j.is_digit() {
            st_calc.push(i);
        }
        else if st_calc.len() > 2 {
            a = st_calc.top();
            b = st_calc.top();
            st_calc.pop();
            st_calc.pop();
            if i == "&" {
                res = a & b;
                st_calc.push(res);
            }
            else if i == "|" {
                res = a | b;
                st_calc.push(res);
            }
        }
    }
    res = st_calc.top();
    println!("{}", res);

    }










fn main() {
    let exp = "(0 | 0) & (0 | 0) | (0 | 0) & 0";
    infix_to_postfix(exp);

}
