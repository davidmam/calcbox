# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 08:35:13 2019

@author: David
"""

import random

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
    
def get_random_array(lenfrom=5, lento=10):   
    arr = []
    for p in range(random.randint(lenfrom, lento)):
        arr.append(random.random()*random.randint(1,10))
    arr = [round(x, 2) for x in set(arr)]
    return arr
        