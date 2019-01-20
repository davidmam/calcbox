# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 08:35:13 2019

@author: David
"""

import random,csv

KEYWORDS = """False       class        finally     is               return
None       continue   for          lambda      try
True        def            from       nonlocal    while
and         del            global     not            with
as           elif             if              or              yield
assert     else          import    pass
break      except      in            raise""".split()

NOTKEYWORDS = "finish length elseif delete remove last module array dictionary whilst define function".split()

RANDOMWORDS = [x.strip() for x in open('words_alpha.txt','r').readlines()]

def arrayq1(qid):
    question = {'qtype': 'MC', 'correct': [], 'incorrect': [], 'prompt': ''}
    arr = get_random_array()
    index = random.randint(0,len(arr)-1) 
    text = """Given the list arr = {}, give the code which will retrieve the element with value {}"""
    question['prompt'] = text.format(str(arr), arr[index])
    question['correct'].append("arr[{}]".format(index))
    question['incorrect'].append( "arr({})".format(index))
    question['incorrect'].append( "arr{{{}}}".format(index+1))
    question['incorrect'].append( "arr({})".format(index+1))
    question['incorrect'].append( "arr[{}]".format(index+1))
    return question

def arrayq2(qid):
    question = {'qtype': 'MC', 'correct': [], 'incorrect': [], 'prompt': ''}
    arr = get_random_array()
    index = random.randint(1,len(arr)-2) 
    text = """Given the list arr = {}, give the value which will be returned with the code {}"""
    question['prompt'] = text.format(str(arr), "arr[{}]".format(index))
    question['correct'].append(arr[index])
    question['incorrect'].append( arr[index+1])
    question['incorrect'].append( arr[index-1])
    question['incorrect'].append( "An error occurs")
    return question

def arrayq3(qid):    
    question = {'qtype': 'MC', 'correct': [], 'incorrect': [], 'prompt': ''}
    arr = get_random_array()
    index = random.randint(1,len(arr)-2) 
    incorrect = ("arr({})", "arr{{{}}}")
    text = """Given the list arr = {}, give the value which will be returned with the code {}"""
    question['prompt'] = text.format(str(arr), random.choice(incorrect).format(index))
    question['correct'].append("An error occurs")
    question['incorrect'].append(arr[index+1])
    question['incorrect'].append(arr[index])
    question['incorrect'].append(arr[index-1])

    return question
    
def arrayq4(qid):
    question = {'qtype': 'MC', 'correct': [], 'incorrect': [], 'prompt': ''}
    arr = get_random_array(6,11)
    startindex = random.randint(1,int(len(arr)/3))
    endindex = random.randint(startindex+1, len(arr)-2)
    text = """Given the list arr = {}, give the values which will be returned with the code {}"""
    question['prompt'] = text.format(str(arr), "arr[{}:{}]".format(startindex, endindex))
    question['correct'].append(arr[startindex:endindex])
    question['incorrect'].append(arr[startindex:endindex+1])
    question['incorrect'].append(arr[startindex-1:endindex])
    question['incorrect'].append(arr[startindex-1:endindex-1])
    return question

def arrayq5(qid):
    question = {'qtype': 'MC', 'correct': [], 'incorrect': [], 'prompt': ''}
    arr = get_random_array()
    startindex = random.randint(1,int(len(arr)/3))
    endindex = random.randint(startindex+1, len(arr)-2)
    text = """Given the list arr = {}, give the code which will return the values {}"""
    question['prompt'] = text.format(str(arr), arr[startindex:endindex])
    question['correct'].append("arr[{}:{}]".format(startindex,endindex))
    question['incorrect'].append("arr[{}:{}]".format(startindex,endindex-1))
    question['incorrect'].append("arr[{}:{}]".format(startindex+1,endindex))
    question['incorrect'].append("An error occurs")
    return question

def arrayq6(qid):
    question = {'qtype': 'MC', 'correct': [], 'incorrect': [], 'prompt': ''}
    arr = get_random_array()
    startindex = random.randint(1,int(len(arr)/3))
    endindex = random.randint(startindex+1, len(arr)-2)
    text = """Given the list arr = {}, give the code which will return the values {}"""
    question['prompt'] = text.format(str(arr), arr[startindex:endindex])
    question['correct'].append("arr[{}:{}]".format(startindex,endindex))
    question['incorrect'].append("arr[{},{}]".format(startindex,endindex))
    question['incorrect'].append("arr[{}-{}]".format(startindex,endindex))
    question['incorrect'].append("arr({}:{})".format(startindex,endindex))
    question['incorrect'].append("An error occurs")
    return question

def varq7(qid):
    question = {'qtype': 'MC', 'correct': [], 'incorrect': [], 'prompt': ''}
    var = random.random()*random.randint(1,10)
    options=(str, int, float)
    var = random.choice(options)(round(var,0))
    if type(var).__name__ == 'str':
        var = "'{}'".format(var)
    text = """<![CDATA[If the variable <tt>code</tt> gives the following result when queried, what is the type of the variable?
    <code>&gt; var
    {}
    </code>]]>"""
    question['prompt'] = text.format(var)
    question['correct'].append(type(var).__name__)
    opts = ['str','int','float']
    opts.remove(type(var).__name__)
    for t in opts:
        question['incorrect'].append("{}".format(t))
    question['incorrect'].append("Something else")
    return question

def varq8(qid):
    question = {'qtype': 'MC', 'correct': [], 'incorrect': [], 'prompt': ''}
    
    var1 = random.random()*random.randint(1,10)
    var2 = random.random()*random.randint(1,10)
    options=(str, int, float)
    var1 = random.choice(options)(round(var1,0))
    var2 = random.choice(options)(round(var2,0))
    
    try:
        correct = type(var1 + var2).__name__
    except:
        correct = "An error occurs"
    if type(var1).__name__ == 'str':
        var1 = "'{}'".format(var1)
    if type(var2).__name__ == 'str':
        var2 = "'{}'".format(var2)
    text = """<![CDATA[What is the type of the variable <tt>c</tt> after the following code has been excecuted?
    <code>&gt; a = {}
    &gt; b = {}
    &gt; c = a + b
    </code>]]>"""
    question['prompt'] = text.format(var1,var2)
    question['correct'].append(correct)
    opts = ['str','int','float']
    if correct in opts:
        opts.remove(correct)
        question['incorrect'].append("An error occurs")
    for a in opts:
        question['incorrect'].append(a)
    return question

def varq9(qid):
    question = {'qtype': 'MR', 'correct': [], 'incorrect': [], 'prompt': ''}
    question['prompt'] ="Which of the following are legitimate variable names? Select all that apply."
    question['incorrect'].append(random.choice(KEYWORDS))
    question['correct'].append(random.choice(NOTKEYWORDS))
    word = random.choice(RANDOMWORDS)
    if word in KEYWORDS:
        question['incorrect'].append(word)
    else:
        question['correct'].append(word)
    word = random.choice(RANDOMWORDS)
    question['incorrect'].append(word + random.choice([" ",".","-"])+str(random.randint(0,9)))
    words = random.choices(RANDOMWORDS, k=random.randint(2,5))
    question['incorrect'].append(random.choice([" ","-","."]).join([x.capitalize() for x in words]))
    words = random.choices(RANDOMWORDS, k=random.randint(2,5))
    question['correct'].append(random.choice(["","_"]).join([x.capitalize() for x in words]))
    return question

def dictq10(qid):
    question = {'qtype': 'MC', 'correct': [], 'incorrect': [], 'prompt': ''}
    count = random.randint(3,7)
    words = random.choices(RANDOMWORDS, k=count)
    numbers = []
    for p in range(count):
        numbers.append(random.randint(1,100))
    d = dict(zip(words,numbers))
    keypairs = ", ".join(["'{}' &rarr; {}".format(k,v) for k,v in d.items()])

    question['prompt'] = "<![CDATA[Which of the following is the correct way to define the dictionary <tt>d</tt> for the key &rarr; value pairs {kv} ?.]]>".format( kv=keypairs)
    question['correct'].append("d = {}".format(str(d)))
    question['incorrect'].append("d = {}".format(list(d.items())))
    question['incorrect'].append("d = {{{}}}".format(", ".join(["{} : {}".format(k,v) for k,v in d.items()])))
    question['incorrect'].append( "d = {{{}}}".format(list(d.items())))
    return question

def dictq11(qid):
    question = {'qtype': 'MC', 'correct': [], 'incorrect': [], 'prompt': ''}
    count = random.randint(3,7)
    words = random.choices(RANDOMWORDS, k=count)
    numbers = []
    randkey = random.choice(words)
    for p in range(count):
        numbers.append(random.randint(1,100))
    d = dict(zip(words,numbers))
    keypairs = ", ".join(["'{}' &rarr; {}".format(k,v) for k,v in d.items()])
    question['prompt'] = '<![CDATA[Which of the following is the correct way to retrieve the value indexed by <tt>{key}</tt> from the dictionary <tt>d</tt> containing the following key &rarr; value pairs: {kv}?  ]]>'.format( key=randkey, kv=keypairs)
    question['correct'].append("d['{}']".format(randkey))
    question['incorrect'].append("d[{}]".format(randkey))
    question['incorrect'].append("d{{{}}}".format(randkey))
    question['incorrect'].append("d{{'{}'}}".format(randkey))
    question['incorrect'].append("d({})".format(randkey))
    question['incorrect'].append("d<{}>".format(randkey))
    return question

def listq12(qid):
    question = {'qtype': 'MC', 'correct': [], 'incorrect': [], 'prompt': ''}
    dim1 = random.randint(3,5)
    dim2 = random.randint(2,4)
    arr=[]
    for p in range(dim1):
        arr.append( [round(random.random()*random.randint(1,10),2) for __ in range(dim2)])
    qdim1 = random.randint(0,dim1-1)
    qdim2 = qdim1
    while qdim2 == qdim1:
        qdim2 =random.randint(0,dim2-1)
    question['prompt'] = '<![CDATA[Which of the following is the correct way to retrieve the value {val} from the list <tt>l</tt> {lv}?  ]]>'.format( val=arr[qdim1][qdim2], lv=str(arr))
    question['correct'].append("l[{d1}][{d2}]".format(d1=qdim1, d2=qdim2))
    question['incorrect'].append("l[{d1},{d2}]".format(d1=qdim1, d2=qdim2))
    question['incorrect'].append("l[{d1}:{d2}]".format(d1=qdim1, d2=qdim2))
    question['incorrect'].append("l[{d1}][{d2}]".format(d1=qdim1+1, d2=qdim2+1))
    question['incorrect'].append("l[{d1},{d2}]".format(d1=qdim1+1, d2=qdim2+1))
    question['incorrect'].append("l[{d1}:{d2}]".format(d1=qdim1+1, d2=qdim2+1))
    return question
    
def listq13(qid):
    question = {'qtype': 'MC', 'correct': [], 'incorrect': [], 'prompt': ''}
    dim1 = random.randint(3,5)
    dim2 = random.randint(3,4)
    #print(qid,":")
    arr=[]
    for p in range(dim1):
        arr.append( [round(random.random()*random.randint(1,10),2) for __ in range(dim2)])
    qdim1 = random.randint(0,min(dim1,dim2)-2)
    qdim2 = qdim1
    while qdim2 == qdim1:
        qdim2 =random.randint(0,min(dim1,dim2)-2)
    question['prompt'] = '<![CDATA[Which of the following is the value returned by <tt>{val}</tt> from the list <code>l =  {lv}</code>?  ]]>'.format( val=arr[qdim1][qdim2], lv=str(arr))
    question['correct'].append("{}".format(arr[qdim1][qdim2]))
    question['incorrect'].append("{}".format(arr[qdim1+1][qdim2+1]))
    question['incorrect'].append("{}".format(arr[qdim2][qdim1]))
    question['incorrect'].append("{}".format(arr[qdim2+1][qdim1+1]))
    question['incorrect'].append("An error occurs")
    return question
    


        
def get_random_array(lenfrom=5, lento=10):   
    arr = []
    for p in range(random.randint(lenfrom, lento)):
        arr.append(random.random()*random.randint(1,10))
    arr = [round(x, 2) for x in set(arr)]
    return arr

def qtoCSV(q,csvfh):
    line=[q.get('qtype', 'MC'), q.get('prompt', 'No Question')]
    for c in q['correct']:
        line += [c, 1, 'Correct']
    for i in q['incorrect']:
        line += [i, 0, 'Wrong']
    csvfh.writerow(line)
    