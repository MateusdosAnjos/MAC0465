match=+1
mismatch=-1
gap=-2
memo={}
nrec=0

def p(a,b):
    if a==b: return match
    else: return mismatch

def gsim( s, t ):
    if len(s)==0: return len(t)*gap
    if len(t)==0: return len(s)*gap
    m = gsim(s[0:-1],t[0:-1]) + p(s[len(s)-1],t[len(t)-1])
    m = max( m, gsim(s[0:-1],t) + gap )
    m = max( m, gsim(s,t[0:-1]) + gap )
    return m

def gsimij( s, i, t, j ):
    global nrec
    if i==0: return j*gap
    if j==0: return i*gap
    nrec += 1
    m = gsimij(s,i-1,t,j-1) + p(s[i-1],t[j-1])
    m = max( m, gsimij(s,i-1,t,j) + gap )
    m = max( m, gsimij(s,i,t,j-1) + gap )
    return m

def gsimijm( s, i, t, j ):
    global nrec
    if memo.has_key( (i,j) ): return memo[(i,j)] 
    #print i, j
    if i==0: return j*gap
    if j==0: return i*gap
    nrec += 1
    m = gsimijm(s,i-1,t,j-1) + p(s[i-1],t[j-1])
    m = max( m, gsimijm(s,i-1,t,j) + gap )
    m = max( m, gsimijm(s,i,t,j-1) + gap )
    memo[(i,j)] = m
    return m

def main():
    global nrec
    s,t = 'AAAC','AGC'
    nrec=1
    print( gsim(s,t) )
    print nrec
    nrec = 1
    print( gsimij(s,len(s),t,len(t)) )
    print nrec
    nrec = 1
    print( gsimijm(s,len(s),t,len(t)) )
    print nrec

main()
