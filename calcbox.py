# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 08:39:54 2016

@author: www
"""
import random, re
import qrcode

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
  
uvvisM={'p-Nitrophenol':18200,
       }  

uvvisW = {'DNA': [50,260],
          'Protein': [1, 280] }

def writeqr(text, fileid, savedir='qrcodes'):
    qr=QRCode()
    qr.add_data(text)
    img=qr.make_image()
    img.save('/'.join(['.',savedir,fileid+'.png']))
  
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
    
    ''',
    'q3': ''' The relationship between the concentration (in moles/litre expressed 
    as $\\textrm{mol}L^{-1}$), volume ( in litres, $L$), mass (in grams, $g$) and 
    relative molecular mass (RMM, also referred to as \\emph{gram formula mass} 
    or \\emph{molar mass}) is given by the formula below
    
    $$ \\textrm{concentration} = \\frac{\\textrm{mass}}{\\textrm{RMM}\\times \\text{volume}} $$
    
    This can be rearranged for mass to give
    
    $$ \\textrm{mass} =  \\textrm{concentration} \\times \\textrm{volume} \\times \\textrm{RMM} $$

    When performing an acid/base titration, the point of change is when the charges in the base 
    equal the charges in the acid, ie they are at the same normality. Assume the unknown acid is 
    univalent unless indicated otherwise to give the relative molecular mass with 
    respect to charge.    
    
    ''',
    'q4': '''
    The equation for dilutions is the molar equivalence
    
    $$ C_1V_1 = C_2V_2 $$
    
    When a fixed volume of a solution is diluted, the total number of moles $C_1V_1$ 
    remains the same. This can be rearranged for the unknown concentration or volume as follows:
    
    $$ C_1 = \\frac{C_2V_2}{V_1} $$
    or
    $$ V_1 = \\frac{C_2V_2}{C_1} $$
    ''',
    'q5': '''
    The equation for dilutions is the molar equivalence
    
    $$ C_1V_1 = C_2V_2 $$
    
    When a fixed volume of a solution is diluted, the total number of moles $C_1V_1$ 
    remains the same. This can be rearranged for the unknown concentration or volume as follows:
    
    $$ C_1 = \\frac{C_2V_2}{V_1} $$
    or
    $$ V_1 = \\frac{C_2V_2}{C_1} $$
    ''',
    'q6': '''
    The relationship between the absorbance and concentration is given by the Beer-Lambert law.
    
    $$ A = \\epsilon.c.l $$
    
    where $A$ is the concentration coefficient, $\\epsilon$ is the extinction coefficient, 
    $c$ is the concentration and $l$ is the path length. This can be readily 
    rearranged for $c$ or $\\epsilon$''',
    'q7': '''
    The relationship between the absorbance and concentration is given by the Beer-Lambert law.
    
    $$ A = \\epsilon.c.l $$
    
    where $A$ is the concentration coefficient, $\\epsilon$ is the extinction coefficient, 
    $c$ is the concentration and $l$ is the path length. This can be readily 
    rearranged for $c$ or $\\epsilon$''',
    }

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
    qcat='A1 Concentrations'
    qtext='''Calculate the mass of each compound which must be used to make a %s ml 
    solution with the following composition:
    
    %s'''
    rmms=[rmm[x] for x in compounds]
    data=zip(compounds,concentrations, rmms)
    stuff=[]    
    answers=[]
    for d in data:
        conc=d[1]
        units='mM'
        if d[1] >=100:
            conc/=1000
            units='M'
        stuff.append('%s %s %s (RMM: %s Da)'%(conc,units,latexformat(d[0]),d[2]))
        answers.append('%s: %s'%(d[0],d[1]*d[2]*volume/1000000 ))
        
    return {'title':qcat,'question':qtext%(volume,'\\\\\n'.join(stuff)),'answers': '; '.join(answers)}
    
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
    qcat='A1 Concentrations'
    
    qtext='''Calculate the concentration of each compound in a 
    solution of volume %s ml with the following composition:
    
    %s'''
    rmms=[rmm[x] for x in compounds]
    answers=[]
    
    data=zip(compounds,concentrations, rmms)
    stuff=[]    
    for d in data:
        component= list(d)[:]
        component.append(volume*d[1]*d[2]/1000000)
        stuff.append('%s g %s (RMM: %s Da)'%(component[3],latexformat(component[0]),component[2]))
        answers.append('%s: %s'%(d[0], d[1]))

    return {'title':qcat,'question':qtext%(volume,'\\\\\n'.join(stuff)),'answers': '; '.join(answers)}  
           
def q3():
    '''calculate the empirical molecular weightfor an unknown compound.'''
    molwt=float(random.randint(1500,3500))/10
    volume=random.randint(1,20)*5*(10**random.randint(1,2))
    concentration=random.randint(1,10)*(10**random.randint(0,2))
    mass=volume*concentration*molwt/100000
    titvol=concentration*10/100
    qcat='B6 Complex Concentrations'
    qtext= '''%s g of an unknown acid is dissolved in %s ml water. 10 ml of 
    the solution is titrated against a 0.1 M solution of a strong univalent base. %s ml is required for 
    neutralisation. What is the empirical molecular weight of the unknown 
    acid?'''%(mass, volume,titvol)      
    answer='%s Da'%molwt
    return {'title':qcat, 'question':qtext, 'answers':answer}
    
def q4():
    '''Application of the dilution law'''
    concentration1=random.randint(1,10)*(10**random.randint(1,2))
    concentration2=random.randint(1,9)*(10**(random.randint(0,1,2)-2))
    volume2=random.randint(1,20)*5*(10**random.randint(1,2))
    volume1=concentration2*volume2/concentration1
    qcat='A2 Dilutions'
    qtext='''%s ml of a solution with concentration %s mM is diluted to a total 
    volume of %s ml. What is the concentration of the resulting solution?'''%(volume1,concentration1, volume2)
    answer=concentration2
    return {'title': qcat, 'question':qtext,'answers':answer}

def q5():
    '''Application of the dilution law'''
    concentration1=random.randint(1,10)*(10**random.randint(1,2))
    concentration2=random.randint(1,9)*(10**(random.randint(0,2)-2))
    volume2=random.randint(1,20)*5*(10**random.randint(1,2))
    volume1=concentration2*volume2/concentration1
    qcat='A2 Dilutions'
    qtext='''What volume of a solution with concentration %s mM is required to 
    make %s ml of a solution with a final concentration of %s mM?'''%(concentration1, volume2, concentration2)
    answer=volume1
    return {'title': qcat, 'question':qtext,'answers':answer}
    
def q6():
    '''Beer-Lambert Law - Basic by molarity '''
    absorb= float(random.randint(1,1000))/1000
    compound=random.sample(uvvisM.keys(),1)[0]
    unitText=['M','mM','uM', 'nM','pM']
    units=0    
    conc=absorb/uvvisM[compound]
    while conc< 0.1:
        conc=conc*1000
        units+=1
    qcat='A3 Absorbance'
    qtext='''A sample of %s with extinction coefficient %s $ML^{-1}cm_{-1}$ gives 
    an absorbance reading of %s when read in a cuvette with path length 1cm.
What is the concentration of the test solution?'''%(compound, uvvisM[compound], absorb)    
    answer='%s %s'%(conc, units)
    return {'title':qcat, 'question':qtext, 'answers':answer}

def q7():
    '''Beer-Lambert Law - Basic by molarity '''
    absorb= float(random.randint(1,1000))/1000
    compound=random.sample(uvvisM.keys(),1)[0]
    unitText=['M','mM','uM', 'nM','pM']
    units=0    
    conc=absorb/uvvisM[compound]
    while conc< 0.1:
        conc=conc*1000
        units+=1
    qcat='A3 Absorbance'
    qtext='''What absorbance reading would a sample of %s with extinction coefficient %s $ML^{-1}cm_{-1}$ 
    and concentration %s %s when read in a UV-vis spectrometer.'''%(compound, uvvisM[compound], conc, units)    
    answer='%s'%absorb
    return {'title':qcat, 'question':qtext, 'answers':answer}
    
    
    
    
    
    
    
    