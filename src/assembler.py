# Notes:
# -> Add the location counter access handle "$"
# -> Add basic expression handeling
# -> Put restrictions on valid symbol and label entries
# -> Add decimal and binary base functionality
##############################################################################################################
import re
import sys
import table
import instructions

errors = ""

##############################################################################################################
# Experimental Code Classes

class Symbol:

    def __init__(self):
        self.labelDefs = {}
        self.eightBitDefs = {}
        self.sixteenBitDefs = {}

class Code:

    def __init__(self):
        self.data = []
        self.address = 0
        self.label = ""

    def write(self, data, line, instrct = "", mode = "number"):
        # Format: [line] [address] [label] [instruction + argument] [hex code] [comment]

        lineNum = line[0][0]
        addressStr = '0x{0:0{1}X}'.format(self.address,4)
        a = 0

        if(mode == "number"):
            a = '0x{0:0{1}X}'.format(data,2)
        elif(mode == "symbol"):
            a = data

        comment = ''
        pc = line[0][1]
        if(len(self.data) == 0 or pc != self.data[-1][0][0][1]):
            comment = line[2]

        self.data.append([line, addressStr, self.label, instrct, a, comment])
        self.address += 1
        self.label = ""

    def update(self, data, index):

        self.data[index][4] = "0x" + data


##############################################################################################################
# File reading functions

def read(name):
    # This function reads in lines from the asm file
    # It processes them and puts them into the form:
    # [[Line_number, Program_Counter] [body] [comment]]
    # Line_number corrisponds to the line on the 
    # source code. the Program_Counter is incremented
    # every time there is a non-empty line. Note that
    # two consecutive PC locations do NOT nessisarily
    # corrispond to two consecutive address locations

    # [[Line_number, Program_Counter] [body] 'comment']
    
    file = open(name, 'r')
    lines = []
    lineNumber = 0
    pc = 0
    
    for lineNumber, line in enumerate(file, start = 1):
        line = line.strip()
        line = line.upper()
        if(line):
            block = []
            rest = []
            comment = ''
            commentIndex = line.find(";")
            if(commentIndex != -1):
                comment = line[commentIndex:]
                rest = line[:commentIndex].strip()
            else:
                rest = line

            block.append([lineNumber, pc])
            if(rest):
                split_rest = re.split(r'([-+,\s]\s*)', rest)
                split_rest = [word for word in split_rest if not re.match(r'^\s*$',word)]
                split_rest = list(filter(None, split_rest))
                block.append(split_rest)
            else:
                block.append([])
            block.append(comment)
            lines.append(block)
            pc += 1
            
    file.close()
    return lines

##############################################################################################################
# Utility functions


##############################################################################################################
# Directive functions


##############################################################################################################
# Parsing functions
def parse_mnemonic(line, index, code, lines):
    # This function constructs an instruction and checks
    # to see if it is valid

    pc = line[0][1]
    
    mnemonic = line[1][index]
    instruction = mnemonic + " "
    argument = 0
    
    numOfMArgs = table.numOfMArgs(mnemonic)
    numOfArgs = table.numOfArgs(mnemonic)
    
    # Check the number of arguments to the instruction
    # Create an argument list from the line string
    args_with_comma = list(map(str.strip, line[1][index + 1:]))
    args = [x for x in args_with_comma if x != ","]
    if(len(args) != numOfArgs):
        error("Bad number of arguments to instruction!", line)
        return

    i, q, = 0, 0
    while(q < numOfMArgs):
        instruction += args_with_comma[i]
        if(args_with_comma[i] != ","):
            q += 1
        i += 1
    instruction = instruction.strip()

    # Construct the argStr which is a string of the arguments to the instruction
    argStr = ""
    if(i == 0):
        argStr += " "
    argStr += "".join(line[1][index+i+1:])
    
    # Check to see if the constructed instruction is valid
    if(instruction not in instructions.instructions):
        error("Bad instruction: " + str(instruction),line)
        return 

    # Write the instruction to memory
    instructArgStr = instruction+argStr
    code.write(instructions.instructions[instruction],line,instrct=instructArgStr)
    
    # Check to see if the argument to the instruction is valid
    argType = table.mnemonics[mnemonic][2]
    
    if(argType != "none"):
        argument = args[numOfArgs-1]

##        "data"
##        not data, not address, yes symbol--- good
##        not data, not address, not symbol--- bad
##        not data, yes address--------------- bad
##        yes data---------------------------- good
##
##        "address"
##        not address, not data, yes symbol--- good
##        not address, not data, not symbol--- bad
##        not address, yes data--------------- good
##        yes address------------------------- good
##
##
##        "data" and "address"
##        not data, not address, yes symbol--- good, good
##        not data, not address, not symbol--- bad,  bad
##        not data, yes address--------------- bad,  null
##        yes data, not address--------------- null, good
##        yes data---------------------------- good, ~~~~
##        yes address------------------------- ~~~~, good
        
        if(argType == "data"):
            if(not re.match(r'^(0[Xx])?[0-9A-Fa-f]{2}$',argument)):         # If it does not match the data format (not great)
                if(not re.match(r'^(0[Xx])?[0-9A-Fa-f]{2}$',argument)):     # If it does not match the address format (better)                  
                    if(re.match(r'^[A-Za-z_]+[A-Za-z0-9_]*$',argument)):    # If it matches the symbol format (great)
                        code.write("D_" + argument, line, mode = "symbol")
                    else:                                                   # If it does not match the symbol format
                        error("Bad argument: " + argument, line)              
                else:                                                       # If it matches the address format (bad)
                    error("Bad argument: " + argument, line)
            else:                                                           # If it matches the data format (great)
                code.write(int(argument, base = 16), line)

        elif(argType == "address"):
            if(not re.match(r'^(0[Xx])?[0-9A-Fa-f]{4}$',argument)):         # If it does not match the address format (not great)
                if(not re.match(r'^(0[Xx])?[0-9A-Fa-f]{2}$',argument)):     # If it does not match the data format (better)
                    if(re.match(r'^[A-Za-z_]+[A-Za-z0-9_]*$',argument)):    # If it matches the symbol format (great)
                        code.write("L_"+argument, line, mode = "symbol")
                        code.write("H_"+argument, line, mode = "symbol")
                    else:                                                   # If it does not match the symbol format (bad)
                        error("Bad argument: " + argument, line)
                else:                                                       # If it does match the data format, asssume the upper
                    code.write(int(argument, base = 16), line)              # part of the address is 00
                    code.write(00, line)
            else:                                                           # If it matches the address format (great)
                code.write(int(argument[2:], base = 16), line)
                code.write(int(argument[:2], base = 16), line)
    

##############################################################################################################
# Passes
               
def secondPass(symbols, code):
    # Format: [line] [address] [label] [instruction + argument] [hex code] [comment]
    for i, codeLine in enumerate(code.data):
        line = codeLine[0]
        data = codeLine[4][0]
        symbol = ""
        if(data == "D" or data == "L" or data == "H"):
            symbol = codeLine[4][2:]
            if(symbol not in symbols.labelDefs and symbol not in symbols.eightBitDefs and symbol not in symbols.sixteenBitDefs):
                error("Label \"" + symbol + "\" not defined!",line)
                return
        else:
            continue
            
        if(data == "D"):
            if(symbol in symbols.labelDefs):
                error("You cannot use an address label where an 8-bit value is expected!",line)
                return
                
            elif(symbol in symbols.eightBitDefs):
                code.update(symbols.eightBitDefs[symbol],i)
                   
            elif(symbol in symbols.sixteenBitDefs):
                error("You cannot use a 16-bit label constant where an 8-bit value is expected!",line)
                return
                
        elif(data == "L"):
            if(symbol in symbols.labelDefs):
                code.update(symbols.labelDefs[symbol][2:],i)

            elif(symbol in symbols.eightBitDefs):
                error("You cannot use a 8-bit label constant where a 16-bit value is expected!",line)
                return

            elif(symbol in symbols.sixteenBitDefs): 
                code.update(symbols.sixteenBitDefs[symbol][2:],i)

        elif(data == "H"):
            if(symbol in symbols.labelDefs):
                code.update(symbols.labelDefs[symbol][:2],i)

            elif(symbol in symbols.sixteenBitDefs):
                code.update(symbols.sixteenBitDefs[symbol][:2],i)

##############################################################################################################
# Output

def output(code, name):
    # Format: [line] [address] [label] [instruction + argument] [hex code]
    f = open(name,'w') if name else sys.stdout
    print('{:<20}{:<20}{:<20}{:<20}{:<20}'.format("Address","Label","Instruction","Hex Code","Comment"),file=f)
    print("----------------------------------------------------------------------------------------------------------------------------------",file=f)
    for l in code.data:
        print('{:<20}{:<20}{:<20}{:<20}{:<20}'.format(l[1],l[2],l[3],l[4],l[5]),file=f)

    print("\n" + errors,file=f)
    if f is not sys.stdout:
        f.close()
##############################################################################################################
# Experimental

def error(message, line):
    print("Error at line " + str(line[0][0]) + ": " + message)

#for lineNumber, line in enumerate(file, start = 1):
def lexer(lines):
    tokens = []
    code_lines = [x for x in lines if len(x[1])]
    for line in code_lines:
        pc, tl = line[0][1], []
        for word in line[1]:
            word = word.strip()
            if word in table.mnm_0:
                tl.append(["<mnm_0>", word])
            elif(re.match(r'^(0[Xx])?[0-9A-Fa-f]{2}$', word)):
                tl.append(["<08nm>", word, pc])
            elif word in table.mnm_0_e:
                tl.append(["<mnm_0_e>", word])
            elif word in table.mnm_1:
                tl.append(["<mnm_1>", word])
            elif word in table.mnm_1_e:
                tl.append(["<mnm_1_e>", word])
            elif word in table.mnm_2:
                tl.append(["<mnm_2>", word])
            elif word in table.reg:
                tl.append(["<reg>", word])
            elif word == ",":
                tl.append(["<comma>", word])
            elif word == "+":
                tl.append(["<plus>", word])
            elif word == "-":
                tl.append(["<minus>", word])
            elif word in table.drct_1:
                tl.append(["<drct_1>", word])
            elif word in table.drct_p:
                tl.append(["<drct_p>", word])
            elif word in table.drct_w:
                tl.append(["<drct_w>", word])
            elif re.match(r'^.+:$',word):
                tl.append(["<lbl_def>", word])
            elif(re.match(r'^(0[Xx])?[0-9A-Fa-f]{4}$', word)):
                tl.append(["<16nm>", word])
            elif(re.match(r'^[A-Za-z_]+[A-Za-z0-9_]*$', word)):
                tl.append(["<symbol>", word])
            elif word == "$":
                tl.append(["<lc>", word, pc])
            else:
                tl.append(["<idk_man>", word])
                error("Uknown token!", line)
        tokens.append(tl)

    return [code_lines, tokens]
######################################################################################
def evaluate(expr, symbols, code):
    sign, pop, result = 1, 2, 0
    while(expr):
        ###################################
        if(len(expr) >= 2):
            pop = 2
            if(expr[-2][0] == "<plus>"):
                sign = 1
            else:
                sign = -1
        else:
            pop = 1
            sign = 1
        ###################################
        if(expr[-1][0] in {"<08nm>", "<16nm>", "<numb>"}):
            result += sign*int(expr[-1][1], base=16)
            expr = expr[:-pop]
        elif(expr[-1][0] == "<lc>"):
            result += sign*code.address
            expr = expr[:-pop] 
        else:
            if(expr[-1][1] in symbols.eightBitDefs):
                result += sign*int(symbols.eightBitDefs[expr[-1][1]], base=16)
                expr = expr[:-pop]
            elif(expr[-1][1] in symbols.sixteenBitDefs):
                result += sign*int(symbols.sixteenBitDefs[expr[-1][1]], base=16)
                expr = expr[:-pop]
            else:
                expr += [["<plus>", "+"],["<numb>", hex(result)]]
                return expr
        ###################################
    return [result]
######################################################################################
def parse_lbl_def(tokens, symbols, code, line):
    er = ["<error>"]
    if not tokens:
        return 0
    if(tokens[0][0] == "<lbl_def>"):
        lbl = tokens[0][1]
        if lbl[:-1] in symbols.labelDefs:
            error("Label already in use!",line)
            return er
        elif lbl[:-1] in table.reserved:
            error("Label cannot be keyword!",line)
            return er
        elif lbl[:-1] in (symbols.eightBitDefs, symbols.sixteenBitDefs):
            error("Label conflicts with previous symbol definition",line)
            return er
        else:
            symbols.labelDefs[lbl[:-1]] = '{0:0{1}X}'.format(code.address,4)
            code.label = lbl
        return tokens.pop(0)
    else:
        return 0

######################################################################################
# Grammar:
#
# <line> ::= <lbl_def> [<drct>] [<code>]
#          | <drct> [<code>]
#          | <code>
#
# <code> ::= <mnm_0>
#          | <mnm_0_e> <expr>
#          | <mnm_1> <reg>
#          | <mnm_1_e> <reg> "," <expr>
#          | <mnm_2> <reg> "," <reg>
#
# <expr> ::= [ (<plus> | <minus>) ] <numb> { (<plus> | <minus> <numb> }
#
# <drct> ::= <drct_1> <expr>
#          | <drct_p> <expr> { ","  <expr> }
#          | <symbol> <drct_w> <expr>
#
# <numb> := <08nm> | <16nm> | <symbol> | <lc>
######################################################################################
def parse(lines, symbols, code):

    code_lines, tokenLines = lexer(lines)
    tree = []
    for tokens, line in zip(tokenLines, code_lines):
        tree.append(parse_line(tokens, symbols, code, line))

    print("tree:")
    for l in tree:
        print(l)

def org(arg, symbols, code, line):
    val = evaluate(arg, symbols, code)
    if(len(val) == 1):
        num = val[0]
        if(num < 0):
            error("Expression must be positive!",line)
            return
        else:
            code.address = num
            return
    else:
        error("Expression depends on unresolved symbol!",line)
        return

def db(args, symbols, code, line):
    for expr in args:
        val = evaluate(expr, symbols, code)
        if(len(val) == 1):
            num = val[0]
            if(num < 0):
                error("Expression must be positive!",line)
                return
            elif(num > 255):
                error("Expression too large! Must evaluate to an 8-bit number!", line)
                return
            else:
                pass #code.write()

def db_old(line, tags_with_comma, tags, args_with_comma, args, symbols, code):

    i = 0
    while(i < len(args_with_comma)):
        if(not i%2):
            if(tags_with_comma[i] == "[xx]"):
                code.write(int(args_with_comma[i],base = 16),line,instrct="DB")
            elif(tags_with_comma[i] == "symbol"):
                code.write("D_"+args_with_comma[i],line, instrct = "DB", mode="symbol")
            elif(tags_with_comma[i] == "comma"):
                error("Directive has bad comma!",line)
                return
            else:
                error("Directive has bad argument!",line)
                return
        else:
            if(tags_with_comma[i] != "comma"):
                error("Directive missing comma!",line)
                return
        i += 1

def equ(args, symbols, code, line):
    name = args[0][1]
    if(name in table.reserved):
        error("Cannot use reserved keyword in equ directive!",line)
        return
    elif(name in (symbols.eightBitDefs, symbols.sixteenBitDefs)):
        error("Symbol already defined!",line)
        return
    elif(name in symbols.labelDefs):
        error("Symbol conflicts with previous labelDef!",line)
        return

    val = evaluate(args[1], symbols, code)
    if(len(val) == 1):
        num = val[0]
        if num > 65535:
            error("Expression greater than 0xFFFF!",line)
            return
        elif num > 255:
            symbols.sixteenBitDefs[name] = '{0:0{1}X}'.format(num,4)
            return
        elif num >= 0:
            symbols.eightBitDefs[name] = '{0:0{1}X}'.format(num,2)
            return
        else:
            error("Expression must be positive!",line)
            return
    else:
        error("Expression depends on unresolved symbol!",line)
        return

def ds(arg, symbols, code, line):
    val = evaluate(arg, symbols, code)
    if(len(val) == 1):
        num = val[0]
        if(num < 0):
            error("Expression must be positive!",line)
            return
        else:
            code.address += num
            return
    else:
        error("Expression depends on unresolved symbol!",line)
        return

directives = {
    #Format:
    # [function, min_args, max_args, name]
    # -1 means no bound
    "ORG": [org, 1, 1, "ORG"],
    "DB":  [db, 1, -1, "DB"],
    "EQU": [equ, 2, 2, "EQU"],
    "DS":  [ds, 1, 1, "DS"],
}

def parse_expr(tokens, symbols, code, line):
    data = ["<expr>"]
    er = ["<error>"]
    if not tokens:
        print("Empty expr")
        return 0
    ##################################################
    if(tokens[0][0] in {"<plus>", "<minus>"}):
        data.append(tokens.pop(0))
    if(not tokens):
        error("Missing number/symbol!",line)
        return er
    if(tokens[0][0] not in {"<08nm>", "<16nm>", "<symbol>", "<lc>"}):
        if(tokens[0][0] not in {"<plus>", "<minus>"}):
            if(len(data) > 1):
                error("Expression had bad identifier!",line)
                return er
            else:
                # No expression found
                return 0
        error("Expression has extra operator!",line)
        return er

    data.append(tokens.pop(0))
    while(tokens):
        if(tokens[0][0] not in {"<plus>", "<minus>"}):
            if(tokens[0][0] not in {"<08nm>", "<16nm>", "<symbol>", "<lc>"}):
                # reached end of expression
                return data
            error("Expression missing operator!",line)
            return er
        data.append(tokens.pop(0))
        if(not tokens):
            error("Expression missing number/symbol!",line)
            return er
        if(tokens[0][0] not in {"<08nm>", "<16nm>", "<symbol>", "<lc>"}):
            if(tokens[0][0] not in {"<plus>", "<minus>"}):
                error("Expression has bad identifier!",line)
                return er
            error("Expression has extra operator!",line)
            return er
        data.append(tokens.pop(0))
    return data
######################################################################################
def parse_drct(tokens, symbols, code, line):
    data = ["<drct>"]
    er = ["<error>"]
    if not tokens:
        return 0
    ##################################################
    # [drct_1]
    if(tokens[0][0] == "<drct_1>"):
        data.append(tokens.pop(0))
        if(not tokens):
            error("Directive missing argument!",line)
            return er
        expr = parse_expr(tokens, symbols, code, line)
        if(expr == er):
            return er
        data.append(expr)

        arg = data[2][1:]
        directives[data[1][1]][0](arg,symbols,code,line)
        return data
    ##################################################
    # [drct_p]
    elif(tokens[0][0] in {"<drct_p>", "<08nm>"}):
        if(tokens[0][0] == "<08nm>"):
            if(tokens[0][1] != "DB"):
                return 0
            tokens[0][0] = "<drct_p>"
        data.append(tokens.pop(0))
        if(not tokens):
            error("Directive missing argument!",line)
            return er

        expr = parse_expr(tokens, symbols, code, line)
        if(expr == er):
            return er
        data.append(expr)

        while(tokens):
            if(tokens[0][0] != "<comma>"):
                error("Missing comma!",line)
                return er
            data.append(tokens.pop(0))
            if(not tokens):
                error("Directive missing last argument or has extra comma!",line)
                return er
            expr = parse_expr(tokens, symbols, code, line)
            if(expr == er):
                return er
            if(not expr):
                error("Directive has bad argument!",line)
                return er
            data.append(expr)
        args = [x[1:] for x in data[2:] if x[0] != "<comma>"]
        directives[data[1][1]][0](args,symbols,code,line)
        return data
    ##################################################
    # [drct_w]
    elif(tokens[0][0] == "<symbol>"):
        data.append(tokens.pop(0))
        if(not tokens or tokens[0][0] != "<drct_w>"):
            error("Bad Identifier!",line)
            return er
        data.append(tokens.pop(0))
        if(not tokens):
            error("Directive missing argument!",line)
            return er
        expr = parse_expr(tokens, symbols, code, line)
        if(expr == er):
            return er
        data.append(expr)
        ##############################################
        arg1 = data[1]
        arg2 = data[3][1:]
        directives[data[2][1]][0]([arg1,arg2],symbols,code,line)
        return data
    elif(tokens[0][0] == "<drct_w>"):
        error("Directive missing initial argument!",line)
        return er

    return 0
######################################################
def parse_code(tokens, symbols, code, line):
    data = ["<code>"]
    er = ["<error>"]
    if not tokens:
        return 0
    ##################################################
    # [mnm_0]
    if(tokens[0][0] == "<mnm_0>"):
        data.append(tokens.pop(0))
        return data
    ##################################################
    # [mnm_0_e]
    elif(tokens[0][0] in {"<mnm_0_e>", "<08nm>"}):
        if(tokens[0][0] == "<08nm>"):
            if(tokens[0][1] != "CC"):
                return 0
            tokens[0][0] = "<mnm_0_e>"
        data.append(tokens.pop(0))
        if(not tokens):
            error("Instruction missing argument!",line)
            return er
        expr = parse_expr(tokens, symbols, code, line)
        if(expr == er):
            return er
        data.append(expr)
        return data
    ##################################################
    # [mnm_1]
    elif(tokens[0][0] == "<mnm_1>"):
        data.append(tokens.pop(0))
        if(not tokens):
            error("Instruction missing register/register-pair",line)
            return er
        if(tokens[0][0] != "<reg>"):
            error("Instruction has bad register/register-pair",line)
            return er
        data.append(tokens.pop(0))
        return data
    ##################################################
    # [mnm_1_e]
    elif(tokens[0][0] == "<mnm_1_e>"):
        data.append(tokens.pop(0))
        if(not tokens):
            error("Instruction missing register/register-pair!",line)
            return er
        if(tokens[0][0] != "<reg>"):
            error("Instruction has bad register/register-pair!",line)
            return er
        data.append(tokens.pop(0))
        if(not tokens):
            error("Instruction missing comma and argument!",line)
            return er
        if(tokens[0][0] != "<comma>"):
            if(tokens[0][0] not in {"<08nm>", "<16nm>", "<symbol>"}):
                error("Instruction has bad argument!",line)
                return er
            error("Instruction missing comma!",line)
            return er
        data.append(tokens.pop(0))
        if(not tokens):
            error("Instruction missing argument!",line)
            return er
        expr = parse_expr(tokens, symbols, code, line)
        if(expr == er):
            return er
        data.append(expr)
        return data
    ##################################################
    # [mnm_2]
    elif(tokens[0][0] == "<mnm_2>"):
        data.append(tokens.pop(0))
        if(not tokens):
            error("Instruction missing register/register-pair!",line)
            return er
        if(tokens[0][0] != "<reg>"):
            error("Instruction has bad register/register-pair!",line)
            return er
        data.append(tokens.pop(0))
        if(not tokens):
            error("Instruction missing comma and register/register-pair!",line)
            return er
        if(tokens[0][0] != "<comma>"):
            if(tokens[0][0] != "<reg>"):
                error("Instruction has bad register/register-pair!",line)
                return er
            error("Instruction missing comma!",line)
            return er
        data.append(tokens.pop(0))
        if(not tokens):
            error("Instruction missing register/register-pair!",line)
            return er
        if(tokens[0][0] != "<reg>"):
            error("Instruction has bad register/register-pair!",line)
            return er
        data.append(tokens.pop(0))
        return data

    return 0
######################################################################################
def parse_line(tokens, symbols, code, line):
    data = ["<line>"]
    er = ["<error>"]
    if(len(tokens) == 0):
        return 0
    ################################
    # [lbl_def]
    lbl_def = parse_lbl_def(tokens, symbols, code, line)
    if(lbl_def):
        if(lbl_def == er):
            return er
        data.append(lbl_def)
    ################################
    # [drct]
    drct = parse_drct(tokens, symbols, code, line)
    if(drct):
        if(drct == er):
            return er
        data.append(drct)
    ################################
    # [code]
    code = parse_code(tokens, symbols, code, line)
    if(code):
        if(code == er):
            return er
        data.append(code)
    ###############################
    # check to see that we have at
    # least one of lbl_def, drct,
    # or code
    if(len(data) < 2):
        tokens.pop(0)
        error("Bad Initial Identifier!",line)
        return er
    ###############################
    # check to see if we have any
    # tokens left
    if(len(tokens)):   
        error("Bad Identifier!",line)
        return er
    ###############################
    # everything's good
    return data

######################################################################################
# Main program

code = Code()
symbols = Symbol()

callArgs = sys.argv
inFile =""
outFile = ""

if(len(sys.argv) == 3):
    inFile = sys.argv[1]
    outFile = sys.argv[2]
else:
    inFile = "pgm.asm"

parse(read(inFile),symbols,code)