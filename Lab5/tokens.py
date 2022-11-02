keywords = ["decl", "enddecl", "start", "end", "exit", "int", "string", "arr", "if", "else", "elseif", "read", "write", "while", "not", "and", "or"]
operators = ["+", "-", "*", "/", "%", "=", ">", "<", "<=", ">="]
separators = [";", " ", "{", "}", "(", ")", "\n", "[", "]", "\""]

identifier = r'^[a-zA-Z]([a-zA-Z]|[0-9])*$'
constant = r'^(0|[+-]?[1-9][0-9]*)$|^\".\"$|^\".*\"$'
