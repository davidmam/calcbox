# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 08:39:54 2016

@author: www
"""
import random, re

# define molecular weights of common chemicals
rmm={
'NaCl':58.44,
'KCl': 74.5513,
'Na2CO3': 105.9888,
'NaHCO3': 84.007,
'Na3PO4': 163.94,
'Na2HPO4': 141.96,
'NaH2PO4': 119.98,
'K3PO4': 212.27,
'K2HPO4': 174.18,
'KH2PO4': 136.09,
'CH3COONa': 82.03,
'CaCO3': 100.09

}
H2O=18.015

buffers=(('NaH2PO4','Na2HPO4',7.21 ), 
         ('KH2PO4', 'K2HPO4', 7.21),
        ('NaHCO3', 'Na2CO3', 9.9),
        ('CH3COOH', 'CH3COONa', 4.74)
)

hydrates = {'Na2HPO4': [0,2,7,12],
            'K2HPO4': [0,3],
            'CH3COONa':[0,3]
}
  
def latexformat(text):
    return re.sub(r'([A-Za-z])(\d+)',r'\1\\textsubscript{\2}', text)

guides={'q1':
    ''' The relationship between the concentration (in moles/litre expressed 
    as $\\textrm{mol}L^{-1}$), volume ( in litres, $L$), mass (in grams, $g$) and 
    relative molecular mass (RMM, also referred to as \\emph{gram formula mass} 
    or \\emph{molar mass}) is given by the formula below
    
    $$ \\textrm{concentration} = \\frac{\\textrm{mass}}{\\textrm{RMM}\\times \\text{volume}} $$
    
    This can be rearranged for mass to give
    
    $$ \\textrm{mass} =  \\textrm{concentration} \\times \\textrm{volume} \\times \\textrm{RMM} $$
    
    ''',
    'q2': ''' The relationship between the concentration (in moles/litre expressed 
    as $\\textrm{mol}L^{-1}$), volume ( in litres, $L$), mass (in grams, $g$) and 
    relative molecular mass (RMM, also referred to as \\emph{gram formula mass} 
    or \\emph{molar mass}) is given by the formula below
    
    $$ \\textrm{concentration} = \\frac{\\textrm{mass}}{\\textrm{RMM}\\times \\text{volume}} $$
    
    This can be rearranged for mass to give
    
    $$ \\textrm{mass} =  \\textrm{concentration} \\times \\textrm{volume} \\times \\textrm{RMM} $$
    
    ''',}

def q1():
    '''Prepare a solution of a given concentration 
    and volume with the given compound(s)'''
    #how many compounds shall we make?
    number=random.randint(1,3)
    #choose compounds
    compounds = random.sample(rmm.keys(),number)
    #set random concentrations
    concentrations=[random.randint(1,10)*(10**random.randint(0,2)) for x in compounds]      
    #set a volume
    volume=random.randint(1,20)*5*(10**random.randint(1,2))
    
    qtext='''Calculate the mass of each compound which must be used to make a %s ml 
    solution with the following composition:
    
    %s'''
    rmms=[rmm[x] for x in compounds]
    data=zip(compounds,concentrations, rmms)
    stuff=[]    
    for d in data:
        conc=d[1]
        units='mM'
        if d[1] >=100:
            conc/=1000
            units='M'
        stuff.append('%s %s %s (RMM: %s Da)'%(conc,units,latexformat(d[0]),d[2]))
    return qtext%(volume,'\\\\\n'.join(stuff))
    
def q2():
    '''What concentration is obtained by dissolving the following compounds in this volume'''
    #how many compounds shall we make?
    number=random.randint(1,3)
    #choose compounds
    compounds = random.sample(rmm.keys(),number)
    #set random concentrations
    concentrations=[random.randint(1,10)*(10**random.randint(0,2)) for x in compounds]      
    #set a volume
    volume=random.randint(1,20)*5*(10**random.randint(1,2))
    
    qtext='''Calculate the concentration of each compound in a 
    solution of volume %s ml with the following composition:
    
    %s'''
    rmms=[rmm[x] for x in compounds]
    
    data=zip(compounds,concentrations, rmms)
    stuff=[]    
    for d in data:
        component= list(d)[:]
        component.append(volume*d[1]*d[2]/1000000)
        stuff.append('%s g %s (RMM: %s Da)'%(component[3],latexformat(component[0]),component[2]))
    return qtext%(volume,'\\\\\n'.join(stuff))
           
    
    