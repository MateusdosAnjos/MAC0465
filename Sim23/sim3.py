import sys
import unittest

match=+1
mismatch=0
gap=-1
menosinfinito=-2**31 # or float('-inf')
memo={}
nrec=0

def p(a,b):
    if a==b: return match
    else: return mismatch

def gsimijkm( s, i, t, j, u, k ):
    global nrec, memo
    if memo.has_key( (i,j,k) ): return memo[(i,j,k)] 
    if i<0 or j<0 or k<0: return menosinfinito
    nrec += 1
    m = gsimijkm(s,i-1,t,j-1,u,k-1) + p(s[i-1],t[j-1]) + p(s[i-1],u[k-1]) + p(u[k-1],t[j-1])
    m = max( m, gsimijkm(s,i-1,t,j-1,u,k) + p(s[i-1],t[j-1]) + 2*gap )
    m = max( m, gsimijkm(s,i-1,t,j,u,k-1) + p(s[i-1],u[k-1]) + 2*gap )
    m = max( m, gsimijkm(s,i,t,j-1,u,k-1) + p(u[k-1],t[j-1]) + 2*gap )
    m = max( m, gsimijkm(s,i-1,t,j,u,k) + 2*gap )
    m = max( m, gsimijkm(s,i,t,j-1,u,k) + 2*gap )
    m = max( m, gsimijkm(s,i,t,j,u,k-1) + 2*gap )
    memo[(i,j,k)] = m
    return m

def backtrace( s,t,u, m ):
    i,j,k = len(s),len(t),len(u)
    score = m[(i,j,k)]
    while i>0 or j>0 or k>0:
        if score == m[(i-1,j-1,k-1)] + p(s[i-1],t[j-1]) + p(s[i-1],u[k-1]) + p(u[k-1],t[j-1]):
            print s[i-1],t[j-1],u[k-1]
            i,j,k = i-1,j-1,k-1
        elif score == m[(i-1,j-1,k)] + p(s[i-1],t[j-1]) + 2*gap:
            print s[i-1],t[j-1],'-'
            i,j,k = i-1,j-1,k
        elif score == m[(i-1,j,k-1)] + p(s[i-1],u[k-1]) + 2*gap:
            print s[i-1],'-',u[k-1]
            i,j,k = i-1,j,k-1
        elif score == m[(i,j-1,k-1)] + p(u[k-1],t[j-1]) + 2*gap:
            print '-',t[j-1],u[k-1]
            i,j,k = i,j-1,k-1
        elif score == m[(i-1,j,k)] + 2*gap:
            print s[i-1],'-','-'
            i,j,k = i-1,j,k
        elif score == m[(i,j-1,k)] + 2*gap:
            print '-',t[j-1],'-'
            i,j,k = i,j-1,k
        elif score == m[(i,j,k-1)] + 2*gap:
            print '-','-',u[k-1]
            i,j,k = i,j,k-1
        else: raise Exception('Invalid Alignment Matrix')
        score = m[(i,j,k)]
        

class TestAllignmentMethods(unittest.TestCase):

    def test_TripleGlobalAlignment(self):
        global memo
        s,t,u = 'MQPILLL','MLRLL', 'MKILLL'
        memo[(0,0,0)] = 0
        p = gsimijkm(s,len(s),t,len(t),u,len(u))
        self.assertEqual(p,7)

if __name__ == '__main__':
    if len(sys.argv)!=4:
        unittest.main()         # roda teste de unidade test_TripleGlobalAlignment
    else:
        # na linha de comando do terminal rode algo como
        # python ./sim3.py 'MQPILLL' 'MLRLL' 'MKILLL'
        s,t,u = sys.argv[1:]
        memo[(0,0,0)] = 0
        print 'max score', gsimijkm(s,len(s),t,len(t),u,len(u)), 'with', nrec, 'recursive calls'
        backtrace(s,t,u,memo)
        
