##### Input .local files for testing

### LEXING/PARSING TESTS:
# cond_stmt.py local test inputs:
if_test = '''if a
    print("a is true");'''

ifelse_test = '''if a
    print("a is true");
else
    print("a is false");'''

nesting_test = '''if a {
    print("a is true");
    if b
        print("made it here");
    else
        print("made it there");
}
else
    print("a is false");'''

# math_expr.py local test inputs:
math_test1 = '''a = isd + dsa * 12 + (7/5);'''

# assign_stmt.py local test inputs:
assign_test = '''a = 10;
b = 0;'''

# exit
exit_test = '''exit(1);'''


### BLACK BOX TESTS:
# Hello World:
helloworld_test = '''print("Hello, world!");'''

# example1.py local test inputs:
example1_test = '''x = 1;
y = 2;
z = 1.1;
w1 = x + y;
w2 = x - y;
w3 = x + z;'''
