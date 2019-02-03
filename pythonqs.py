# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 08:35:13 2019

@author: David
"""

import random,csv
import xml.dom.minidom as xmldom

QML_HEADER = """<?xml version="1.0" encoding="utf-8" standalone="no"?>
<!DOCTYPE QML SYSTEM "QML_V3.dtd">
<QML>
"""

METHODLIST = [arrayq1, arrayq2,arrayq3,arrayq4,arrayq5,arrayq6,varq7,varq8,varq9,dictq10,dictq11,listq12,listq13, arrayq14]

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
    question = {'qtype': 'MC', 'correct': [], 'incorrect': [], 'prompt': '', 'description':'listq 1 {}'.format(qid) }
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
    question = {'qtype': 'MC', 'correct': [], 'incorrect': [], 'prompt': '', 'description':'listq 2 {}'.format(qid)}
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
    question = {'qtype': 'MC', 'correct': [], 'incorrect': [], 'prompt': '', 'description':'listq 3 {}'.format(qid)}
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
    question = {'qtype': 'MC', 'correct': [], 'incorrect': [], 'prompt': '', 'description':'listq 4 {}'.format(qid)}
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
    question = {'qtype': 'MC', 'correct': [], 'incorrect': [], 'prompt': '', 'description':'listq 5 {}'.format(qid)}
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
    question = {'qtype': 'MC', 'correct': [], 'incorrect': [], 'prompt': '', 'description':'listq 6 {}'.format(qid)}
    arr = get_random_array()
    startindex = random.randint(1,int(len(arr)/3))
    endindex = random.randint(startindex+1, len(arr)-2)
    text = """Given the list arr = {}, give the code which will return the values {}"""
    question['prompt'] = text.format(str(arr), arr[startindex:endindex])
    question['correct'].append("arr[{}:{}]".format(startindex,endindex))
    question['incorrect'].append("arr[{},{}]".format(startindex,endindex))
    question['incorrect'].append("arr[{}-{}]".format(startindex,endindex))
    question['incorrect'].append("arr({}:{})".format(startindex,endindex))
    return question
def arrayq14(qid):
    question = {'qtype': 'MC', 'correct': [], 'incorrect': [], 'prompt': '', 'description':'arrayq 14 {}'.format(qid)}
    arr = get_random_array()
    startindex = random.randint(1,int(len(arr)/3))
    endindex = random.randint(startindex+1, len(arr)-2)
    text = """Given the list arr = {}, give the code which will return the values {}"""
    question['prompt'] = text.format(str(arr), arr[startindex:endindex])
    question['correct'].append("arr[{}:{}]".format(startindex,endindex))
    question['incorrect'].append("arr[{}:{}]".format(startindex+1,endindex))
    question['incorrect'].append("arr[{}:{}]".format(startindex,endindex-1))
    question['incorrect'].append("arr[{}:{}]".format(startindex+1,endindex+1))
    return question

def varq7(qid):
    question = {'qtype': 'MC', 'correct': [], 'incorrect': [], 'prompt': '', 'description':'varq 7 {}'.format(qid)}
    var = random.random()*random.randint(1,10)
    options=(str, int, float)
    var = random.choice(options)(round(var,0))
    if type(var).__name__ == 'str':
        var = "'{}'".format(var)
    text = """If the variable <tt>code</tt> gives the following result when queried, what is the type of the variable?
    <code>&gt; var
    {}
    </code>"""
    question['prompt'] = text.format(var)
    question['correct'].append(type(var).__name__)
    opts = ['str','int','float']
    opts.remove(type(var).__name__)
    for t in opts:
        question['incorrect'].append("{}".format(t))
    question['incorrect'].append("Something else")
    return question

def varq8(qid):
    question = {'qtype': 'MC', 'correct': [], 'incorrect': [], 'prompt': '', 'description':'varq 8 {}'.format(qid)}
    
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
    text = """What is the type of the variable <tt>c</tt> after the following code has been excecuted?
    <code>&gt; a = {}
    &gt; b = {}
    &gt; c = a + b
    </code>"""
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
    question = {'qtype': 'MR', 'correct': [], 'incorrect': [], 'prompt': '', 'description':'varq 9 {}'.format(qid)}
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
    question = {'qtype': 'MC', 'correct': [], 'incorrect': [], 'prompt': '', 'description':'dictq 10 {}'.format(qid)}
    count = random.randint(3,7)
    words = random.choices(RANDOMWORDS, k=count)
    numbers = []
    for p in range(count):
        numbers.append(random.randint(1,100))
    d = dict(zip(words,numbers))
    keypairs = ", ".join(["'{}' &rarr; {}".format(k,v) for k,v in d.items()])

    question['prompt'] = "Which of the following is the correct way to define the dictionary <tt>d</tt> for the key &rarr; value pairs {kv} ?.".format( kv=keypairs)
    question['correct'].append("d = {}".format(str(d)))
    question['incorrect'].append("d = {}".format(list(d.items())))
    question['incorrect'].append("d = {{{}}}".format(", ".join(["{} : {}".format(k,v) for k,v in d.items()])))
    question['incorrect'].append( "d = {{{}}}".format(list(d.items())))
    return question

def dictq11(qid):
    question = {'qtype': 'MC', 'correct': [], 'incorrect': [], 'prompt': '', 'description':'dictq 11 {}'.format(qid)}
    count = random.randint(3,7)
    words = random.choices(RANDOMWORDS, k=count)
    numbers = []
    randkey = random.choice(words)
    for p in range(count):
        numbers.append(random.randint(1,100))
    d = dict(zip(words,numbers))
    keypairs = ", ".join(["'{}' &rarr; {}".format(k,v) for k,v in d.items()])
    question['prompt'] = 'Which of the following is the correct way to retrieve the value indexed by <tt>{key}</tt> from the dictionary <tt>d</tt> containing the following key &rarr; value pairs: {kv}? '.format( key=randkey, kv=keypairs)
    question['correct'].append("d['{}']".format(randkey))
    question['incorrect'].append("d[{}]".format(randkey))
    question['incorrect'].append("d{{{}}}".format(randkey))
    question['incorrect'].append("d{{'{}'}}".format(randkey))
    question['incorrect'].append("d({})".format(randkey))
    question['incorrect'].append("d<{}>".format(randkey))
    return question

def listq12(qid):
    question = {'qtype': 'MC', 'correct': [], 'incorrect': [], 'prompt': '', 'description':'listq 12 {}'.format(qid)}
    dim1 = random.randint(3,5)
    dim2 = random.randint(2,4)
    arr=[]
    for p in range(dim1):
        arr.append( [round(random.random()*random.randint(1,10),2) for __ in range(dim2)])
    qdim1 = random.randint(0,dim1-1)
    qdim2 = qdim1
    while qdim2 == qdim1:
        qdim2 =random.randint(0,dim2-1)
    question['prompt'] = 'Which of the following is the correct way to retrieve the value {val} from the list <tt>l</tt> {lv}? '.format( val=arr[qdim1][qdim2], lv=str(arr))
    question['correct'].append("l[{d1}][{d2}]".format(d1=qdim1, d2=qdim2))
    question['incorrect'].append("l[{d1},{d2}]".format(d1=qdim1, d2=qdim2))
    question['incorrect'].append("l[{d1}:{d2}]".format(d1=qdim1, d2=qdim2))
    question['incorrect'].append("l[{d1}][{d2}]".format(d1=qdim1+1, d2=qdim2+1))
    question['incorrect'].append("l[{d1},{d2}]".format(d1=qdim1+1, d2=qdim2+1))
    question['incorrect'].append("l[{d1}:{d2}]".format(d1=qdim1+1, d2=qdim2+1))
    return question
    
def listq13(qid):
    question = {'qtype': 'MC', 'correct': [], 'incorrect': [], 'prompt': '', 'description':'listq 13 {}'.format(qid)}
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
    question['prompt'] = 'Which of the following is the value returned by <tt>{val}</tt> from the list <code>l =  {lv}</code>?'.format( val=arr[qdim1][qdim2], lv=str(arr))
    question['correct'].append("{}".format(arr[qdim1][qdim2]))
    question['incorrect'].append("{}".format(arr[qdim1+1][qdim2+1]))
    question['incorrect'].append("{}".format(arr[qdim2][qdim1]))
    question['incorrect'].append("{}".format(arr[qdim2+1][qdim1+1]))
    question['incorrect'].append("An error occurs")
    return question
    
def rangeq14(qid):
     '''questions based on range(x)'''
     question = {'qtype': 'MC', 'correct': [], 'incorrect': [], 'prompt': '',
      'description':'rangeq 14 {}'.format(qid)}
     i = random.randint(4,8)
     r = list(range(i))
     pos = random.randint(0, len(r))
     descriptors = ['first','second', 'third', 'fourth','fifth', 'sixth','seventh', 'eighth', 'ninth']
     question['prompt'] = 'Which of the following is the {descr} value returned by the function <tt>range({maxval})</tt>?'.format(descr=descriptors[pos],maxval=i)
     if pos == len(r):
         question['correct'].append('No such value returned')
     else:
         question['incorrect'].append('No such value returned')
         question['correct'].append(r[pos])
     for i in random.sample([x for x in r if x != pos],3):
         question['incorrect'].append(r[pos])
     return question
 
def rangeq15(qid):
     '''questions based on range(x,y)'''
     question = {'qtype': 'MC', 'correct': [], 'incorrect': [], 'prompt': '',
      'description':'rangeq 15 {}'.format(qid)}
     i = random.randint(4,8)
     j = random.randint(4,8)
     r = list(range(i,i+j))
     pos = random.randint(0, len(r))
     descriptors = ['first','second', 'third', 'fourth','fifth', 'sixth','seventh', 'eighth', 'ninth']
     question['prompt'] = 'Which of the following is the {descr} value returned by the function <tt>range({minval},{maxval})</tt>?'.format(descr=descriptors[pos],minval=i,maxval=i+j)
     if pos == len(r):
         question['correct'].append('No such value returned')
     else:
         question['incorrect'].append('No such value returned')
         question['correct'].append(r[pos])
     question['incorrect'].append('An error occurs')
     for i in random.sample([x for x in r if x != pos],3):
         question['incorrect'].append(r[pos])
     return question
 
def rangeq16(qid):
     '''questions based on range(x,y)'''
     question = {'qtype': 'MC', 'correct': [], 'incorrect': [], 'prompt': '',
      'description':'rangeq 16 {}'.format(qid)}
     i = random.randint(4,8)
     j = random.randint(4,8)
     r = list(range(i,i+j))
     pos = random.randint(0, len(r))
     descriptors = ['first','second', 'third', 'fourth','fifth', 'sixth','seventh', 'eighth', 'ninth']
     question['prompt'] = 'Which of the following is the {descr} value returned by the function <tt>range({minval}:{maxval})</tt>?'.format(descr=descriptors[pos],minval=i,maxval=i+j)
     question['correct'].append('An error occurs')
     question['incorrect'].append('No such value returned')
         
     for i in random.sample(r,3):
         question['incorrect'].append(r[pos])
     return question

def rangeq17(qid):
     '''questions based on range(x,y,z)'''
     question = {'qtype': 'MC', 'correct': [], 'incorrect': [], 'prompt': '',
      'description':'rangeq 17 {}'.format(qid)}
     i = random.randint(4,8)
     j = random.randint(4,8)
     z = random.randint(1,3)
     r = list(range(i,i+z*j,z))
     pos = random.randint(0, len(r))
     descriptors = ['first','second', 'third', 'fourth','fifth', 'sixth','seventh', 'eighth', 'ninth']
     question['prompt'] = 'Which of the following is the {descr} value returned by the function <tt>range({minval},{maxval},{stepval})</tt>?'.format(descr=descriptors[pos],minval=i,maxval=i+z*j, stepval=z)
     if pos == len(r):
         question['correct'].append('No such value returned')
     else:
         question['incorrect'].append('No such value returned')
         question['correct'].append(r[pos])
     question['incorrect'].append('An error occurs')
     for i in random.sample([x for x in r if x != pos],3):
         question['incorrect'].append(r[pos])
     return question

def formatq18(qid):
    '''questions based on string.format()'''
    formats = ["{:04d}","{: 04d}","{: 4d}","{: 4d}","{:d}","{: d}","{:03d}"]
    choice = random.randint(0,len(formats)-1)
    randomdata = int(10**(random.random()*4))
    question = {'qtype': 'MC', 'correct': [], 'incorrect': [], 'prompt': '',
      'description':'formatq 18 {}'.format(qid)}
    question['prompt'] = "Which of the following options should replace 'string' in <tt>'!string!'.format({val})</tt> to give the output <tt>!{output}!</tt>?".format(val=randomdata, output=formats[choice].format(randomdata))
    question['correct'].append(formats[choice])
    for f in random.sample([x for x in range(len(formats)) if x != choice],4):
        question['incorrect'].append(formats[f])
    return question
    
def formatq19(qid):
    '''questions based on string.format()'''
    formats = ["{:04d}","{: 04d}","{: 4d}","{: 4d}","{:d}","{: d}","{:03d}"]
    choice = random.randint(0,len(formats)-1)
    randomdata = int(10**(random.random()*4))
    question = {'qtype': 'MC', 'correct': [], 'incorrect': [], 'prompt': '',
      'description':'formatq 19 {}'.format(qid)}
    question['prompt'] = "Which of the following outputs should result from the command <tt>'!{code}!'.format({val})</tt>?".format(val=randomdata, output=formats[choice].format(randomdata))
    question['correct'].append(formats[choice].format(randomdata))
    for f in random.sample([x for x in range(len(formats)) if x.format(randomdata) != formats[choice].format(randomdata)],4):
        question['incorrect'].append(formats[f].format(randomdata))
    return question
         
def formatq20(qid):
    '''questions based on string.format()'''
    formats = ["{:04d}","{: 04d}","{: 4d}","{: 4d}","{:d}","{: d}","{:03d}"]
    choice = random.randint(0,len(formats)-1)
    randomdata = round(10**(random.random()*4),2)
    question = {'qtype': 'MC', 'correct': [], 'incorrect': [], 'prompt': '',
      'description':'formatq 20 {}'.format(qid)}
    question['prompt'] = "Which of the following outputs should result from the command <tt>'!{code}!'.format({val})</tt>?".format(val=randomdata, output=formats[choice].format(randomdata))
    question['correct'].append('An error occurs')
    for f in random.sample([x for x in range(len(formats))],4):
        question['incorrect'].append(formats[f].format(int(randomdata)))
    return question

def formatq21(qid):
    '''questions based on string.format()'''
    formats = ["{:04f}","{: 04f}","{:. 4f}","{: .4f}","{:02.4f}","{: 2.3f}","{:03.3f}"]
    choice = random.randint(0,len(formats)-1)
    randomdata = 10**(random.random()*4)
    question = {'qtype': 'MC', 'correct': [], 'incorrect': [], 'prompt': '',
      'description':'formatq 19 {}'.format(qid)}
    question['prompt'] = "Which of the following outputs should result from the command <tt>'!{code}!'.format({val})</tt>?".format(val=randomdata, output=formats[choice].format(randomdata))
    question['correct'].append(formats[choice].format(randomdata))
    for f in random.sample([x for x in range(len(formats)) if x.format(randomdata) != formats[choice].format(randomdata)],4):
        question['incorrect'].append(formats[f].format(randomdata))
    return question

def formatq22(qid):
    '''questions based on string.format()'''
    formats = ["{:04f}","{: 04f}","{:. 4f}","{: .4f}","{:02.4f}","{: 2.3f}","{:03.3f}"]
    choice = random.randint(0,len(formats)-1)
    randomdata = 10**(random.random()*4)
    question = {'qtype': 'MC', 'correct': [], 'incorrect': [], 'prompt': '',
      'description':'formatq 18 {}'.format(qid)}
    question['prompt'] = "Which of the following options should replace 'string' in <tt>'!string!'.format({val})</tt> to give the output <tt>!{output}!</tt>?".format(val=randomdata, output=formats[choice].format(randomdata))
    question['correct'].append(formats[choice])
    for f in random.sample([x for x in range(len(formats)) if x != choice],4):
        question['incorrect'].append(formats[f])
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

def qtoQML(q, qid,qname):
    newqdoc = xmldom.getDOMImplementation().createDocument(None,'QUESTION',None)
    newq = newqdoc.documentElement
    newq.setAttribute('ID', "{:016d}".format(qid))
    newq.setAttribute('DESCRIPTION', q.get('description', 'question'))
    newq.setAttribute('TOPIC', "CLS BS21010\{}".format(qname)) 
    newq.setAttribute('STATUS', "Normal")
    content = newqdoc.createElement('CONTENT')
    content.setAttribute('TYPE', 'text/html')
    newq.appendChild(content)
    content.appendChild(newqdoc.createCDATASection(q['prompt']))
    answers= newqdoc.createElement('ANSWER')
    answers.setAttribute('QTYPE', q['qtype'])
    answers.setAttribute('SHUFFLE', 'YES')
    answers.setAttribute('SUBTYPE', 'VERT')
    newq.appendChild(answers)
    acount = 0
    for c in q['correct']:
        opt = newqdoc.createElement('CHOICE')
        opt.setAttribute('ID','{}'.format(acount))
        cont = newqdoc.createElement('CONTENT')
        opt.appendChild(cont)
        cont.setAttribute('TYPE', 'text/html')
        text = newqdoc.createCDATASection(str(c))
        cont.appendChild(text)
        answers.appendChild(opt)
        outcome = newqdoc.createElement('OUTCOME')
        outcome.setAttribute('ID','{}'.format(acount))
        outcome.setAttribute('SCORE', "1")
        condition = newqdoc.createElement('CONDITION')
        ctext=newqdoc.createTextNode('{}'.format(acount))
        condition.appendChild(ctext)
        outcome.appendChild(condition)
        ccont = newqdoc.createElement('CONTENT')
        cctext = newqdoc.createCDATASection('Correct')
        ccont.appendChild(cctext)
        ccont.setAttribute('TYPE', 'text/html')
        outcome.appendChild(ccont)
        newq.appendChild(outcome)
        acount += 1
    for c in q['incorrect']:
        opt = newqdoc.createElement('CHOICE')
        opt.setAttribute('ID','{}'.format(acount))
        cont = newqdoc.createElement('CONTENT')
        opt.appendChild(cont)
        cont.setAttribute('TYPE', 'text/html')
        text = newqdoc.createCDATASection(str(c))
        cont.appendChild(text)
        answers.appendChild(opt)
        outcome = newqdoc.createElement('OUTCOME')
        outcome.setAttribute('ID','{}'.format(acount))
        outcome.setAttribute('SCORE', "0")
        condition = newqdoc.createElement('CONDITION')
        ctext=newqdoc.createTextNode('{}'.format(acount))
        condition.appendChild(ctext)
        outcome.appendChild(condition)
        ccont = newqdoc.createElement('CONTENT')
        cctext = newqdoc.createCDATASection('Wrong')
        ccont.appendChild(cctext)
        ccont.setAttribute('TYPE', 'text/html')
        outcome.appendChild(ccont)
        newq.appendChild(outcome)
        acount += 1
    return newq

def getq(methodlist, count):
    for f in methodlist:
        text = ''
        fh=open(f.__name__+".qml", 'w')
        print(QML_HEADER, file=fh)
        for p in range(40):
            text +=qtoQML(f(p),99999999+ p*40+p,f.__name__).toxml()
        print(text.replace("<CONDITION>", '<CONDITION>"').replace("</CONDITION>", '"</CONDITION>'), file=fh)  
        print('</QML>', file=fh)
        fh.close()