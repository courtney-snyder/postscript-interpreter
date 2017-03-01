# Courtney Snyder
# CptS 355, Homework 2 part B
# Last Updated: 2/27/2017
# Written on Windows 10
# Description: Part 2 of the Postscript interpreter written in Python.

import re

opStack = []

def opPop():
    if (len(opStack) > 0):
        return opStack.pop(-1) #Remove the element from the end of the list and return a copy of its value
    else:
        print("Error; empty operand stack")

def opPush(value):
    if isinstance(value, str): # A string can be a variable or just a string
        if len(dictStack) > 0 and value in dictStack[-1]: # If pushing a variable or function to the stack, push it's dictionary value if it is in the dictionary
            pushMe = lookup(value) # Determine if the dictionary value of value is a code array or a variable
            if pushMe == None: # lookup entered lookupHelper to interpret a code array and didn't return anything
                pass
            else: # If value was not a code array, pushMe is a variable, push pushMe to opStack
                opStack.append(pushMe)
        else: # If the value is just a string or undefined variable
            opStack.append(value)
    else: # The value is a number or an integer array
        opStack.append(value) #Add the given value to the end of the list

dictStack = []

def dictPop():
    if len(dictStack) > 0:
        return dictStack.pop(-1)
    else:
        print("Error; empty dictionary stack")

def dictPush(name,value):
    if len(dictStack) > 0: # If there is already a dictionary on the dictStack, add to it
        dictStack[-1][name] = value # Get the dictionary on top (element -1) and add to the name and value to it
    else: # If dictStack is empty, push a new dictionary onto it with the name and value in the current dictionary
        dictStack.append({name:value})

def define(name, value):
    dictPush(name, value)

def lookup(name):
    if name in dictStack[-1]: # If the element is in the current dictionary, return it
        if isinstance(dictStack[-1][name], list):
            lookupHelper(dictStack[-1][name])
        else:
            return dictStack[-1][name]
    else:
        print("Error; variable not defined in current dictionary")

def lookupHelper(inputArray): # Runs the input array through the interpretter to determine if it is a code array or integer array
    interpret(inputArray)

def add ():
    if len(opStack) > 1: # If there are at least 2 operands in the stack
        operand2 = opStack.pop()
        operand1 = opStack.pop()
        if isinstance(operand1, str):
            operand1 = lookup(operand1)
        if isinstance(operand2, str):
            operand2 = lookup(operand2)
        result = operand1 + operand2
        opPush(result)
    else:
        print("Error; not enough operands on operator stack for add")

def sub ():
    if len(opStack) > 1: # If there are at least 2 operands in the stack
        operand2 = opStack.pop()
        operand1 = opStack.pop()
        if isinstance(operand1, str):
            operand1 = lookup(operand1)
        if isinstance(operand2, str):
            operand2 = lookup(operand2)
        result = operand1 - operand2
        opPush(result)
    else:
        print("Error; not enough operands on operator stack for sub")

def mul ():
    if len(opStack) > 1: # If there are at least 2 operands in the stack)
        operand2 = opStack.pop()
        operand1 = opStack.pop()
        if isinstance(operand1, str):
            operand1 = lookup(operand1)
        if isinstance(operand2, str):
            operand2 = lookup(operand2)
        result = operand1 * operand2
        opPush(result)
    else:
        print("Error; not enough operands on operator stack for mul")

def div ():
    if len(opStack) > 1: # If there are at least 2 operands in the stack
        operand2 = opStack.pop()
        operand1 = opStack.pop()
        if isinstance(operand1, str):
            operand1 = lookup(operand1)
        if isinstance(operand2, str):
            operand2 = lookup(operand2)
        result = operand1 / operand2
        opPush(result)
    else:
        print("Error; not enough operands on operator stack for div")

def mod ():
    if len(opStack) > 1: # If there are at least 2 operands in the stack
        operand2 = opStack.pop()
        operand1 = opStack.pop()
        if isinstance(operand1, str):
            operand1 = lookup(operand1)
        if isinstance(operand2, str):
            operand2 = lookup(operand2)
        result = operand1 % operand2
        opPush(result)
    else:
        print("Error; not enough operands on operator stack for mod")

def length ():
    array = opPop()
    if isinstance(array, list):
        opPush(len(array))
    else:
        print("Error; not an array")

def get ():
    index = opPop()
    array = opPop()
    if isinstance(array, list) and index < len(array): # If the index is in the bounds of the array
        opPush(array[index])
    else:
        print("Error; either not an array or index was out of bounds")

def psFor():
    codeArray = opPop()
    final = opPop()
    increment = opPop()
    initial = opPop()
    if isinstance(codeArray, list):
        if increment > 0:
            for x in range(initial, final+1, increment):
                opPush(x)
                interpret(codeArray)
        if increment < 0:
            for x in range (initial, final, increment):
                opPush(x)
                interpret(codeArray)
    else:
        print("Error; not a code array")

def forall():
    codeArray = opPop()
    array = opPop()
    if isinstance(array, list):
        for element in array:
            opPush(element)
            interpret(codeArray)
    else:
        print("Error; either not an array or not a code array")

def dup ():
    if len(opStack) > 0: #Make sure there is at least one thing to copy
        if isinstance(opStack[-1],str): # If the top element is a variable, get it from the dictionary
            temp = lookup(opStack[-1])
            opPush(temp)
        else: # If the top element is a number, push it to the stack again to make a copy
            opPush(opStack[-1])
    else:
        print("Error; empty operand stack")

def exch ():
    if len(opStack) > 1:
        top = opPop()
        second = opPop()
        opPush(top)
        opPush(second)
    else:
        print("Error; not enough operands on operator stack for exch")

def pop ():
    opPop()

def roll ():
    rollAmount = opPop() # How many numbers to roll
    rollElements = opPop() # Indeces to roll
    if rollAmount <= len(opStack):
        tempStack = opStack[len(opStack)-rollElements:] # Get a sublist of the elements to roll
        for i in range(rollElements):
            opPop() # Pop the elements that will be rolled
        if rollAmount < 0: #Negative: Bottom value(s) move to the top (front elements (0) move to the end (n) )
            for number in range(abs(rollAmount)):
                temp = tempStack[0] # Get value of the front element
                tempStack.append(temp) # Push to the end of the list
                tempStack.remove(temp) # Pop from the front
        else: #Positive: Top value(s) move to the bottom (end elements (n) move to the front (0) )
            for number in range(rollAmount):
                temp = tempStack.pop() # Get the end of the list, and pop it
                tempStack.insert(0, temp) # Insert at front
        for everything in range(len(tempStack)):
            opPush(tempStack[everything]) # Push the elements in their new order
    else:
        print("Error; not enough operands in operator stack to roll")

def copy ():
    toCopy = opPop()
    if len(opStack) >= toCopy:
        for i in range(toCopy):
            opPush(opStack[i])

def clear ():
    opStack.clear()
    dictStack.clear()

def stack():
    print(opStack)

def psDict (): # Changed from dict because that is a keyword in Python
    size = opPop()
    opStack.append({})

def begin ():
    newDict = opPop()
    if isinstance(newDict, dict):
        dictStack.append(newDict)
    else:
        print("Error; cannot push non-dictionary to dictionary stack")

def end ():
    if len(dictStack) > 0:
        dictPop()
    else:
        print("Error; empty dictionary stack")

def psDef ():
    if len(opStack) > 1:
        value = opPop()
        name = opPop()
        name = name[1:] # Get rid of the /
        define(name, value)
    else:
        print("Error; not enough operands on operator stack for psDef")

def tokenize(s):
    retValue = re.findall("/?[a-zA-Z][a-zA-Z0-9_]*|[[][a-zA-Z0-9_\s!][a-zA-Z09_\s!]*[]]|[-]?[0-9]+|[}{]+|%.*|[^ \t\n]", s)
    return retValue

def groupMatching(it):
    res = ['(']
    for c in it:
        if c == ')':
            res.append(')')
            return res
        else:
            res.append(groupMatching(it))
    return False

def group(s):
    if s[0] == '(':
        return groupMatching(iter(s[1:]))
    else: return False

def parseMatching(it):
    res = []
    for c in it:
        if c == '}' or c == ']':
            return res
        elif c == '{' or c == '[': # Beginning of a new array or a new code array
            res.append(parseMatching(it)) # For each new array or code array, recursively create a list within res
        elif c.isnumeric() or c[0] == '-': # If c is a positive number then c.isnumeric will be true, if c is a negative number then c[0] == '-' will be true
            res.append(int(c))
        else:
            res.append(c)
    return False

#parse: Takes a list of tokens, finds matching curly braces, and returns a code array
def parse(tokens):
    if tokens[0] == '{':
        return parseMatching(iter(tokens[1:]))
    else: return False

#interpret: Takes a list of tokens and decides what to do with it
def interpret(code):
    functionDict = {'add':add, 'sub':sub, 'mul':mul, 'div':div, 'mod':mod, 'def':psDef, 'length':length, 'get':get, 'dup':dup, 'stack':stack, 'clear':clear,
                    'exch':exch, 'pop':pop, 'roll':roll, 'copy':copy, 'dict':psDict, 'begin':begin, 'end':end, 'for':psFor, 'forall':forall}
    for word in code:
        if isinstance(word, list) or word not in functionDict.keys(): # If word is a list (code array or integer array), variable name, or number
            opPush(word)
        else: # If word is a keyword
            functionDict[word]() # Call the function

def interpreter(s):
    interpret(parse(tokenize(s)))

def testParse():
    testString1 = parse(tokenize("{Testing {Hello World} }"))
    if testString1 != ['Testing', ['Hello', 'World']]:
        return False
    testString2 = parse(tokenize("{/n 5 def n -1 1 {mul} }"))
    if testString2!= ['/n', 5, 'def', 'n', -1, 1, ['mul']]:
        return False
    testString3 = parse(tokenize("{ /sum { -1 0 {add} for} def 0 [1 2 3 4] length sum 2 mul [1 2 3 4] {2 mul} forall add add add stack }"))
    if testString3 != ['/sum', [-1, 0, ['add'], 'for'], 'def', 0, [1, 2, 3, 4], 'length', 'sum', 2, 'mul', [1, 2 , 3, 4], [2, 'mul'], 'forall', 'add', 'add', 'add', 'stack']:
        return False
    return True

def testInterpreter():
    interpreter("{6 4 add 10 5 sub 8 3 mul 100 25 div 42 7 mod}")
    if opStack != [10, 5, 24, 4, 0]:
        return False
    clear()
    interpreter("{1 2 3 4 5 6 4 2 roll}")
    if opStack != [1, 2, 5, 6, 3, 4]:
        return False
    clear()
    interpreter("{/x 4 def x x add}")
    if opPop() != 8:
        return False
    clear()
    interpreter("{ [1 2 3 4 5] length dup [1 2 3 4 5] 3 get }")
    if opStack != [5, 5, 4]:
        return False
    clear()
    interpreter("{/testFunction { 1 1 3 {10 mul } for } def testFunction }")
    if opStack != [10, 20, 30]:
        return False
    clear()
    interpreter("{ /fact { 0 dict begin /n exch def 1 n -1 1 {mul} for end } def [1 2 3 4 5] dup 4 get pop length fact stack }")
    if (opPop() != 120):
        return False
    clear()
    interpreter("{ /sum { -1 0 {add} for} def 0 [1 2 3 4] length sum 2 mul [1 2 3 4] {2 mul} forall add add add stack}")
    if (opStack != [20, 20]):
        return False
    return True

if __name__ == '__main__':
    debugging = True
    def debug(*s):
        if debugging:
            print(*s)
    testCases = [("Parse", testParse()), ("Interpreter", testInterpreter())]
    debug(testCases)