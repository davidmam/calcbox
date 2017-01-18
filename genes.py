
gene = 'ATGATGAGGTCGAAAGTAGACCATATCCGCCGGAAGCTCTATAGTCA' + \
       'CGATGCCCCAGCATGGGGTGCTATATGTGAATGA'

geneticCode = {
        "AAA":"K", "AAC":"N", "AAG":"K", "AAT":"N",
        "ACA":"T", "ACC":"T", "ACG":"T", "ACT":"T",
        "AGA":"R", "AGC":"S", "AGG":"R", "AGT":"S",
        "ATA":"I", "ATC":"I", "ATG":"M", "ATT":"I",
        "CAA":"Q", "CAC":"H", "CAG":"Q", "CAT":"H",
        "CCA":"P", "CCC":"P", "CCG":"P", "CCT":"P",
        "CGA":"R", "CGC":"R", "CGG":"R", "CGT":"R",
        "CTA":"L", "CTC":"L", "CTG":"L", "CTT":"L",
        "GAA":"E", "GAC":"D", "GAG":"E", "GAT":"D",
        "GCA":"A", "GCC":"A", "GCG":"A", "GCT":"A",
        "GGA":"G", "GGC":"G", "GGG":"G", "GGT":"G",
        "GTA":"V", "GTC":"V", "GTG":"V", "GTT":"V",
        "TAA":"*", "TAC":"Y", "TAG":"*", "TAT":"Y",
        "TCA":"S", "TCC":"S", "TCG":"S", "TCT":"S",
        "TGA":"*", "TGC":"C", "TGG":"W", "TGT":"C",
        "TTA":"L", "TTC":"F", "TTG":"L", "TTT":"F" 
    }

protein = ''

for c in range(0, len(gene), 3):
    codon = gene[c:c+3]    
    aa = geneticCode[codon]
    protein = protein + aa
    
print(protein)
    





protein = ''
for c in range(0,len(gene),3):
    codon = gene[c:c+3]
    aa = geneticCode[codon]
    protein = protein + aa
    
print(protein)



# base composition
bases={}
for b in gene:
    bases[b] =bases.get(b, 0)+1
    

































































































































































