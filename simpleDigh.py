import numpy as nu
import sys
orgs =3 # Number of organisms
spk = 0 # Offset in dictionary used for transition table where
        # the next word to speak appears.
newthk =1 # Offset in dictionary used for transition table where
        # the next thought to think appears.
connectionmat = nu.zeros ((orgs,orgs), nu.int32)
probConnect = .5
seedint = 196
nu.random.seed(seedint)
rows = 16
bitl = 4 # Maximum bit length.
tranTable=nu.zeros((rows,4),nu.int32)
def prOggs(og,itr):
	print
	print (itr)
	for s in range (1,orgs+1):
		print (s,'hear:'+og[s]['hear'])
		print (s,'think:'+og[s]['think'])
		print (s,'say:'+og[s]['say'])
		print ()

# Fill connection matrix with Digh's random values (p. 45)					
def digCon(cma):
	cma[0][1]=1
	cma[1][0]=1
	cma[2][0]=1
	
# Fill transition table with Digh's values (p. 44)	
def fillTran():
	tranT ={}	
	tranT[('0','0')] = ('0','0')
	tranT[('0','1')] = ('11','0')
	tranT[('0','10')] = ('10','1')
	tranT[('0','11')] = ('10','0')
	tranT[('1','0')] = ('10','11')
	tranT[('1','1')] = ('0','11')
	tranT[('1','10')] = ('0','0')
	tranT[('1','11')] = ('0','0')
	tranT[('10','0')] = ('11','1')
	tranT[('10','1')] = ('10','11')
	tranT[('10','10')] = ('0','1')
	tranT[('10','11')] = ('1','0')
	tranT[('11','0')] = ('1','1')
	tranT[('11','1')] = ('0','1')
	tranT[('11','10')] = ('0','10')
	tranT[('11','11')] = ('10','11')				
	return tranT
		
def makeOrgs(): # Page 43
	lorgs = {}
	lorgs[1]={}
	lorgs[1]['hear']= '11'
	lorgs[1]['think']= '1'
	lorgs[1]['say']= '0'
	lorgs[2]={}
	lorgs[2]['hear']= '0'
	lorgs[2]['think']= '1'
	lorgs[2]['say']= '0'
	lorgs[3]={}
	lorgs[3]['hear']= '1'
	lorgs[3]['think']= '10'
	lorgs[3]['say']= '0'
	return lorgs
	
def recordState(og,stdic, num):
		li=[]
		for oi in range(1, orgs+1):
			# Put all entries in all organisms in one list
			# so that cycles may be detected.
			li+=[og[oi]['hear'],og[oi]['think'],og[oi]['say']]
		stdic[num] = tuple(li) # Change list to tuple.
		
def chkForCycle(stdic):#,ckt):
	klis= max(stdic.keys())
	ckt = stdic[klis] # The most recently entered tuple
			  # is at key 'klis'. Check this tuple
			  # klis against the prior tuples to 
			  # see if it matches them. If yes,
			  # flag the cycle and exit.
	for yy in range (klis):
		if stdic[yy] == ckt:
			print ("Cycle detected:", yy, klis)
			print ("Transient length:", yy -1)
			print ("Cycle length:", klis - yy)
			sys.exit()
		
def doSim(cyc,oggs,tra,cmat):
	stateDict={}
	recordState(oggs,stateDict, 0)
	f=1
	while (1):#for f in range(1, cyc+1):	
		prOggs(oggs,f-1)
		if f != 1: recordState(oggs,stateDict, f-1)
		chkForCycle(stateDict)
		for og in range(1, orgs+1):
			for oi in range(1, orgs+1):
				if cmat[og-1][oi-1]: # If there is a connection,
						 # listen to what is currently in ears, 
						 # consider current thought,
						 # then put new output in mouth.
						oggs[og]['say'] = tra[(oggs[og]['hear'],oggs[og]['think'])][ spk ]
						oggs[og]['think'] = tra[(oggs[og]['hear'],oggs[og]['think'])][ newthk ]
						oggs[oi]['hear'] = oggs[og]['say']
		
		if f > cyc: break
		f=f+1
							
digCon(connectionmat)
trand = fillTran()
lorgs = makeOrgs() # Put population in the initial state.

cycles = 7

doSim(cycles,lorgs,trand,connectionmat)



	

