#! Unfinished (Suposed to differentiate a function given as a string)
operators = ["*", "+", "-", "/", "^"]
# other functionsto be added:   sin()
#                               cos()
#                               tan()
import sys
def getFormula():
    args = sys.argv
    try:
        formula = args[1]
    except:
        primt("Error: No arguments")
        quit()
    print(formula)
    return formula

def main():
    raw_formula = getFormula()
    symbolList = extractParameters(raw_formula)
    f = makeFunction(raw_formula, symbolList)

    differentiate(raw_formula, "x")


def extractParameters(raw_formula):
    ignored_operators = operators+ ["(", ")"] 
    allElements = splitOnSymbols( raw_formula, ignored_operators)
    isNumList = [isNum(i) for i in allElements]
    symbolList = [i for i in allElements if not isNum(i) and i!= ""]
    unique = set(symbolList)
    symbolList = sorted(list(unique))
    return symbolList


def splitOnSymbols( string, symbols):
    workingList = [string]
    for i in symbols:
        splitList = []
        for j in workingList:
            splitList+= j.split(i)
        workingList = splitList
    return workingList

def makeFunction(rawString, parameterNames):
    funString = "lambda "+ ",".join(parameterNames) +" : " + rawString +"\n"
    f = eval(funString)

    return f

def isNum(string):
    try:
        float(string)
        return True
    except:
        return False




def differentiate(formula, symbol):
    parInd = getParenthesis(formula)
    firstExprssion = formula[1: parInd]

    if parInd== -1:
        return rawDifferentiate(formula)
    else: 
        merge( formula[:parInd], formula[parInd+1], formula[parInd+2:])


def rawDifferentiate(formula, symbol):
    isSymbol = True
    for i in operator:
        if i in formula:
            isSymbol = True
    
    if isSymbol == True:
        if formula == symbol:
            return 1
        else: 
            return None
    else:
        A, op, B = opSplit(formula)
        return merge(A, op, B, symbol)

def opSplit(formula):
    f = lambda x:formula.find(x)
    firstSplit = min(operators, key = f)
    A =formula[:firstSplit]
    op =formula[firstSplit]
    B = formula[firstSplit+1:]
    A, op, B




def merge(A, op, B, symbol):
    dA = differentiate(A, symbol)
    dB = differentiate(B, symbol)
    result = ""
    if op == "+" or op =="-": 
        result = comb(dA, op, B)
    elif operator =="/":
        first = comb(dA, "/", B) 
        last = comb(comb(A, "*", dB), "/",  comb(B, "*", B))
        result = comb(first, "-", last)
    elif op == "*":
        first = comb(dA, "*", B)
        last = comb(A, "*", dB)
        result= comb(first, "+", last)
    elif op =="^": 
        first = comb(comb(dA, "*", A), "^", B)#TODO FIX THIS
    return result


    
def comb(A, op, B):
    if A != None:
        A = "("+A+")"
    if B != None:
        B = "("+B+")"
    #mul
    if op == "*":
        if A == None or B == None:
            return None
        return A+"*"+B
    #div
    elif op =="/":
        if A == None:
            return None
        return A+"/"+B
    #Add and sub
    elif op == "+" or op =="-":
        if A != None and B != None:
            return A+op+B
        elif B == None:
            return A
        else:
            if op == "-":
                return "-"+ B
            else:
                return B
    #pow
    elif op =="^":
        if A == None: 
            return None
        elif B == None:
            return 1
        elif B == 1:
            return A
        return "("+A +"^"+B+")"

def getParenthesisIndex(formula):
    counter =0
    if formula[0] != "(":
        return -1
    for ind, el in enumerate(formula):
        if el =="(":
            counter +=1
        if el ==")":
            counter -=1
        if counter ==0:
            print(ind)
            return ind
    



if __name__ == '__main__':
    main()
