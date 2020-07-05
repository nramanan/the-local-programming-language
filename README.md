The local compiler

To run,

  python local.py PROGNAME

where PROGNAME is the name of the program you wish to compile

If you want the output saved to a file that you can then execute with Python,
run

  python local.py PROGNAME > TARGNAME

where TARGNAME is the name of the target Python file

For example,

  python local.py hello.local > hello.py

You can then run hello.py with Python.

  python hello.py

local.py also supports the following options:

-d : Enables debugging of the parsing and AST walk (lex debugging must be
     enabled in the code manually)

-p : Forces the compiler to quit immediately after parsing without walking
     the AST. This is useful for testing production rules with no associated
     actions.


------------------------------
####### Testing Notes #######
------------------------------
To run the suite of tests, go to the testing folder and type the following to 
link your folder to the base files:
$ ln -s /home/plt/the-local-programming-language/trunk/haversine.py .
$ ln -s /home/plt/the-local-programming-language/trunk/conversion.py .

Substitute the path to your copy of the repository for "/home/plt/the-local..." 
if it is different from the above listed path.

Use the Makefile:
$ make

To run the local file, use the following commands from the trunk folder:
$ python local.py testing/coffee.local
$ python testing/coffee.py

The demo is designed to be run as if one were starting from Mudd Building 
on Columbia's Morningside Campus, coordinates are (40.809343, -73.959811)
Give yourself a reasonable amount of time, such as 30-45 minutes until your
next event.  Those coffee lines are long!


------------------------------
### Developer Instructions ###
------------------------------
To compile a working copy of our code for testing, do the following steps:
1. Create your new file, e.g. assign_statement.py
2. Create a local program to test your statement, e.g.
   sandbox/checkassign.local
3. Test the program compilation with the following (adjust for your statement):
    python local.py sandbox/checkassign.local
4. Redirect the program output with the following (adjust for your statement):
    python local.py sandbox/checkassign.local > sandbox/checkassign.py
5. Run the test output:
    python sandbox/checkassign.py

** 'testing' folder is for automated testing as per our test plan.
   'sandbox' folder is for stim testing by individual team members.