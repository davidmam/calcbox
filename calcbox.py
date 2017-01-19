# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 08:39:54 2016

@author: www
"""
import random, re
import qrcode,os, os.path
import errno
import math
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
'CH3COOH': 60.05,
'CaCO3': 100.09

}
AVOGADRO=6.022*10**23
H2O=18.015

buffers=(('NaH2PO4','Na2HPO4',7.21 ), 
         ('KH2PO4', 'K2HPO4', 7.21),
        ('NaHCO3', 'Na2CO3', 9.9),
        ('CH3COOH', 'CH3COONa', 4.74),
)

hydrates = {'Na2HPO4': [0,2,7,12],
            'K2HPO4': [0,3],
            'CH3COONa':[0,3]
}
  
uvvisM={'p-Nitrophenol':18200,
        'Oxyhaemoglobin':551620,
        'Haemoglobin':524280,
        'Cytochrome C (\\emph{Pseudomonas aureginosa})':31180,
        'Cytochrome C (\\emph{D. Gigas})': 124400,
        'Cytochrome C (\\emph{E.equus})': 29000,
        '2-nitro-5-thiobenzoic acid (DTNB)':13600, # Ellmans reagent
       }  

uvvisW = {'DNA': [50,260],
          'Protein': [1, 280] }
          
concunits=['M','mM','uM','nM','pM','fM']
unitlist=['f','p','n','u','m','','k','M']

def latexgraph(xbox=5,ybox=5,xlog=False,ylog=True, height=180, width=180):
    '''draw a block of graph paper'''
    loggaps=[6.02, 9.54, 12.04, 13.98, 15.56, 16.90, 18.06, 19.08]
    unitlength=int(min(height/ybox,width/xbox))/200
    graphtext='''
    \\setlength{\\unitlength}{%scm}
    \\begin{picture}(%s,%s)
    \\linethickness{0.5pt}
    '''%(unitlength,xbox*20, ybox*20)
    graphtext+="\\color{Gray}\n"
    if xlog:
        for k in loggaps:
            graphtext+="\\multiput(%s,0)(20,0){%s}{\\line(0,1){%s}}\n"%(k,xbox,ybox*20)
    else:
         graphtext+="\\color{Gray}\n\\multiput(2,0)(2,0){%s}{\\line(0,1){%s}}\n\\color{Gray}\n"%(xbox*10,ybox*20)     
         graphtext+="\\color{blue}\n\\multiput(10,0)(20,0){%s}{\\line(0,1){%s}}\n\\color{Gray}\n"%(xbox, ybox*20,)

    if ylog:
        for k in loggaps:
            graphtext+="\\multiput(0,%s)(0,20){%s}{\\line(1,0){%s}}\n"%(k,ybox,xbox*20)
    else:
         graphtext+="\\color{Gray}\n\\multiput(0,2)(0,2){%s}{\\line(1,0){%s}}\n\\color{Gray}\n"%(ybox*10,xbox*20)     
         graphtext+="\\color{blue}\n\\multiput(0,10)(0,20){%s}{\\line(1,0){%s}}\n\\color{Gray}\n"%(ybox,xbox*20)

    graphtext+='''\\color{blue}
    \\linethickness{1pt}
    \\multiput(0,0)(0,20){%s}{\\line(1,0){%s}}
    \\multiput(0,0)(20,0){%s}{\\line(0,1){%s}}
    \\end{picture}
    '''%(ybox+1,xbox*20,xbox+1, ybox*20)
    return graphtext
    
def writeqr(text, fileid, savedir='qrcodes'):
    qr=qrcode.QRCode()
    qr.add_data(text)
    img=qr.make_image()
    img.save('/'.join(['.',savedir,fileid+'.png']))
  
def latexformat(text):
    return re.sub(r'([A-Za-z])(\d+)',r'\1\\textsubscript{\2}', text)
qpp={'A1':2,
     'A2':2,
     'A3':2,
     'A4':4,
     'A5':4,
     'A6':4,
     'A7':4,
     'A8':2,
     'B1':2,
     'B2':3,
     }
guides={'A1':
    ''' \\section*{A1 Concentrations}
    The relationship between the concentration (in moles/litre expressed 
    as $\\textrm{mol}L^{-1}$), volume ( in litres, $L$), mass (in grams, $g$) and 
    relative molecular mass (RMM, also referred to as \\emph{gram formula mass} 
    or \\emph{molar mass}) is given by the formula below
    
    $$ \\textrm{concentration} = \\frac{\\textrm{mass}}{\\textrm{RMM}\\times \\textrm{volume}} $$
    
    This can be rearranged for mass to give
    
    $$ \\textrm{mass} =  \\textrm{concentration} \\times \\textrm{volume} \\times \\textrm{RMM} $$
    
    For solutions expressed in g/L the equivalence is straightforward. Concentration is expressed as a ratio, 
    so to convert between different common units (femto, pico, nano, micro, milli etc.)
    you should multiply by 1000 when using a smaller unit, or divide by 1000 when using a larger unit. 
    The following values are all equivalent 
    
    $$ 5 \\frac{\\mu g}{mL} = 0.005 \\frac{\\mu g}{\\mu L} = 5000 \\frac{\\mu g}{L} = 5 \\frac{ng}{\\mu L} $$
    
    ''',
    'A2': '''
    \\section*{A2 Dilutions}
    The equation for dilutions is the molar equivalence
    
    $$ C_1V_1 = C_2V_2 $$
    
    When a fixed volume of a solution is diluted, the total number of moles $C_1V_1$ 
    remains the same. This can be rearranged for the unknown concentration or volume as follows:
    
    $$ C_1 = \\frac{C_2V_2}{V_1} $$
    or
    $$ V_1 = \\frac{C_2V_2}{C_1} $$
    ''',
    'A3': '''
    \\section*{A3 Absorbance}
    The relationship between the absorbance and concentration is given by the Beer-Lambert law.
    
    $$ A = \\epsilon.c.l $$
    
    where $A$ is the concentration coefficient, $\\epsilon$ is the extinction coefficient, 
    $c$ is the concentration and $l$ is the path length. This can be readily 
    rearranged for $c$ or $\\epsilon$''',
    'A4':'''    \\section*{A4 Units and Scientific notation}
    Scientific notation allows use to express easily very large or very small numbers, and to multiply or divide them.
    We do that by stating the number as a multiple of powers of ten, so we can take the mantissa (the first bit), 
    and multiply that by the power of ten given by the exponent. e.g for the number 0.000345 this would be
    
    $$ 3.45 \\times 10^{-4} $$
    
    where 3.45 is the mantissa and -4 is the exponent.
    
    As can be seen, the exponent is the number of places before (for positive) or after (for negative)
the decimal point. So 345 would be $3.45 \\times 10^{2}$.    
    
    When multiplying and dividing numbers in scientific notation we can add the 
    exponents when multiplying, or subtract the exponent for the denominator (the number on the bottom)
    from the exponent for the numerator (the number on the top). Divide the mantissas in the usual way  
    and make any corrections neccessary.

    $$ 3.45 \\times 10^{-7}\\  \\textrm{multiplied by}\\  2.80 \\times 10^{4} $$
    Add the exponents
    $$ 3.45\\  \\textrm{multiplied by}\\ 2.80 \\times 10^{-7+4}\\ ( =10^{-3}) $$
    Multiply the mantissas
    $$  3.45 \\times 10^{-7}\\  \\textrm{multiplied by}\\ 2.80 \\times 10^{4} = 9.66 \\times 10^{-3} $$

Dividing is similar, though this time we will need to make a small correction to the exponent

$$ \\frac{6.82 \\times 10^{3}}{8.43 \\times 10^{-5}} $$

Subtract the exponent of the denominator (the bottom, -5 ) from the exponent of the numerator (the top, 3)
$$ \\frac{6.82}{8.43} \\times 10^{3 - -5} \\textrm{\mbox{\parbox[c]{3in}{(subtracting a negatve number is the same as adding the positive number)}}}\\ = \\frac{6.82}{8.43} \\times 10^{8} $$
Divide the mantissas, and then add or subtract from the exponent to get 1 digit before the decimal point.

$$ 0.809 \\times 10^{8} = 8.09 \\times 10^{7} $$

\subsection*{Common Units}

It can be inconvenient to use Scientific notation all the time. Common units are multiples of 
the unit, typically in steps of 1000 ($10^{3}$). A comprehensive list is on the poster 
of nearly everything, but common ones are milli ($10^{-3}$), micro ($10^{-6}$), 
nano ($10^{-9}$), kilo ($10^{3}$), Mega ($10^{6}$), Giga ($10^{9}$)

e.g. 1000 mg = 1 g = 1 $\\times 10^6$ ug = 1$\\times 10^{-3}$ kg

    '''  ,
    'A5':
        '''
        \\section*{A5 Moles and Molarity}
        The \\textsl{mole} is used in chemistry to describe a fixed number of molecules.
        The weight of molecules varies according to their elemental composition, 
        so comparing them by weight becomes difficult. Instead we can compare 
        fixed numbers of molecules. The counting unit for chemistry is the 
        \\textbf{mole} which corresponds to a count of 
        $6.022 \\times 10^{23}$, known as \\emph{Avogadro's number} ($N_A$). 
        Avogadro's number has the units of \\emph{reciprocal mole} ($\\textsl{mol}^{-1}$).
        
        The \\emph{relative molecular mass} (\\emph{RMM}, also known as the \\emph{gram formula mass} or \\emph{Molecular Weight})
        of a compound is the mass in grams of 1 mole of that compound, i.e. $6.022 \\times 10^{23}$ molecules.
        
        Concentrations can be expressed as moles per Litre ($\\textsl{mol}L^{-1}$). 
        The number of molecules in a particular volume can therefore be expressed as:
        
        $$\\textrm{molecules} = \\textrm{volume} \\times \\textrm{concentration} \\times N_A $$        
        
        To calculate the number of molecules in a given mass, divide by the relative molecular mass to get 
        the number of moles, then multiply by $N_A$
        
        $$ \\textrm{molecules} = \\frac{\\textrm{mass}}{\\textsl{RMM}} \\times N_A $$
        
        To express exponents in a computer we typically use the formulation 
        6.022 $\\times$ 10e23 to refer to $6.022 \\times 10^{23}$.
               
        ''',
       'A6':
       '''\\section*{A6 Scaling and Aliquots}
       We commonly use two sorts of measures in science - relative and absolute. 
       Relative measures are proportional, they describe one quantity (e.g. weight, or
       distance) in terms of another (e.g. volume, or time.) We see this as, for example, concentrations
       (\\textsl{moles} per \\textsl{Liter}) or speed ( \\textsl{meters} per \\textsl{second}) or cell density
       (\\textsl{number of cells} per \\textsl{volume} or \\textsl{area}).
       
       Absolute measures are a fixed quantity, e.g. weight, distance, count, volume.
       
       An \\textbf{aliquot} is a portion of a \\textbf{bulk}. It will have the 
       \\emph{same relative properties} as the bulk but the \\emph{absolute properties scale}
       in proportion to the relative sizes of the aliquot and bulk.
       
       If we represent the absolute quantity as $Q$ and the quantity it is measured 
       relative to as $V$ (another absolute property), then we can state the relative property as
       $$\\frac{Q}{V}$$
       
       Taking an aliquot of volume $V_a$ from a bulk with volume $V_b$ gives us the equality
       
       $$ \\frac{Q_a}{V_a} = \\frac{Q_b}{V_b} $$
       
       so the ratio $\\frac{Q_a}{Q_b}$ is the same as the ratio $\\frac{V_a}{V_b}$
       
       Example:
       
       An aliquot of $10\\mu L$ is taken from a culture of 200ml. When spread on a plate 
       there are 133 colonies. How many colonies would we get from the full culture?
       
       Using
       $$ \\frac{V_a}{V_b} = \\frac{Q_a}{Q_b} $$
        where $Q_a$ is 133 cells, $V_a$ is $10\times 10^{-6}L$ and $V_b$ is $0.2 L$, we can 
        rearrange to find the unknown quantity $Q_b$
        $$ Q_b = \\frac{Q_a \\times V_b}{V_a} = \\frac{133\ \\textrm{colonies} \\times 0.2L}{10x10^{-6}L} = 2.66 \\times 10^6\ \\textrm{colonies} $$

\\subsection*{Describing dilutions}
There are several ways of describing a diution. Essentially these all mean the same thing.

'A $10^5$ dilution' - the sample has been diluted so that one part of the original solution is in 100000 times the volume.\\
'A 100000-fold dilution', 'A $100000\\times$ dilution' and 'a 1 in 1000000 dilution' mean exactly the same.

Note that '1 in 10 dilution' and '1:9' are the same, but '1:10 (one part to ten parts)' is an 11-fold dilution.        
       
       ''',
       'A7': '''\\section*{A7 Percentages and proportional solutions}
       For some compounds or mixtures it is impossible to determina a molecular weight and hence 
       impossible to state the concentration of a solution in $\\textsl{moles}L^{-1}$. Instead,
       for both solutions and mixtures, we     can use percentages expressed either as 
       proportions of weight (weight for weight, w/w), weight to volume (w/v), or volume as 
       volume for volume (v/v). Typical examples in the lab are expressed as percentages 
       where an $n\\%$ w/w mixture will contain $n$ gramms of the compound in a total mass of 100g,
       an $n\\%$ w/v solution will contain $n$ grams in 100ml, and a $n\\%$ v/v
       solution will contain $n$ ml of the liquid in a total volume of 100ml.
       
       Percentage solutions are easy to calculate and will follow the smae rules for dilution as
       solutions expressed as a molar concentration.
       
       $$\\textrm{concentration (w/v)} = 100 \\times \\frac{\\textrm{mass}}{\\textrm{volume}} $$
       $$\\textrm{concentration (v/v)} = 100 \\times \\frac{\\textrm{compound volume}}{\\textrm{total volume}} $$
       
       These can be readily rearranged for the added mass in a given volume/concentration and so on.
       
       ''',
       'A8':'''\\section*{A8 DNA}
DNA concentrations are typically measured in weight per volume. The concentration 
can be compared to a known standard and determined by ratios.

If DNA with a concentration of 50 $\\mu$g/ml has an absorbance of 1.000 then it is
straight forward to determine the concentration by multiplying the absorbance read
by 50 to get the concentration in $\\mu$g/ml

$$\\frac{C_{\\textrm{Unknown}}}{50 \\mu g/ml} = \\frac{A_{\\textrm{measured}}}{1.000} $$
$$  C_{\\textrm{Unknown}}  = 50 \\mu g/ml \\times   \\frac{A_{\\textrm{measured}}}{1.000} $$
       
To calculate the molecular weight of a band on a gel, first measure the migration distance of two 
standards, one either side of the . 
The log of the molecular weight is linearly negatively proportional to the distance migrated on the gel, 
at least to a close enough approximation over the usable portion of the gel.

To calculate the log(molecular weight), interpolate from the standards either side, $S_h$ 
for the standard with a molecular weight higher than the band, and $S_l$ for the one with a 
weight lower than the band.
(Or you can fit a linear model to all the data in R and mutliply the migration distance by the gradient and add the intercept. This is the log(molecular weight))

Calculate the difference in log(molecular weight) between the two standards:

$$ D_{weight} = \\log(S_h) - \\log{S_l}$$

Calculate the difference in migration distance $D$ for the standards (this will be negative)

$$ D_{mig} = D_l - D_h $$

Calculate the difference in migration distance for the band ($D_b$) and the lower standard

$$ D_{diff} = D_l - D_b $$

Now add to $\\log(S_l)$ the proportional difference between the log of the lower 
and higher molecular weights

$$ \\log(S_b) = \\log(S_l) +\\frac{D_{diff}}{D_{mig}} \\times D_{weight} $$

Raise the appropriate base (10 or $e$ depending on whether you used log to base 10 
or natural logarithms) to $\\log(S_b)$ to get your molecular weight.

$$ S_b = 10^{\\log(S_b)} $$

       ''',
       'B1':'''\\section*{B1 Buffers}
To make a buffer of the correct pH, the appropriate proportions of acid and base must be mixed. 
Each buffer has a specific affinity for  $H^+$ ions and excess base will tend to 
associate with free $H^+$, reducing the concentration in the solution and raising the pH. Excess 
acid will contribute $H^+$ to the solution, lowering the pH. The relationship between the $pH$ of a solution, 
the association constant for the buffer ($pK_a$) and the relative concentrations 
of acids \\textsl{[Acid]} and bases \\textsl{[Base]} is given by

$$ pH = pK_a + \\log\\bigg(\\frac{\\textsl{[Base]}}{\\textsl{[Acid]}}\\bigg) $$

This formula gives the pH for a specific ratio of Base to Acid for a buffer with a given pKa. 
To obtain the proportion of constituents required for a specific pH, the equation needs to be rearranged.

$$ pH - pK_a = \\log\\bigg(\\frac{\\textsl{[Base]}}{\\textsl{[Acid]}}\\bigg) $$
Take the exponent to get the ratio
$$ 10^{(pH-pK_a)}= \\frac{\\textsl{[Base]}}{\\textsl{[Acid]}} $$
and rearrange
$$ 10^{(pH-pK_a)} \\times \\textsl{[Acid]} = \\textsl{[Base]} $$

The total concentration is \\textsl{[Acid] + [Base]} so

$$ \\textsl{[Acid]} = \\textsl{[total]} \\times \\frac{1}{1+10^{(pH-pK_a)}} $$
 and for \\textsl{[Base]}
$$ \\textsl{[Base]} = \\textsl{[total]} \\times \\frac{10^{(pH-pK_a)}}{1+10^{(pH-pK_a)}} $$
       
       ''',
       'B2':'''\\section*{B2 First-order kinetics}
       First-order kinetics occurs when the reaction rate of a compound is dependent directly 
       on the concentration of that compound according to the equation:
       $$ -\\frac{d[A]}{dt} = k[A] $$
       where $k$ is the rate constant for the reaction. As the units on the left hand side 
       of the equation are $\\textsl{mol}L^{-1}s^{-1}$ it can be determined that 
       the units for the rate constant are $s^{-1}$ or \\textsl{per second}.
       
       Integrating the rate equation for time, $t$ gives the following form where $[A]_0$ 
       is the starting concentration and $[A]_t$ is the concntration after time $t$:
       
       $$ [A]_t = [A]_0\\exp^{-kt}$$
       or in it's logarithmic form
       $$ \\ln([A]_t)=\\ln([A]_0)-kt $$

    We can rearrange this for any of the desired components:
    $$ \\ln([A]_0) - \\ln([A]_t) = \\ln\\Bigg(\\frac{[A]_0}{[A]_t}\\Bigg) = kt   $$
    $$ k = \\frac{(\\ln([A]_0) - \\ln([A]_t)) }{t} $$
    $$ t =  \\frac{(\\ln([A]_0) - \\ln([A]_t)) }{k} $$   
    
    \\subsection*{Half life}
    The half life of a reaction, $t_{\\frac{1}{2}}$ is the time taken for the substrate concentration 
    to reduce to $1/2$ the starting value.
    At $t_{\\frac{1}{2}}$, $\\frac{[A]_0}{[A]_t}$ is 2, so the half life $t_{\\frac{1}{2}}$
    is:
    
    $$ t_{\\frac{1}{2}} =\\frac{\\ln(2)}{k} $$
    
    ''',
    'B3': '''\\section*{B3 Pressure and Poisselles law}
    The change in pressure of a fluid travelling along a tube can be described 
with Poisselle's law. 

    $$ Q =  \frac{\pi r^4(P_1 - P_2) }{ 8\eta L } $$
    where $Q$ is the overall flow (in $\text{cm}^3\text{s}^{-1}$), 
    $r$ is the radius of the tube, 
    $\eta$ is the viscosity of the liquid (measured in dyn $\text{cm.s}^{-1}$)
    and $L$ is the length of the tube in cm.
    
    For a given viscosity and length of tube, the pressure drop is directly
    related to the radius of the tube. For many problems that look at a change
    in radius with relation to pressure,the viscosity and length are constants that
    can be cancelled.
    
    
    
    
    
    
    '''
       
       
    }

def exponent(number):
    expon= int(math.log10(number))
    if expon < 0:
        expon-=1
    return expon
    
def mantissa (number):    
    return number/10**exponent(number)
    

def readlatexstart(template='latexstart.tex'):
    return open(template).read()
    
def formatquestion(qcat,qtext, atext, qid, height=120):
    ftext='\\noindent\\fbox{\\begin{minipage}[t][%dmm][t]{\\textwidth}\n'%height
    ftext+="\\section*{%s}\n"%qcat
    ftext+="%s\n"%qtext
    ftext+="\\vskip 4mm\n"
    writeqr(atext,qid)
    ftext+="\\includegraphics[width=25mm]{%s}\n"%qid
    ftext+="\\end{minipage}}\n\n"
    return ftext

def writequestions(qfile='questions.tex', count=1, pages=None):
    '''This is where we write the questions out to file.'''
    fh=open(qfile, 'w')
    index=0
    try:
        os.makedirs('qrcodes')
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    fh.write(readlatexstart())
    if pages==None:
        pages= {'A1':[q1,q2,q27,q28], 'A2':[q4,q5], 
        'A3':[q6,q7],'A4':[q8,q10,q9],'A5':[q11,q12,q13,q14,q15,q16,q17,q18],
        'A6': [q19,q20,q21,q22],'A7':[q23,q24,q25,q26],'B1':[q101,q102],
        'B2': [q103,q104,q105,q106],'A8': [q29, q30]}
    for i in range(count):
        print('printing set %s of %s'%(i, count))
        for page in pages.keys():
            qcount=0
            for qf in pages[page]:
                qcount+=1                
                index=index+1
                qrfn="Q%05d"%index
                qh=(240-qpp[page]*3)/qpp[page]
                #print(qh)
                #print('writing question %s'%qf)
                #print('%s'%qf())
                q=qf()
                fh.write(formatquestion(q['title'],q['question'],q['answers'],qrfn, height=qh))
                if qcount%qpp[page]==0:
                    fh.write("\\newpage\n")
                    fh.write(guides[page]+"\n\\newpage\n")
            if qcount%qpp[page]!=0:
                fh.write("\\newpage\n")
                fh.write(guides[page]+"\n\\newpage\n")
    fh.write('\\end{document}\n')
    fh.close()     

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
        aval=d[1]*d[2]*volume/1000000
        rdig=2-int(math.log10(aval))
        
        answers.append('%s: %s g'%(d[0],round(d[1]*d[2]*volume/1000000,rdig )))
        
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
        aval=d[1]*d[2]*volume/1000000
        rdig=2-int(math.log10(aval))
        component.append(round(aval,rdig))
        stuff.append('%s g %s (RMM: %s Da)'%(component[3],latexformat(component[0]),component[2]))
        answers.append('%s: %s mM'%(d[0], d[1]))

    return {'title':qcat,'question':qtext%(volume,'\\\\\n'.join(stuff)),'answers': '; '.join(answers)}  
           
def q3():
    '''calculate the empirical molecular weight for an unknown compound.'''
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
    answer='%s Da'%round(molwt,1)
    return {'title':qcat, 'question':qtext, 'answers':answer}
    
def q4():
    '''Application of the dilution law'''
    concentration1=random.randint(1,10)*(10**random.randint(1,2))
    concentration2=random.randint(1,9)*(10**(random.randint(0,2)-2))
    volume2=random.randint(1,20)*5*(10**random.randint(1,2))
    aval=concentration2*volume2/concentration1
    rdig=2-int(math.log10(aval))
    volume1=round(aval,rdig)
    units=1
    while concentration2 <1:
        concentration2 *=1000
        units +=1
    qcat='A2 Dilutions'
    qtext='''%s ml of a solution with concentration %s mM is diluted to a total 
    volume of %s ml. What is the concentration of the resulting solution?'''%(volume1,concentration1, volume2)
    answer="%s %s"%(round(concentration2,2),concunits[units])
    return {'title': qcat, 'question':qtext,'answers':answer}

def q5():
    '''Application of the dilution law'''
    concentration1=random.randint(1,10)*(10**random.randint(1,2))
    concentration2=random.randint(1,9)*(10**(random.randint(0,2)-2))
    volume2=random.randint(1,20)*5*(10**random.randint(1,2))
    aval=concentration2*volume2/concentration1
    rdig=2-int(math.log10(aval))
    volume1=round(aval,rdig)
    units=1
    while concentration2 <1:
        concentration2 *=1000
        units +=1
    qcat='A2 Dilutions'
    qtext='''What volume of a solution with concentration %s mM is required to 
    make %s ml of a solution with a final concentration of %s %s?'''%(concentration1, volume2, round(concentration2,2),concunits[units])
    answer="%s ml"%volume1
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
    answer='%s %s'%(round(conc,2), concunits[units])
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
    and concentration %s %s give when read in a UV-vis spectrometer.'''%(compound, uvvisM[compound], round(conc,2), concunits[units])    
    answer='%s'%absorb
    return {'title':qcat, 'question':qtext, 'answers':answer}
 



   
def q8():
    '''convert and represent units'''
    unitlist=['f','p','n','u','m','','k','M']
    unitoffset=5
    exponent=random.randint(1,13)-12
    mantissa=random.random()
    while mantissa <1:
        mantissa *=10
    mantissa=round(mantissa,2)
    startvalue=mantissa *10**exponent
    avalue=startvalue    
    while avalue >1000:
        avalue /= 1000
        unitoffset +=1
    while avalue < 1:
        avalue *=1000
        unitoffset -=1    
    unit=random.sample(['g','L','m','s','M'],1)[0]
    
    qcat='A4 Units and scientific notation'
    qtext= 'Express $%.02f \\times 10^{%d}$ %s in common units (milli, micro, kilo etc.)'%(mantissa,exponent,unit)
    qanswer='%.2f %s%s'%(avalue,unitlist[unitoffset],unit)
    if avalue > 100:
        qanswer += ' or %.3f %s%s'%(avalue/1000,unitlist[unitoffset+1],unit)
    return {'title':qcat, 'question':qtext,'answers':qanswer}
    
def q8a():
    '''convert and represent units'''
    unitlist=['f','p','n','u','m','','k','M']
    unitoffset=5
    start_e=random.randint(1,13)-7
    start_m=random.random()
    while start_m <1:
        start_m *=10
    start_m=round(start_m,3)
    startvalue=start_m *10**start_e
    avalue=startvalue    
    while avalue >1000:
        avalue /= 1000
        unitoffset +=1
    while avalue < 1:
        avalue *=1000
        unitoffset -=1    
    unit=random.sample(['g','L','m','s','M','Pa'],1)[0]
    startunit=0
    while startunit==0 or startunit+unitoffset >=len(unitlist) or startunit+unitoffset <0:
        #print(startunit)
        startunit=random.randint(-3,3)
    new_e=exponent(avalue)-3*startunit
    qcat='A4 Units and scientific notation'
    qtext= 'Express $%.03f \\times 10^{%d}$ %s%s in common units (milli, micro, kilo etc.)'%(start_m,new_e,unitlist[startunit+unitoffset],unit)
    try:
        qanswer='%.2f %s%s'%(avalue,unitlist[unitoffset],unit)
    except:
        print(unitoffset)
        raise
    if avalue > 100:
        qanswer += ' or %.3f %s%s'%(avalue/1000,unitlist[unitoffset+1],unit)
    return {'title':qcat, 'question':qtext,'answers':qanswer}
    
    
    
    
def q9():
    '''convert and represent units'''
    unitlist=['f','p','n','u','m','','k','M']
    unitoffset=5
    exponent=random.randint(1,13)-7
    mantissa=random.random()
    while mantissa <1:
        mantissa *=10
    mantissa=round(mantissa,2)
    startvalue=mantissa *10**exponent
    qvalue=startvalue    
    while qvalue >1000:
        qvalue /= 1000
        unitoffset +=1
    while qvalue < 1:
        qvalue *=1000
        unitoffset -=1    
    unit=random.sample(['g','L','m','s','M'],1)[0]
    multexponent=random.randint(-9,9)
    while exponent+multexponent > 6 or exponent+multexponent <-12:    
        multexponent=random.randint(-9,9)
    multmantissa=random.random()
    while multmantissa <1:
        multmantissa *=10
    multmantissa=round(multmantissa,2)
    mvalue=multmantissa*10**multexponent
    avalue=startvalue*mvalue
    munitoffset=5
    while avalue >1000:
        avalue /= 1000
        munitoffset +=1
    while avalue < 1:
        avalue *=1000
        munitoffset -=1  
    qcat='A4 Units and scientific notation'
    qtext= 'Calculate $%.02f\\times 10^{%d}$ times %.02f  %s%s  and give the answer in common units (milli, micro, kilo etc.)'%(multmantissa, multexponent,qvalue,unitlist[unitoffset],unit)
    qanswer='%.2f %s%s'%(avalue,unitlist[munitoffset],unit)
    
    if avalue > 100:
        qanswer += ' or %.3f %s%s'%(avalue/1000,unitlist[munitoffset+1],unit)
    return {'title':qcat, 'question':qtext,'answers':qanswer}
    
def q10():
    '''convert and represent units''' # TODO #
    unitoffset=5
    exponent=random.randint(1,13)-12
    mantissa=random.random()
    while mantissa <1:
        mantissa *=10
    mantissa=round(mantissa,2)
    startvalue=mantissa *10**exponent
    qvalue=startvalue    
    while qvalue >1000:
        qvalue /= 1000
        unitoffset +=1
    while qvalue < 1:
        qvalue *=1000
        unitoffset -=1    
    unit=random.sample(['g','L','m','s','M'],1)[0]
    multexponent=random.randint(-9,9)
    while exponent-multexponent > 6 or exponent-multexponent <-12:    
        multexponent=random.randint(-9,9)
    multmantissa=random.random()
    while multmantissa <1:
        multmantissa *=10
    multmantissa=round(multmantissa,2)
    mvalue=multmantissa*10**multexponent
    avalue=startvalue/mvalue
    munitoffset=5
    while avalue >1000:
        avalue /= 1000
        munitoffset +=1
    while avalue < 1:
        avalue *=1000
        munitoffset -=1  
    qcat='A4 Units and scientific notation'
    qtext= 'Calculate  %.02f  %s%s divided by $%.02f \\times 10^{%d}$   and give the answer in common units (milli, micro, kilo etc.)'%(qvalue,unitlist[unitoffset],unit,multmantissa, multexponent)
    qanswer='%s %s%s'%(round(avalue,2-int(math.log10(avalue))),unitlist[munitoffset],unit)
    if avalue > 100:
        qanswer += ' or %.3f %s%s'%(avalue/1000,unitlist[munitoffset+1],unit)
    return {'title':qcat, 'question':qtext,'answers':qanswer}
     
def q11():
    '''moles and molarity'''
    conc_unit=random.randint(2,len(concunits)-1)
    conc_e=-3*conc_unit
    conc_m=random.randint(1,999)/(10**random.randint(0,2))
    vol_unit=random.randint(1,5)
    vol_e=(5-vol_unit)*-3
    vol_m=random.randint(1,999)/(10**random.randint(0,2))
    mol=vol_m*conc_m*10**(conc_e+vol_e)
    molecule=random.sample(rmm.keys(),1)[0]
    qtext='How many molecules of %s are present in %s %sL of a solution with concentration %s %s? Give your answer in scientific notation'%(
    molecule,vol_m,unitlist[vol_unit],conc_m, concunits[conc_unit] )
    qanswer='%s x 10e%s molecules'%(round(mantissa(mol*AVOGADRO),3),exponent(mol*AVOGADRO))
    qcat='A5 Moles and Molarity'
    return {'title':qcat, 'question':qtext,'answers':qanswer}
     
def q12():
    '''moles and molarity'''
    conc_unit=random.randint(2,len(concunits)-1)
    conc_e=-3*conc_unit
    conc_m=random.randint(1,999)/(10**random.randint(0,2))
    vol_unit=random.randint(1,5)
    vol_e=(5-vol_unit)*-3
    vol_m=random.randint(1,999)/(10**random.randint(0,2))
    mol_num=AVOGADRO*vol_m*conc_m*10**(conc_e+vol_e)
    molecule=random.sample(rmm.keys(),1)[0]
    qtext='if $%s \\times 10^{%s}$ molecules of %s are present in %s %sL of a solution, what is the concentration? Give your answer in common units'%(
    round(mantissa(mol_num),3),exponent(mol_num), molecule, vol_m,unitlist[vol_unit] )
    qanswer='%s %s'%(conc_m,concunits[conc_unit])
    qcat='A5 Moles and Molarity'
    return {'title':qcat, 'question':qtext,'answers':qanswer}
     
def q13():
    '''moles and molarity'''
    mass_unit=random.randint(1,5)
    mass_e=(5-mass_unit)*-3
    mass_m=random.randint(1,999)/(10**random.randint(0,2))
    molecule=random.sample(rmm.keys(),1)[0]
    mol_num=AVOGADRO*(mass_m/rmm[molecule])*10**mass_e
        
    qtext='How many molecules of %s (RMM: %s) are present in a sample of mass %s %sg? Give your answer in scientific notation'%(
    molecule, rmm[molecule], mass_m,unitlist[mass_unit] )
    qanswer='%s x 10e%s molecules'%(round(mantissa(mol_num),3),exponent(mol_num))
    qcat='A5 Moles and Molarity'
    return {'title':qcat, 'question':qtext,'answers':qanswer}

def q14():
    '''moles and molarity'''
    mass_unit=random.randint(1,5)
    mass_e=(5-mass_unit)*-3
    mass_m=random.randint(1,999)/(10**random.randint(0,2))
    molecule=random.sample(rmm.keys(),1)[0]
    mol_num=AVOGADRO*(mass_m/rmm[molecule])*10**mass_e        
    qtext='what is the mass of $%s \\times 10^{%s}$ molecules of %s (RMM: %s)? Give your answer in common units'%(
    round(mantissa(mol_num),3),exponent(mol_num), molecule, rmm[molecule] )
    qanswer='%s %sg'%(mass_m,unitlist[mass_unit])
    qcat='A5 Moles and Molarity'
    return {'title':qcat, 'question':qtext,'answers':qanswer}
     
def q15():
    '''moles and molarity'''
    conc_unit=random.randint(2,len(concunits)-1)
    conc_e=-3*conc_unit
    conc_m=random.randint(1,999)/(10**random.randint(0,2))
    vol_unit=random.randint(1,5)
    vol_e=(5-vol_unit)*-3
    vol_m=random.randint(1,999)/(10**random.randint(0,2))
    mol=vol_m*conc_m*10**(conc_e+vol_e)
    molecule=random.sample(rmm.keys(),1)[0]
    qtext='How many moles of %s are present in %s %sL of a solution with concentration %s %s? Give your answer in scientific notation'%(
    molecule,vol_m,unitlist[vol_unit],conc_m, concunits[conc_unit] )
    qanswer='%s x 10e%s moles'%(round(mantissa(mol),3),exponent(mol))
    qcat='A5 Moles and Molarity'
    return {'title':qcat, 'question':qtext,'answers':qanswer}
     
def q16():
    '''moles and molarity'''
    conc_unit=random.randint(2,len(concunits)-1)
    conc_e=-3*conc_unit
    conc_m=random.randint(1,999)/(10**random.randint(0,2))
    vol_unit=random.randint(1,5)
    vol_e=(5-vol_unit)*-3
    vol_m=random.randint(1,999)/(10**random.randint(0,2))
    mol_num=vol_m*conc_m*10**(conc_e+vol_e)
    molecule=random.sample(rmm.keys(),1)[0]
    qtext='if $%s \\times 10^{%s}$ moles of %s are present in %s %sL of a solution, what is the concentration? Give your answer in common units'%(
    round(mantissa(mol_num),3),exponent(mol_num), molecule, vol_m,unitlist[vol_unit] )
    qanswer='%s %s'%(conc_m,concunits[conc_unit])
    qcat='A5 Moles and Molarity'
    return {'title':qcat, 'question':qtext,'answers':qanswer}
     
def q17():
    '''moles and molarity'''
    mass_unit=random.randint(1,5)
    mass_e=(5-mass_unit)*-3
    mass_m=random.randint(1,999)/(10**random.randint(0,2))
    molecule=random.sample(rmm.keys(),1)[0]
    mol_num=(mass_m/rmm[molecule])*10**mass_e
        
    qtext='How many moles of %s (RMM: %s) are present in a sample of mass %s %sg? Give your answer in scientific notation'%(
    molecule, rmm[molecule], mass_m,unitlist[mass_unit] )
    qanswer='%s x 10e%s moles'%(round(mantissa(mol_num),3),exponent(mol_num))
    qcat='A5 Moles and Molarity'
    return {'title':qcat, 'question':qtext,'answers':qanswer}

def q18():
    '''moles and molarity'''
    mass_unit=random.randint(1,5)
    mass_e=(5-mass_unit)*-3
    mass_m=random.randint(1,999)/(10**random.randint(0,2))
    molecule=random.sample(rmm.keys(),1)[0]
    mol_num=(mass_m/rmm[molecule])*10**mass_e        
    qtext='what is the mass of $%s \\times 10^{%s}$ moles of %s (RMM: %s)? Give your answer in common units'%(
    round(mantissa(mol_num),3),exponent(mol_num), molecule, rmm[molecule] )
    qanswer='%s %sg'%(mass_m,unitlist[mass_unit])
    qcat='A5 Moles and Molarity'
    return {'title':qcat, 'question':qtext,'answers':qanswer}

def q19():
    '''scaling and aliquots'''
    vol_b=random.randint(1,20)*50 # mL
    vol_a=random.randint(1,20)*10 # uL
    count_a = random.randint(30,300)
    count_b = vol_b * count_a * 1000 /vol_a
    qtext='If an aliquot of $%s\\mu L$ taken from a culture of total volume $%s mL$ contains %s cells, how many cells are present in the whole culture?'%(
    vol_a, vol_b, count_a)
    qanswer='%s x 10e%s cells'%(round(mantissa(count_b),3), exponent(count_b))
    qcat='A6 Scaling and Aliquots'
    return {'title':qcat, 'question':qtext,'answers':qanswer}
    
def q20():
    '''scaling and aliquots'''
    vol_b=random.randint(1,20)*50 # mL
    vol_a=random.randint(1,20)*10 # uL
    count_a = random.randint(30,300)
    count_b = vol_b * count_a * 1000 /vol_a
    qtext='If an aliquot of $%s\\mu L$ contains %s cells, what volume would contain $%s \\times 10^{%s}$ cells'%(
    vol_a, count_a, round(mantissa(count_b),3), exponent(count_b))
    qanswer='%s mL'%(vol_b)
    qcat='A6 Scaling and Aliquots'
    return {'title':qcat, 'question':qtext,'answers':qanswer}

def q21():
    '''scaling and aliquots'''
    mass_b=random.randint(1,20)*50 # mL
    mass_a=random.randint(1,20)*10 # uL
    count_a = random.randint(30,300) 
    count_b = mass_b * count_a * 1000 /mass_a
    qtext='If a sample of mass $%s mg$ taken from a specimen of total mass $%s g$ contains %s nanomoles of a bioactive compound, how many moles are present in the whole specimen?'%(
    mass_a, mass_b, count_a)
    qanswer='%s x 10e%s moles'%(round(mantissa(count_b),3), exponent(count_b)-9)
    qcat='A6 Scaling and Aliquots'
    return {'title':qcat, 'question':qtext,'answers':qanswer}


def q22():
    '''scaling and aliquots'''
    mass_a=random.randint(1,20)*10 # mg
    count_a = random.randint(30,300) 
    count_b = random.randint(1,10)*10**random.randint(3,6)
    mass_b = count_b * mass_a /count_a
    qtext='If a sample of mass $%s mg$ taken from a specimen contains %s nanomoles of a bioactive compound, what mass would contain $%s \\times 10^{%s}$ moles?'%(
    mass_a, count_a,round(mantissa(count_b),3), exponent(count_b)-9 )    
    qanswer='%s x10e%sg'%(round(mantissa(mass_b),2), exponent(mass_b)-3)
    qcat='A6 Scaling and Aliquots'
    return {'title':qcat, 'question':qtext,'answers':qanswer}
    
    
    
def q23():
    '''percentage solutions'''
    conc_a=random.randint(1,10)*10**random.randint(-1,0)
    vol_unit=random.randint(3,5)
    vol_e=(5-vol_unit)*-3
    vol_m=random.randint(1,999)/(10**random.randint(0,2))
    qcat='A7 Percentages and solutions'
    qtext='What mass of compound is required to make %s %sL of a %s\\%% w/v solution?'%(
    vol_m, unitlist[vol_unit],round(conc_a,2))
    qanswer="%s g"%(conc_a*vol_m*10*10**vol_e)
    return {'title':qcat, 'question':qtext,'answers':qanswer}
    
def q24():
    '''percentage solutions'''
    conc_a=random.randint(1,10)*10**random.randint(-1,0)
    vol_unit=random.randint(3,5)
    vol_e=((5-vol_unit)*-3)
    vol_m=random.randint(1,999)/(10**random.randint(0,2))
    mass=conc_a*vol_m*10*10**vol_e
    qcat='A7 Percentages and solutions'
    etext=" \\times 10^{%s}"%exponent(mass)
    if exponent(mass)==0:
        etext=''
    qtext='What is the concentration in \\%% w/v of a %s %sL solution containing $%s %s$ g of a compound?'%(
    vol_m, unitlist[vol_unit],round(mantissa(mass), 3-exponent(mass)),etext)
    qanswer="%s %% w/v"%(round(conc_a,3))
    return {'title':qcat, 'question':qtext,'answers':qanswer}
    
def q25():
    '''percentage solutions'''
    conc_a=random.randint(1,10)*10**random.randint(-1,0)
    vol_unit=random.randint(3,5)
    vol_e=(5-vol_unit)*-3
    vol_m=random.randint(1,999)/(10**random.randint(0,2))
    qcat='A7 Percentages and solutions'
    qtext='What volume of compound is required to make %s %sL of a %s\\%% v/v solution?'%(
    vol_m, unitlist[vol_unit],conc_a)
    qanswer="%s %sL"%(conc_a*vol_m/100, unitlist[vol_unit])
    return {'title':qcat, 'question':qtext,'answers':qanswer}
    
def q26():
    '''percentage solutions'''
    conc_a=random.randint(1,10)*10**random.randint(-1,0)
    vol_unit=random.randint(3,5)
    vol_e=(5-vol_unit)*-3
    vol_m=random.randint(1,999)/(10**random.randint(0,2))
    qcat='A7 Percentages and solutions'
    qtext='What is the concentration in \\%% v/v of a %s %sL solution containing %s %sL of a compound?'%(
    vol_m, unitlist[vol_unit],round(conc_a*vol_m*10,3-exponent(conc_a*vol_m)),unitlist[vol_unit-1])
    qanswer="%s %% v/v"%(round(conc_a,3))
    return {'title':qcat, 'question':qtext,'answers':qanswer}
    
def q27():
    '''mass in a mass per vol solution'''
    mass_m=random.randint(1,999)*10**random.randint(-1,0)
    mass_unit=random.randint(2,4)
    conc_m=random.randint(1,999)/10**random.randint(0,2)
    vol_unit=random.randint(2,4)
    newvol_unit=mass_unit+1
    mass_e=(5-mass_unit)*-3
    vol_e=(5-vol_unit)*-3
    conc_unit=vol_unit-1
    conc_e=(4-vol_unit)*-3
    newvol=mass_m/conc_m 
    while newvol > 1000:
        newvol/=1000
        newvol_unit +=1
    while newvol < 1:
        newvol*=1000
        newvol_unit -=1
        
    qcat='A1 Concentrations'
    qtext='What volume of a %s %sg/%sL solution is required to give %s %sg?'%(
    conc_m, unitlist[conc_unit],unitlist[vol_unit], round(mass_m,2-exponent(mass_m)), unitlist[mass_unit])
    qanswer='%s %sL'%(round(newvol,3-exponent(newvol)), unitlist[newvol_unit])
    return {'title':qcat, 'question':qtext,'answers':qanswer}

def q28():
    '''mass in a mass per vol solution'''
    mass_m=random.randint(1,999)*10**random.randint(-1,0)
    mass_unit=random.randint(2,4)
    conc_m=random.randint(1,999)/10**random.randint(0,2)
    vol_unit=random.randint(2,4)
    newvol_unit=mass_unit+1
    mass_e=(5-mass_unit)*-3
    vol_e=(5-vol_unit)*-3
    conc_unit=vol_unit-1
    conc_e=(4-vol_unit)*-3
    newvol=mass_m/conc_m 
    while newvol > 1000:
        newvol/=1000
        newvol_unit +=1
    while newvol < 1:
        newvol*=1000
        newvol_unit -=1
        
    qcat='A1 Concentrations'
    qtext='What mass of a compound is found in %s %sL of a %s %sg/%sL solution?'%(
    round(newvol,3-exponent(newvol)), unitlist[newvol_unit], conc_m, unitlist[conc_unit],unitlist[vol_unit])
    qanswer='%s %sg'%( round(mass_m,2-exponent(mass_m)), unitlist[mass_unit])
    return {'title':qcat, 'question':qtext,'answers':qanswer}


def q29():
    '''Beer-Lambert Law - Basic by w/v for DNA '''
    absorb= float(random.randint(1,1500))/1000
    unitText=['g','mg','ug', 'ng','pg']
    units=0    
    conc=absorb*0.00005
    while conc < 0.1:
        conc=conc*1000
        units+=1
    qcat='DNA Absorbance'
    qtext='''A pure sample of DNA gives 
    an absorbance reading of {:0.3f} when read in a cuvette with path length 1cm. 
    A 50$\\mu$g/ml solution of DNA has an absorbance reading of 1.0
What is the concentration of the test solution (in g/ml)?'''.format(absorb)    
    answer='%s %s/ml'%(round(conc,2), unitText[units])
    return {'title':qcat, 'question':qtext, 'answers':answer}
    
def q30():
    '''Gel migration distance '''
    standards=[100,200,300,400,500,600,700,800,900,1000,1200,1500,2000,3000,4000,5000,6000,8000,10000]
    heavy=[500,1000,3000]  
    band=random.randint(160,3500)
    gellength=random.randint(700,790)/100
    bandratio = gellength/(math.log(50000)-math.log(80))
    gelstart=8-gellength
    
    qcat='DNA Size'
    qtext='''\\setlength{\\unitlength}{1cm}
    \\begin{tabular}{ll}
    \\begin{picture}(4,8)
    \\put(0,0){\\line(1,0){4}}
    \\put(0,0){\\line(0,1){8}}
    \\put(4,8){\\line(-1,0){4}}
    \\put(4,8){\\line(0,-1){8}}
    \\linethickness{0.5pt}
    \\put(0.7,7){\\line(1,0){1}}
    \\put(0.7,7){\\line(0,1){0.4}}
    \\put(1.7,7){\\line(0,1){0.4}}
    \\put(0.7,7){\\line(0,1){0.4}}
    \\put(3.3,7){\\line(0,1){0.4}}
    \\put(2.3,7){\\line(0,1){0.4}}
    \\put(1.7,7){\\line(0,1){0.4}}
    \\put(2.3,7){\\line(1,0){1}}
'''
    for b in standards:
        if b in heavy:
            qtext += '\\linethickness{2.5pt}\n'
        else:
            qtext += '\\linethickness{1pt}\n'
        qtext += '\\put(0.7,{}){{\\line(1,0){{1}}}}\n'.format((math.log(b)-math.log(80))*bandratio+gelstart)
    qtext += '\\linethickness{{1.5pt}}\n\\put(2.3,{}){{\\line(1,0){{1}}}}\n'.format(
                                                    (math.log(band)-math.log(80))*bandratio+gelstart)    
    qtext+= '''\\end{picture}
     & \parbox[b][8cm][t]{110mm}{
    What is the molecular weight of the band in the lane on the right? The
    molecular weight standards have weights 100, 200, 300, 400, 500*, 600, 700, 800, 900, 1000*
    1200, 1500, 2000, 3000*, 4000, 5000, 6000, 8000, 10000 (extra dense bands marked with *).}
    \\end{tabular}    
    '''
    return {'title': qcat, 'question':qtext, 'answers': '{} bp'.format(band)}


def q101():
    '''Buffer composition'''
    conc_m=random.randint(1,20)*2.5*10**random.randint(0,1) # this will be mM
    vol_m = random.randint(1,50)*10**random.randint(0,2) #this will be ml
    pHdiff=random.randint(-20,20)/10.0
    buffer=random.sample(buffers,1)[0] 
    targetpH=round(buffer[2]+pHdiff, 1)
    abratio=10**(targetpH-buffer[2])
    conc_a=conc_m/(1+abratio)
    conc_b=conc_m*abratio/(1+abratio)
    mass_a=vol_m*conc_a*rmm[buffer[0]]/1000000
    mass_b=vol_m*conc_b*rmm[buffer[1]]/1000000
    qcat='B1 Buffers'
    qtext='what mass of %s (RMM: %s) and %s (RMM: %s, $pK_a$ %s ) would be required to make %s mL of a buffer of concentration %s mM and pH %s?'%(
    buffer[0], rmm[buffer[0]],buffer[1], rmm[buffer[1]],buffer[2], round(vol_m,0), round(conc_m,0), targetpH)
    qanswer='%s: %s g %s: %s g'%(buffer[0], round(mass_a,2-exponent(mass_a)),buffer[1], round(mass_b,2-exponent(mass_b)) )
    return {'title':qcat, 'question':qtext,'answers':qanswer}
    
def q102():
    '''Buffer composition'''
    conc_m=random.randint(1,20)*2.5*10**random.randint(0,1) # this will be mM
    vol_m = random.randint(1,50)*10**random.randint(0,2) #this will be ml
    pHdiff=random.randint(-20,20)/10.0
    buffer=random.sample(buffers,1)[0] 
    targetpH=round(buffer[2]+pHdiff, 1)
    abratio=10**(targetpH-buffer[2])
    conc_a=conc_m/(1+abratio)
    conc_b=conc_m*abratio/(1+abratio)
    mass_a=vol_m*conc_a*rmm[buffer[0]]/1000000
    mass_b=vol_m*conc_b*rmm[buffer[1]]/1000000
    qcat='B1 Buffers'
    qtext='What would be the concentration and pH of a %s mLsolution containing %s g of %s (RMM: %s) and %s g of %s (RMM: %s, $pK_a$ %s )?'%(
     round(vol_m,0),round(mass_a,2-exponent(mass_a)), buffer[0], rmm[buffer[0]], round(mass_b,2-exponent(mass_b)),buffer[1], rmm[buffer[1]],buffer[2])
    qanswer='%s mM pH %s'%(round(conc_m,0), targetpH )
    return {'title':qcat, 'question':qtext,'answers':qanswer}

def q103():
    ''' first order kinetics'''
    conc_b=random.randint(1,999)*10**random.randint(-2,0)
    conc_unit=random.randint(3,5)
    conc_unit_e=conc_unit
    time= random.randint(1,9)* 10**random.randint(0,5)
    change= random.random()
    conc_e=conc_b*change
    rate=-math.log(change)/time
    if exponent(conc_b*change)<0:
        conc_unit_e+=1
        conc_e*=1000
    etime=''
    if time>200:
        secs=time%60
        mins=(time%3600)//60
        hours=time//3600
        if hours:
            etime='%s hours '%hours
        etime += '%s minutes %s seconds'%(mins,secs)
    else:
        etime='%s seconds'%time
    qcat='B2 First order kinetics'
    qtext='''At the start of a reaction, the concentration of substrate is %s %sM. 
    After %s the concentration is %s %sM. What is the rate constant?'''%(
    round(conc_b, 2-exponent(conc_b)), unitlist[conc_unit], etime, 
    round(conc_e, 2-exponent(conc_e)), unitlist[conc_unit_e])
    rate_e=''
    if exponent(rate):
        rate_e=' x 10e%s'%exponent(rate)
    qanswer="%s%s per second"%(round(mantissa(rate),2), rate_e)
    return {'title':qcat, 'question':qtext,'answers':qanswer}

def q104():
    ''' first order kinetics'''
    conc_b=random.randint(1,999)*10**random.randint(-2,0)
    conc_unit=random.randint(3,5)
    conc_unit_e=conc_unit
    time= random.randint(1,9)* 10**random.randint(0,5)
    change= random.random()
    conc_e=conc_b*change
    rate=-math.log(change)/time
    if exponent(conc_b*change)<0:
        conc_unit_e+=1
        conc_e*=1000
    etime=''
    if time>200:
        secs=time%60
        mins=(time%3600)//60
        hours=time//3600
        if hours:
            etime='%s hours '%hours
        etime += '%s minutes %s seconds'%(mins,secs)
    else:
        etime='%s seconds'%time
    rate_e=''
    if exponent(rate):
        rate_e=' \\times 10^{%s}'%exponent(rate)
    qcat='B2 First order kinetics'
    qtext='''At the start of a reaction, the concentration of substrate is %s %sM. 
    If the rate constant is $%s%s s^{-1}$, what will be the concentration after %s?'''%(
    round(conc_b, 2-exponent(conc_b)), unitlist[conc_unit], round(mantissa(rate),2),rate_e, etime)     
    qanswer="%s %sM"%(round(conc_e, 2-exponent(conc_e)), unitlist[conc_unit_e])
    return {'title':qcat, 'question':qtext,'answers':qanswer}
    
def q105():
    ''' first order kinetics'''
    conc_b=random.randint(1,999)*10**random.randint(-2,0)
    conc_unit=random.randint(3,5)
    conc_unit_e=conc_unit
    time= random.randint(1,9)* 10**random.randint(0,5)
    change= random.random()
    conc_e=conc_b*change
    rate=-math.log(change)/time
    if exponent(conc_b*change)<0:
        conc_unit_e+=1
        conc_e*=1000
    etime=''
    if time>200:
        secs=time%60
        mins=(time%3600)//60
        hours=time//3600
        if hours:
            etime='%s hours '%hours
        etime += '%s minutes %s seconds'%(mins,secs)
    else:
        etime='%s seconds'%time
    rate_e=''
    if exponent(rate):
        rate_e=' \\times 10^{%s}'%exponent(rate)
    qcat='B2 First order kinetics'
    qtext='''At the start of a reaction, the concentration of substrate is %s %sM. 
    If the rate constant is $%s%s s^{-1}$, how long will it take for the concentration to drop to %s %sM?'''%(
    round(conc_b, 2-exponent(conc_b)), unitlist[conc_unit], round(mantissa(rate),2),rate_e, round(conc_e, 2-exponent(conc_e)), unitlist[conc_unit_e])     
    qanswer="%s"%(etime)
    return {'title':qcat, 'question':qtext,'answers':qanswer}
    
def q106():
    ''' first order kinetics'''
    conc_b=random.randint(1,999)*10**random.randint(-2,0)
    conc_unit=random.randint(3,5)
    conc_unit_e=conc_unit
    time= random.randint(1,9)* 10**random.randint(0,5)
    change= random.random()
    conc_e=conc_b*change
    rate=-math.log(change)/time
    if exponent(conc_b*change)<0:
        conc_unit_e+=1
        conc_e*=1000
    etime=''
    if time>200:
        secs=time%60
        mins=(time%3600)//60
        hours=time//3600
        if hours:
            etime='%s hours '%hours
        etime += '%s minutes %s seconds'%(mins,secs)
    else:
        etime='%s seconds'%time
    rate_e=''
    if exponent(rate):
        rate_e=' \\times 10^{%s}'%exponent(rate)
    qcat='B2 First order kinetics'
    qtext='''At the start of a first order reaction, the concentration of substrate is %s %sM. 
    After %s the concentration is %s %sM. What is the half life of the reaction?'''%(
    round(conc_b, 2-exponent(conc_b)), unitlist[conc_unit], etime, 
    round(conc_e, 2-exponent(conc_e)), unitlist[conc_unit_e])
    halflife=math.log(2)/rate
    htime=''
    if halflife>200:
        halflife=int(halflife)
        secs=halflife%60
        mins=(halflife%3600)//60
        hours=halflife//3600
        if hours:
            htime='%s hours '%hours
        htime += '%s minutes %s seconds'%(mins,secs)
    else:
        if halflife>10:
            htime='%s seconds'%int(halflife)
        else:
            htime='%s seconds'%round(halflife,2-exponent(halflife))                
    qanswer="%s"%htime
    return {'title':qcat, 'question':qtext,'answers':qanswer}

    
    
