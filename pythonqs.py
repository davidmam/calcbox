# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 08:35:13 2019

@author: David
"""

import random

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
    arr = get_random_array()
    index = random.randint(0,len(arr)-1) 
    text = """Given the array arr = {}, give the code which will retrieve the element with value {}"""
    qtext = '''Q: Array Question {qid}
T: MC
D: {text}
C+: {correct}
'''.format(qid=qid, text=text.format(str(arr), arr[index]), correct="arr[{}]".format(index))
    qtext += "C: arr({})\n".format(index)
    qtext += "C: arr{{{}}}\n".format(index+1)
    qtext += "C: arr({})\n".format(index+1)
    qtext += "C: arr[{}]\n".format(index+1)
    return qtext

def arrayq2(qid):
    arr = get_random_array()
    index = random.randint(1,len(arr)-1) 
    text = """Given the array arr = {}, give the value which will be returned with the code {}"""
    qtext = '''Q: Array Question {qid}
T: MC
D: {text}
C+: {correct}
'''.format(qid=qid, text=text.format(str(arr), "arr[{}]".format(index)), correct=arr[index])
    qtext += "C: {}\n".format(arr[index+1])
    qtext += "C: {}\n".format(arr[index-1])
    qtext += "C: An error occurs\n"
    return qtext

def arrayq3(qid):    
    arr = get_random_array()
    index = random.randint(1,len(arr)-1) 
    text = """Given the array arr = {}, give the value which will be returned with the code {}"""
    incorrect = ("arr({})", "arr{{{}}}")
    qtext = '''Q: Array Question {qid}
T: MC
D: {text}
C+: {correct}
'''.format(qid=qid, text=text.format(str(arr), random.choice(incorrect).format(index)), 
    correct="An error occurs")
    qtext += "C: {}\n".format(arr[index+1])
    qtext += "C: {}\n".format(arr[index-1])
    qtext += "C: {}\n".format(arr[index])
    return qtext
    
def arrayq4(qid):
    arr = get_random_array()
    startindex = random.randint(1,len(arr)-int(len(arr)/3))
    endindex = random.randint(startindex+1, len(arr)-1)
    text = """Given the array arr = {}, give the values which will be returned with the code {}"""
    qtext = '''Q: Array Question {qid}
T: MC
D: {text}
C+: {correct}
'''.format(qid=qid, text=text.format(str(arr), "arr[{}:{}]".format(startindex, endindex)), 
    correct= arr[startindex:endindex])
    qtext += "C: {}\n".format(arr[startindex:endindex+1])
    qtext += "C: {}\n".format(arr[startindex-1:endindex])
    qtext += "C: {}\n".format(arr[startindex-1:endindex-1])
    qtext += "C: An error occurs\n"
    return qtext

def arrayq5(qid):
    arr = get_random_array()
    startindex = random.randint(1,len(arr)-int(len(arr)/3))
    endindex = random.randint(startindex+1, len(arr)-1)
    text = """Given the array arr = {}, give the code which will return the values {}"""
    qtext = '''Q: Array Question {qid}
T: MC
D: {text}
C+: {correct}
'''.format(qid=qid, text=text.format(str(arr), arr[startindex:endindex]), 
    correct= "arr[{}:{}]".format(startindex,endindex))
    qtext += "C: arr[{}:{}]\n".format(startindex,endindex-1)
    qtext += "C: arr[{}:{}]\n".format(startindex+1,endindex)
    qtext += "C: arr[{}:{}]\n".format(startindex+1,endindex+1)
    qtext += "C: An error occurs\n"
    return qtext

def arrayq6(qid):
    arr = get_random_array()
    startindex = random.randint(1,len(arr)-int(len(arr)/3))
    endindex = random.randint(startindex+1, len(arr)-1)
    text = """Given the array arr = {}, give the code which will return the values {}"""
    qtext = '''Q: Array Question {qid}
T: MC
D: {text}
C+: {correct}
'''.format(qid=qid, text=text.format(str(arr), arr[startindex:endindex]), 
    correct= "arr[{}:{}]".format(startindex,endindex))
    qtext += "C: arr[{},{}]\n".format(startindex,endindex)
    qtext += "C: arr[{}-{}]\n".format(startindex,endindex)
    qtext += "C: arr({}:{})\n".format(startindex,endindex)
    qtext += "C: An error occurs\n"
    return qtext

def varq7(qid):
    var = random.random()*random.randint(1,10)
    options=(str, int, float)
    var = random.choice(options)(round(var,0))
    if type(var).__name__ == 'str':
        var = "'{}'".format(var)
    text = """<![CDATA[If the variable <tt>code</tt> gives the following result when queried, what is the type of the variable?
    <code>&gt; var
    {}
    </code>]]>"""
    qtext = '''Q: Variable Question {qid}
T: MC
D: {text}
C+: {correct}
'''.format(qid=qid, text=text.format(var), 
    correct= type(var).__name__)
    opts = ['str','int','float']
    opts.remove(type(var).__name__)
    for t in opts:
        qtext += "C: {}\n".format(t)
    qtext += "C: Something else\n"
    return qtext

def varq8(qid):
    
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
    qtext = '''Q: Variable Question {qid}
T: MC
D: {text}
C+: {correct}
'''.format(qid=qid, text=text.format(var1,var2), 
    correct=correct)
    opts = ['str','int','float']
    if correct in opts:
        opts.remove(correct)
        qtext += "C: An error occurs\n"
    for a in opts:
        qtext += "C: {}\n".format(a)
    return qtext

def varq9(qid):
    qtext = '''Q: Variable Question {qid}
T: MR
D: Which of the following are legitimate variable names? Select all that apply.
'''
    qtext += "C: {}\n".format(random.choice(KEYWORDS))
    qtext += "C+: {}\n".format(random.choice(NOTKEYWORDS))
    word = random.choice(RANDOMWORDS)
    if word in KEYWORDS:
        qtext += "C: {}\n".format(word)
    else:
        qtext += "C+: {}\n".format(word)
    word = random.choice(RANDOMWORDS)
    qtext += "C: {}\n".format(word + random.choice([" ",".","-"])+str(random.randint(0,9)))
    words = random.choices(RANDOMWORDS, k=random.randint(2,5))
    qtext += "C: {}\n".format(random.choice([" ","-","."]).join([x.capitalize() for x in words]))
    words = random.choices(RANDOMWORDS, k=random.randint(2,5))
    qtext += "C+: {}\n".format(random.choice(["","_"]).join([x.capitalize() for x in words]))
    
    return qtext

def dictq10(qid):
    count = random.randint(3,7)
    words = random.choices(RANDOMWORDS, k=count)
    numbers = []
    for p in range(count):
        numbers.append(random.randint(1,100))
    d = dict(zip(words,numbers))
    keypairs = ", ".join(["'{}' &rarr; {}".format(k,v) for k,v in d.items()])

    qtext = '''Q: Dictionary Question {qid}
T: MC
D: <![CDATA[Which of the following is the correct way to define the dictionary <tt>d</tt> for the key &rarr; value pairs {kv} ?.
]]>'''.format(qid=qid, kv=keypairs)
    qtext += "C+: d = {}\n".format(str(d))
    qtext += "C: d = [{}]\n".format(list(d.items()))
    qtext += "C: d = {{{}}}\n".format(", ".join(["{} : {}".format(k,v) for k,v in d.items()]))
    qtext += "C: d = {{{}}}\n".format(list(d.items()))
    return qtext

def dictq11(qid):
    count = random.randint(3,7)
    words = random.choices(RANDOMWORDS, k=count)
    numbers = []
    randkey = random.choice(words)
    for p in range(count):
        numbers.append(random.randint(1,100))
    d = dict(zip(words,numbers))
    keypairs = ", ".join(["'{}' &rarr; {}".format(k,v) for k,v in d.items()])
    qtext = '''Q: Dictionary Question {qid}
T: MC
D: <![CDATA[Which of the following is the correct way to retrieve the value indexed by <tt>{key}</tt> from the dictionary <tt>d</tt> containing the following key &rarr; value pairs: {kv}?  
]]>'''.format(qid=qid, key=randkey, kv=keypairs)
    qtext += "C+: d['{}']\n".format(randkey)
    qtext += "C: d[{}]\n".format(randkey)
    qtext += "C: d{{{}}}\n".format(randkey)
    qtext += "C: d{{'{}'}}\n".format(randkey)
    qtext += "C: d({})\n".format(randkey)
    qtext += "C: d<{}>\n".format(randkey)
    return qtext

def listq12(qid):
    dim1 = random.randint(3,5)
    dim2 = random.randint(2,4)
    
    arr=[]
    for p in range(dim1):
        arr.append( [round(random.random()*random.randint(1,10),2) for __ in range(dim2)])
    qdim1 = random.randint(0,dim1-1)
    qdim2 = qdim1
    while qdim2 == qdim1:
        qdim2 =random.randint(0,dim2-1)
    qtext = '''Q: Dictionary Question {qid}
T: MC
D: <![CDATA[Which of the following is the correct way to retrieve the value {val} from the list <tt>l</tt> {lv}?  
]]>'''.format(qid=qid, val=arr[qdim1][qdim2], lv=str(arr))
    qtext += "C+: l[{d1}][{d2}]\n".format(d1=qdim1, d2=qdim2)
    qtext += "C: l[{d1},{d2}]\n".format(d1=qdim1, d2=qdim2)
    qtext += "C: l[{d1}:{d2}]\n".format(d1=qdim1, d2=qdim2)
    qtext += "C: l[{d1}][{d2}]\n".format(d1=qdim1+1, d2=qdim2+1)
    qtext += "C: l[{d1},{d2}]\n".format(d1=qdim1+1, d2=qdim2+1)
    qtext += "C: l[{d1}:{d2}]\n".format(d1=qdim1+1, d2=qdim2+1)
    return qtext
    
def listq13(qid):
    dim1 = random.randint(3,5)
    dim2 = random.randint(3,4)
    
    arr=[]
    for p in range(dim1):
        arr.append( [round(random.random()*random.randint(1,10),2) for __ in range(dim2)])
    qdim1 = random.randint(0,min(dim1,dim2)-2)
    qdim2 = qdim1
    while qdim2 == qdim1:
        qdim2 =random.randint(0,min(dim1,dim2)-2)
    qtext = '''Q: Dictionary Question {qid}
T: MC
D: <![CDATA[Which of the following is the value returned by <tt>{val}</tt> from the list <code>l =  {lv}</code>?  
]]>'''.format(qid=qid, val="arr[{}][{}]".format(qdim1,qdim2), lv=str(arr))
    qtext += "C+: {}\n".format(arr[qdim1][qdim2])
    qtext += "C: {}\n".format(arr[qdim1+1][qdim2+1])
    qtext += "C: {}\n".format(arr[qdim2][qdim1])
    qtext += "C: {}\n".format(arr[qdim2+1][qdim1+1])
    qtext += "C: An error occurs\n"
    return qtext
    
        

def get_random_array(lenfrom=5, lento=10):   
    arr = []
    for p in range(random.randint(lenfrom, lento)):
        arr.append(random.random()*random.randint(1,10))
    arr = [round(x, 2) for x in set(arr)]
    return arr
        