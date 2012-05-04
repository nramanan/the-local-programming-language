# Filename:                localast.py
# Author:                  Team 13
# Description:             local language AST utilities
# Supported Lanauge(s):    Python 2.x
# Time-stamp:              <2012-05-04 15:38:22 plt>

# Number of spaces a tab equals
INDENT = 4
COUNT = 0

# Indent your children if you are one of these statements
indent_them = ('if', 'elif', 'elif_else', 'else', 'for', 'while', 'def',
               'except')

class Node:
    '''Node class for the AST'''
    def __init__(self,
                 type,          # type of node
                 children=None, # children of the node
                 value=None,    # stored value of the node (a string)
                 line=None):    # Python line to by constructed from subtree
        self.type = type
        if children:
            self.children = children
        else:
            self.children = [ ]
        self.value = value
        self.line = line

# Utility walker function
def _do_arglist_subtree(node, code, debug):
    '''For building a list of arguments'''
    # A list of arguments
    if len(node.children) == 2:
        # Recursively follow the list
        arglist = _do_arglist_subtree(node.children[0], code, debug)
        # Evaluate the atom and append it
        arg = walk_the_tree(node.children[1], code, debug)
        arglist += ", " + arg
        return arglist
    elif len(node.children) == 1:
        arg = walk_the_tree(node.children[0], code, debug)
        return arg

# Main statement block builder
def _do_stmt_list_subtree(node, code, debug):
    if len(node.children) == 2:
        stmt_list = _do_stmt_list_subtree(node.children[0], code, debug)
        stmt = walk_the_tree(node.children[1], code, debug)
        return stmt_list + "\n" + stmt
    elif len(node.children) == 1:
        stmt = walk_the_tree(node.children[0], code, debug)
        return stmt

# Print subtree
def _do_print_subtree(node, code, debug):
    '''For building a format print statement'''
    # Simple print
    if len(node.children) == 1:
        print_str = walk_the_tree(node.children[0], code, debug)
        return "print %s\n" % (print_str)
    # Format print
    elif len(node.children) == 2:
        print_str = walk_the_tree(node.children[0], code, debug)
        print_arglist = _do_arglist_subtree(node.children[1], code, debug)
        return "print %s %% (%s)\n" % (print_str, print_arglist)

# Indented blocks
def _do_if_subtree(node, code, debug):
    '''For indenting IF code blocks'''
    # Walk tree to build expression
    expr = walk_the_tree(node.children[0], code, debug)
    # Walk tree to build statement and split statement on newlines
    if_stmt = walk_the_tree(node.children[1], code, debug).split("\n")
    if_stmt_i = ""
    # Add indents to all the lines in the statement
    for line in if_stmt:
        if_stmt_i += " "*INDENT + line + "\n"
    # Construct the if statment
    return "if %s:\n%s" % (expr, if_stmt_i)

def _do_elif_block(node, code, debug):
    '''For building an arbitrary number of ELIF blocks'''
    # A block of blocks
    if len(node.children) == 3:
        block = _do_elif_block(node.children[0], code, debug)
        expr = walk_the_tree(node.children[1], code, debug)
        stmt = walk_the_tree(node.children[2], code, debug).split("\n")
        stmt_i = ""
        for line in stmt:
            stmt_i += " "*INDENT + line + "\n"
        return "%s\nelif %s:\n%s" % (block, expr, stmt_i)
    # A block
    elif len(node.children) == 2:
        expr = walk_the_tree(node.children[0], code, debug)
        stmt = walk_the_tree(node.children[1], code, debug).split("\n")
        stmt_i = ""
        for line in stmt:
            stmt_i += " "*INDENT + line + "\n"
        return "elif %s:\n%s" % (expr, stmt_i)

def _do_elif_subtree(node, code, debug):
    '''For indenting IF-ELIF code blocks'''
    expr = walk_the_tree(node.children[0], code, debug)
    if_stmt = walk_the_tree(node.children[1], code, debug).split("\n")
    elif_block = _do_elif_block(node.children[2], code, debug)
    if_stmt_i = ""
    for line in if_stmt:
        if_stmt_i += " "*INDENT + line + "\n"
    return "if %s:\n%s\n%s" % (expr, if_stmt_i, elif_block)

def _do_elif_else_subtree(node, code, debug):
    '''For indenting IF-ELIF-ELSE code blocks'''
    expr = walk_the_tree(node.children[0], code, debug)
    if_stmt = walk_the_tree(node.children[1], code, debug).split("\n")
    elif_block = _do_elif_block(node.children[2], code, debug)
    else_stmt = walk_the_tree(node.children[3], code, debug).split("\n")
    if_stmt_i = ""
    else_stmt_i = ""
    for line in if_stmt:
        if_stmt_i += " "*INDENT + line + "\n"
    for line in else_stmt:
        else_stmt_i += " "*INDENT + line + "\n"
    return "if %s:\n%s\n%s\nelse:\n%s" % (expr, if_stmt_i, elif_block,
                                          else_stmt_i)

def _do_else_subtree(node, code, debug):
    '''For indenting IF-ELSE code blocks'''
    expr = walk_the_tree(node.children[0], code, debug)
    if_stmt = walk_the_tree(node.children[1], code, debug).split("\n")
    else_stmt = walk_the_tree(node.children[2], code, debug).split("\n")
    if_stmt_i = ""
    else_stmt_i = ""
    for line in if_stmt:
        if_stmt_i += " "*INDENT + line + "\n"
    for line in else_stmt:
        else_stmt_i += " "*INDENT + line + "\n"
    return "if %s:\n%s\nelse:\n%s" % (expr, if_stmt_i, else_stmt_i)

def _do_def_subtree(node, code, debug):
    '''For indenting DEF code blocks'''
    if len(node.children) == 2:
        def_arg = _do_arglist_subtree(node.children[0], code, debug)
        def_stmt = walk_the_tree(node.children[1], code, debug).split("\n")
    elif len(node.children) == 1:
        def_stmt = walk_the_tree(node.children[0], code, debug).split("\n")
    def_stmt_i = ""
    for line in def_stmt:
        def_stmt_i += " "*INDENT + line + "\n"
    if len(node.children) == 2:
        return "def %s(%s):\n%s\n" % (node.value, def_arg, def_stmt_i)
    elif len(node.children) == 1:
        return "def %s():\n%s\n" % (node.value, def_stmt_i)

def _for_subtree(node, code, debug):
    '''For indenting For block'''
    for_atomchild = walk_the_tree(node.children[0], code, debug)
    for_stmtchild = walk_the_tree(node.children[1], code, debug).split("\n")
    for_stmt_indented = ""
    for line in for_stmtchild:
        for_stmt_indented += " "*INDENT + line + "\n"
    return "for %s in %s:\n%s" % (node.value, for_atomchild, for_stmt_indented)

def _while_subtree(node, code, debug):
    '''For indenting While loop block'''
    while_exprchild = walk_the_tree(node.children[0], code, debug)
    while_stmtchild = walk_the_tree(node.children[1], code, debug).split("\n")
    while_stmt_indented = ""
    for line in while_stmtchild:
        while_stmt_indented += " "*INDENT + line + "\n"
    return "while %s:\n%s" % (while_exprchild, while_stmt_indented)

def _except_subtree(node, code, debug):
    except_try_child = walk_the_tree(node.children[0], code, debug).split("\n")
    print node.children[1]
    except_catch_child = walk_the_tree(node.children[1], code, debug).split("\n")
    except_trychild_indented = ""
    except_catchchild_indented = ""

    for line in except_try_child:
        except_trychild_indented += " "*INDENT + line + "\n"
    for line in except_catch_child:
        except_catchchild_indented += " "*INDENT + line + "\n"
    print except_catch_child
    return "try:\n%s\nexcept %s:\n%s" % (except_trychild_indented, node.value, except_catchchild_indented)

def _do_indent_subtree(node, code, debug):
    '''For indenting statements within blocks'''
    # IF
    if node.type == 'if':
        return _do_if_subtree(node, code, debug)
    # IF-ELIF
    if node.type == 'elif':
        return _do_elif_subtree(node, code, debug)
    # IF-ELIF-ELSE
    if node.type == 'elif_else':
        return _do_elif_else_subtree(node, code, debug)
    # ELSE
    if node.type == 'else':
        return _do_else_subtree(node, code, debug)
    # DEF
    if node.type == 'def':
        return _do_def_subtree(node, code, debug)
    # FOR
    if node.type == 'for':
        return _for_subtree(node, code, debug)
    # WHILE
    if node.type == 'while':
        return _while_subtree(node, code, debug)
    # EXCEPT
    if node.type == 'except':
        return _except_subtree(node, code, debug)

# Main tree-walking function
def walk_the_tree(node, code="", debug=False):
    '''Walk the AST and return a string, which is a Python program'''
    # Default case (should not be hit)
    if node is None:
        return
    # Debugging to watch tree traversal
    if debug:
        print "#type: %s, value: %s" % (node.type, node.value)
    # For nodes with children
    if node.children:
        if node.type == "stmt_list":
            code += _do_stmt_list_subtree(node, code, debug)
        # Certain statements require substatements to be indented
        elif node.type in indent_them:
            code += _do_indent_subtree(node, code, debug)
        # Assignments needs their right side synthesized
        elif node.type == "assign":
            #code += _indent_subtree(node, code, debug)
            rhs = walk_the_tree(node.children[2], code, debug)
            lhs = walk_the_tree(node.children[0], code, debug)
            ms = walk_the_tree(node.children[1], code, debug)
            assmnt = lhs + ms + rhs + "\n"
            code += assmnt
        elif node.type == "print":
            code += _do_print_subtree(node, code, debug)
        # If we need to synthesize a string, build a tuple from the subtree
        elif node.line:
            values = ( )
            # Visit the children
            for child in node.children:
                values += (walk_the_tree(child, code, debug),)
            #print "LINE: ", node.line
            #print "VALUES: ", str(values)
            line = (node.line % values)
            # We're building a line here, not appending to target code
            code = line
        # Otherwise, just walk the tree
        else:
            for child in node.children:
                code = walk_the_tree(child, code, debug)
    # Otherwise, the node is a leaf node (must have a value)
    else:
        code = node.value
    # Return statement for the function. Builds target code in order
    return code
