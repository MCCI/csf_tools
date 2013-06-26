#!/local/python-2.7.1/bin/python  
import sys

class _CSF:
    def __init__(self, id, alphas, betas, coef):
        self.id = int(id)
        self.alphas = alphas
        self.betas = betas
        self.coef = coef

class CSF_Real(_CSF):
    def __init__(self, id, alphas, betas, coef):
        _CSF.__init__(self, id, alphas, betas, coef)
        self.coef = float(self.coef)
    def __str__(self):
        ls = ['{0:6d}  {1: 20.16E} {2:12d} {3:12d}\n'.format(self.id, self.coef, \
            					       self.alphas[0],  \
            					       self.betas[0]) ]
        for i in range(1, len(self.alphas)):
            ls.append('{0:44d} {1:12d}\n'.format(self.alphas[i], self.betas[i]))
        return ''.join(ls)

class CSF_Complex(_CSF):
    def __init__(self, id, alphas, betas, coef):
        _CSF.__init__(self, id, alphas, betas, coef)
        self.coef = complex(self.coef)
    def __str__(self):
        ls =  ['{0:6d}  {1: 20.16E} {2: 20.16E} {3:12d} {4:12d}\n'\
              .format(self.id, self.coef.real, self.coef.imag,    \
                      self.alphas[0], self.betas[0]) ]
        for i in range(1, len(self.alphas)):
            ls.append('{0:68d} {1:12d}\n'.format(self.alphas[i], self.betas[i]))
        return ''.join(ls)

def parse_CSFList(file):
    EOF = False
    line = file.next()
    while not EOF:
        if not ( 4 <= len(line.split()) <= 5 ):
            print "csf_tools: error, malformed CSF declaration:"
            print line
            print "Stopping..."
            sys.exit(1)
        ls = [line]
        line = file.next()
        while len(line.split()) == 2:
            ls.append(line)
            try:
                line = file.next()
            except StopIteration:
                EOF = True
                line = ''
        yield read_CSF(ls)

def read_CSF(lines):
    lines = [l.split() for l in lines]
    if len(lines[0]) == 4:
        cmplx = False
    elif len(lines[0]) == 5:
        cmplx = True
    else:        
        print "csfgrab: error, malformed CSF declaration:"
        print lines[0]
        print "Stopping..."
        sys.exit(1)
    for j in range(1, len(lines)):
        if len(lines[j]) != 2:
            print "csfgrab: error, malformed CSF occupation vector:"
            print lines[j]
            print "Stopping..."
            sys.exit(1)
    id = int(lines[0][0])
    occlist_alpha = (lines[0][-2],) + \
        	    tuple([lines[j][0] for j in range(1,len(lines))])
    occlist_beta  = (lines[0][-1],) + \
        	    tuple([lines[j][1] for j in range(1,len(lines))])
    occlist_alpha = map(int, occlist_alpha)
    occlist_beta = map(int, occlist_beta)
    if cmplx:
        coef = float(lines[0][1]) + float(lines[0][2])*1j
        return CSF_Complex(id, occlist_alpha, occlist_beta, coef)
    else:
        coef = float(lines[0][1])
        return CSF_Real(id, occlist_alpha, occlist_beta, coef)
