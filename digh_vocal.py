from numpy import mean, int8, power, arange, zeros
from numpy import random
from copy import deepcopy
import sys
'''
This program is designed following "The Greek Miracle: An Artificial Life
Simulation of the Effects of Literacy on the Dynamics of Communication." by 
Andrew Douglas Digh. This program only simulates vocal communication among a variable 
population of simple artificial organisms. Each organism is given a number from one
up to the number of organisms. All organisms are placed in one dictionary keyed by
organism number. Organism dictionaries are created by the proby.makeOrgs() function.
Each organism is itself a dictionary containing a set of integer variables representing 
various biological features. In this program there are three dictionary entries: hear,
think, say. The initial state of each of the three integers modeling the organism 
are chosen randomly with a seeded random number generator. The organisms communicate
with each other according to a connection matrix that is a square matrix representing 
the Cartesian product of the one dimensional array {1,2,...number of organisms} with itself. 
A one represents a connection between two organisms, a zero indicates no connection. No organism
connects to itself. The connection matrix is filled randomly. Notice that the
square structure of the connection table creates an upper and lower triangular
echelons so that each pair of (row,column) in the Cartesian product is represented twice
assuming order doesn't matter. The exception is the diagonal of the square where
each organism is paired with itself. As no organism connects to itself, the diagonal
contains zeros. See page 3 of the accompanying marnfix.pdf file for an explanation
of how a spanning path is develeoped from the connection table. The spanning
path changes and is kept at admin.spanlist.
   Once the spanning path is determined and the initial conditions of the organisms
are set, the function doSim() simulates communication within the organism population
until a cycle occurs or the number of iterations surpasses the maximum iteration value
contained in the global integer max_iterations.
   After the simulation run completes, the transient length and the cycle length are
recorded. The transient length is the number of iterations before the state of all organism 
together occurs that is eventually repeated to determine a cycle. The cycle length 
is the difference between the iteration numbers of the state that repeat to determine a cycle.
If the maximum number of iterations has been surpassed, the transient length is set with 
max_iterations and the cycle length is filled with zero.
'''
full_log_file = 'full_log.txt'
full_log = False # If true, output The current state for each
# simorg to full_log_file. If this is true, over 200,000 lines
# are often recorded in this file.
log_tables = True # Print out connection table and transition table.
logarunfile = 'tables.txt' # File where tables will be printed.
tally_by_prob= True # Write all cycle lengths and transient lengths to a file
# for each probability
tally_by_prob_file = 'tally_by_prob.txt'
write_summary = True # Write all cycle lengths and transient lengths to a file
# for each probability
write_csvs = True
write_cycle_csv_file= 'abigcycles_simorgs.csv'
write_b4_csv_file= 'abigb4_simorgs.csv'
write_summary_file = 'summary.txt'
cardinality = 9 # This number squared is the number of rows in
# the transition table. This squared value  is also used as a maximum integer
# for randomly selected integer to fill the ears, brain, and
# mouth for the initial conditions for organisms. It is also
# used as a maximum for random integer selection for the transition
# table entries that are not pre-designated as the tuple (0,0).
orgs =50 # Number of organisms, or if gradualPop is true, the maximum
		# number of organisms.
startPop = 5
stepPop = 5
gradualPop = True # If true, build up to a maximum population of orgs,
# adding one at a time from startPop
if not gradualPop: startPop = orgs

# The transition table is in a dictionary located at proby.tranT
# The dictionary keys are tuples comprising the pairwise combinations
# of the cartesian product of the set {1,2...cardinality**2}
# with itself. The set elements are in binary strings.
# Each transition table key corresponds to an entry that is also
# a tuple.
spk = 0 # Offset in each transition table dictionary entry tuple
		# the next word to speak appears.
newthk = 1 # Offset in dictionary used for transition table entry
		# where the next thought to think appears.

llambda = .9 # The lambda parameter was invented by Chris Langton,
		# who worked at the Santa Fe Institute in the 1990s. One minus
		# the lambda parameter determines the probability that a chosen specific
		# state occurs, in this case ('0','0')

max_iterations = 1000
startSeeds= 100
totalSeeds = 5 # Seed for psuedo random number generation. For
# each seed, the  exact same series of random
# numbers will always recur next time the program runs.

# Each seed is used to create a random transition table at proby.tranT and random
# initial states for all organisms, which are created as dictionary by the function
# proby.makeOrgs() which is only called in the doit() function.

# These variables are used in proby.getseeds() to create
# a one dimensional array of connection probabilities at proby.probray.
endConnectProb = 1.0
beginConnectProb = 0.0
stepConnectProb =.05

class admin(object):
	def setit(self):
		#If a list of cardinalities is given, each will run separately with
		#some code improvement.
		self.card=[cardinality]
		self.rows=[ power(cardinality,2)]

	def data_format_text(self,fout):
		fout.write('\n\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n')
		fout.write('\nData Format Key\nOrganisms: Number of organisms in trial\nProbability: Interconnect probability between organisms\n')
		fout.write('[seed_number, seed, transient_length, cycle_length]\n')
		fout.write('[seed_number, seed, transient_length, cycle_length]\n')
		fout.write('[seed_number, seed, transient_length, cycle_length]\n')
		fout.write('[seed_number, seed, transient_length, cycle_length]\n')
		fout.write('\nMean cycle length: xx\nMean transient length: yy\n')
		fout.write('\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n')

	def tally_by_probf(self,bb):#, seedno, seed):
		fout = open(tally_by_prob_file, 'a')
		fout.write('Transient Lengths and Cycle lengths by Probability and Seed\n')
		self.data_format_text(fout)
		for smorg in sorted(list( bb.organ_dit.keys())):
			for pkee in sorted(list(bb.organ_dit[smorg].keys())):
					fout.write('\n*********************************************\n')
					for yyz in bb.organ_dit[smorg][pkee]:
							fout.write('\nOrganisms: ' + str(smorg))
							fout.write('\nProbability: ' + str(pkee) + '\n')
							cycs = []
							tls = []
							for yy in yyz:
								cycs+=[yy[3]]
								tls+=[yy[2]]
								fout.write(str(yy)+'\n')
							mnc= mean(cycs)
							mnt =  mean(tls)
							bb.cycle_sum[smorg][pkee]=mnc
							bb.tls_sum[smorg][pkee] = mnt
							fout.write('Mean cycle length: ' + str(mnc) + '\n')
							fout.write('Mean transient length: ' + str(mnt) + '\n')
					fout.write('___________________________\n')
		fout.close()
		if write_summary:
			fout = open(write_summary_file, 'a')
			for smig in bb.cycle_sum.keys():
				for pr in bb.cycle_sum[smig].keys():
					fout.write('\nFor Organisms: ' + str(smig) + ' for probability '+str(pr)+'\n')
					fout.write('Mean cycle length: ' + str(bb.cycle_sum[smig][pr]) + '\n')
					fout.write('Mean transient length: ' + str(bb.tls_sum[smig][pr]) + '\n')
		if write_csvs:
			fout = open(write_cycle_csv_file, 'a')
			foutb = open(write_b4_csv_file, 'a')
			fout.write('organisms+probability,cycles\n')
			fout.write('smorg+prob,cycls\n')
			foutb.write('organisms+probability,transient\n')
			foutb.write('smorg+prob,before\n')
			for smig in sorted(list(bb.cycle_sum.keys())):
				for pr in sorted(list(bb.cycle_sum[smig].keys())):
					fout.write( str(smig+(stepPop*pr))+','+ str(bb.cycle_sum[smig][pr]) +'\n')
					foutb.write(  str(smig+(stepPop*pr))+','+str(bb.tls_sum[smig][pr]) + '\n')

	def record_cycle_info (self, bb, cProb, cy, tl, exceeded, seedno, seed, num_orgs):
		if tl == 0: cy =0
		if not exceeded:
			bb.probtls[num_orgs][cProb]+=[[seedno,seed,tl,cy]]
		else:
			bb.probtls[num_orgs][cProb] += [[seedno,seed,max_iterations,0]]
		if (seedno == totalSeeds -1):
			bb.organ_dit[num_orgs][cProb] += [deepcopy(bb.probtls[num_orgs][cProb] )]

	def prOggs(self, og, itr):
		fout = open(full_log_file, 'a')
		fout.write('\n\nIteration: ' + str(itr))
		for s in range(1, orgs + 1):
			fout.write('\nOrganism Number: ' + str(s) + '\n')
			fout.write('hear: ' + str(og[s]['hear']) + '\n')
			fout.write('think: ' + str(og[s]['think']) + '\n')
			fout.write('say: ' + str(og[s]['say'])+ '\n')
		fout.close()

	def recordState(self, og, stdic, num):
		li=[]
		for oi in range(1, len(og.keys())+1):
			# Put all entries in all organisms in one list
			# so that cycles may be detected.
			li+=[og[oi]['hear'],og[oi]['think'],og[oi]['say']]
		stdic[num] = tuple(li) # Change list to tuple.

	def chkForCycle(self,stdic,seed,seedno,prob,bb,num_orgs):
		klis= max(stdic.keys())
		ckt = stdic[klis] # The most recently entered tuple
						  # is at key 'klis'. Check this tuple
						  # klis against the prior tuples to 
						  # see if it matches them. If yes,
						  # record cycle detection statistics
		for yy in range (klis): # We don't have to add one too klis
				# because it is the location of the ckt tuple. The range
				# function ends at one less than klis.
			if stdic[yy] == ckt:		
				if full_log: self.log_cycle(seedno,seed,yy,klis,prob,full_log_file)
				self.record_cycle_info(bb, prob, klis - yy, yy, False, seedno,seed,num_orgs)
				return True, klis, yy
		return False, klis, yy

	def log_cycle(self,seedno,seed,yy,klis,proba,fouta):
		fout = open (fouta, 'a')
		fout.write( "\n\nCycle detected beginning at iteration "+ str(yy)+' ending at ' + str(klis) +'\n')
		fout.write("Probability: " + str(proba) + '\n')
		fout.write('Seed Number: ' + str(seedno) + ', seed: ' + str(seed) + '\n')
		fout.write( "Transient length: " + str( yy )+'\n')
		fout.write( "Cycle length: " + str(klis - yy)+'\n')
		fout.close()

	def toBin(self,bitl):
		ouLi=[]
		for x in range(bitl):
			ouLi+=[int(bin(x), base=2)]
		return ouLi

	def outMats(self, cm, trand,bitl,prob, orgtally):
		ouList=self.toBin(bitl)
		inList=self.toBin(bitl)
		if full_log:
			fout = open(full_log_file, 'a')
			fout.write('\nTransition Table:')
			for ou in ouList:
				for oi in inList:
					fout.write ( '\n'+str((ou,oi))+' '+str(trand[(ou,oi)]))
			fout.write('\nConnection Table:')
			for ou in range(cm.shape[0]):
				fout.write('\n')
				for oi in range (cm.shape[1]):
					fout.write ( +str(cm[ou][oi]))
			fout.close()
		if log_tables:
			fout = open(logarunfile, 'a')
			fout.write('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
			fout.write('\nNumber of organisms: '+str(orgtally)+'\n')
			fout.write('Probability of interconnection: '+str(prob)+'\n')
			fout.write('\nTransition Table:')
			for ou in ouList:
				for oi in inList:
					fout.write('\n' + str((ou, oi)) + ' ' + str(trand[(ou, oi)]))
			fout.write('\nConnection Table:')
			for ou in range(cm.shape[0]):
				fout.write('\n')
				for oi in range (cm.shape[1]):
					fout.write ( str(cm[ou][oi]) + ' ')
			fout.close()

	def createXmat(self,orr):
		return  zeros ((orr,orr),  int8)

	def spanList(self,cma):
		sq= cma.shape[0]
		self.spanlist=[]
		for x in range(sq):
			for y in range (sq):
				if x == y: continue
				if cma[x][y]: self.spanlist +=[[x+1,y+1]]
		
			
class proby(object):
	def __init__(self):
		# Note 'endConnectProb+stepConnectProb' Adding the step to the end point is needed
		# because the arange function completes at the iterval prior to any endpoint.
		self.probray = arange(beginConnectProb, endConnectProb + stepConnectProb, stepConnectProb)
		self.organ_dit = {}
		for x in arange(startPop, orgs + 1, stepPop):
			self.organ_dit[x] = {}
			for pr in self.probray:
				self.organ_dit[x][pr] = []  # This will be a list of lists.
		self.cycle_sum= {}
		for lorgs in self.organ_dit.keys():
			self.cycle_sum[lorgs]= {}
			for pr in self.probray:
					self.cycle_sum[lorgs][pr] = 0.0
		self.tls_sum = deepcopy(self.cycle_sum)


	def seedr(self, seedint):
		random.seed(seedint)

	def getSeeds(self):
		self.seeds=arange (startSeeds,startSeeds+totalSeeds+1)
		self.probtls={}
		for xk in self.organ_dit.keys():
			self.probtls [xk]= {}
			for p in self.probray:
						self.probtls[xk][p] = []
						# A dictionary of lists that will contain transient lengths
						# and cycles for each probability. If the maximum iterations is
						# exceeded, the transient length is recorded as the maximum
						# iterations and cycle length is filled with zero.

	def anint(self,prob):
		if random.ranf() <= prob:
			return int('1', base=2)
		else: return int('0', base=2)

	def pikEnt(self,bg,ed):
		pk=random.choice(range(bg,ed))
		return int(bin(pk), base=2)

	def lambray(self,ry):
		# Iterate over array ry and randomly replace pre-existing zeros with ones
		# with the probability of a one occurring equal to lambda.
		for zz in range(len(ry)):
			ry [zz] = self.anint (llambda)

	# Generate interconnection matrix.
	def genInter(self,cma,rgs,probConnect):	
		for x in range(rgs):
				for y in range (rgs):
					if x != y: # No organism connects to itself.
						cma[x][y] = self.anint(probConnect)

	# Create simulation organisms, simorgs, placing random
	# initial data in ears, brain and mouth. Enumerate
	# organisms starting at 1.
	def makeOrgs( self, jy, bitl):
		lorgs = {}
		for yu in range (1,jy+1):
			lorgs[yu]={}
			lorgs[yu]['hear']= self.pikEnt(0,bitl)
			lorgs[yu]['think']= self.pikEnt(0,bitl)
			lorgs[yu]['say']= self.pikEnt(0,bitl)
		return lorgs

	def noZeroPick (self,lis,toZips,bitl):
			rw =-1
			for ou in range(bitl):
				for oi in range(bitl):
					rw+=1
					if toZips[rw] == 0: # or (ou==0 and oi ==0):
						lis[rw][0] = int('0', base=2)
						lis[rw][1] = int('0', base=2)
					else:
						lis[rw][0] = self.pikEnt(0,bitl)
						lis[rw][1] = self.pikEnt(0,bitl)
						if (lis[rw][0] == int('0', base=2)) and (lis[rw][1] ==int('0', base=2)):
							# This condition won't happen often,
							# but is necessary to preserve the integrity of the
							# lambda parameter
							lis[rw][0] = self.pikEnt(1, bitl)
							lis[rw][1] = self.pikEnt(1, bitl)
			return lis

	def mkLis(self,ni):
		lii=[]
		for d in range(ni):
			lii+=[[int(bin(0), base=2),int(bin(0), base=2)]]
		return lii

	def fillTranRand(self,tableRows,bitl):
		# This function creates a dictionary representation of
		# a transition table.
		# Create a list of length equal to tableRows.
		toZip = tableRows *[0]
		noZeroList = self.mkLis (tableRows)
		self.lambray (toZip) # put a one for each table entry where the output entries
		# in the transition table will not be ('0','0')
		outList=self.noZeroPick(noZeroList,toZip,bitl) # Fill noZeroList with random output pairs
		# other than ('0','0') and place randomly selected ('0','0')
		# entries into the noZeroList and return the list of random outputs
		# as outList.
		tranTt ={}
		rw = 0	
		for x in range(bitl):
				for y in range (bitl):
					tranTt[((int(bin(x), base=2),int(bin(y), base=2)))]= tuple (outList[rw])
					rw += 1
		self.tranT = tranTt

class sim(object):		
	def doSim(self,max_iter,oggs,tra,adm,seed,seedno,prob,bb):
			stateDict={}
			adm.recordState(oggs,stateDict, 0) # Record the initial state
				# of the organisms in stateDict at dictionary key value 0.
			if full_log: adm.prOggs(oggs, 0) # Record the initial state values in the
				# full log file.
			f=1
			while 1:
				for k in adm.spanlist:
				# If there is a connection,
				# listen to what is currently in ears,
				# consider current thought,
				# then put new output in mouth.
					oggs[k[0]]['say'] = tra[(oggs[k[0]]['hear'],oggs[k[0]]['think'])][ spk ]
					oggs[k[0]]['think'] = tra[(oggs[k[0]]['hear'],oggs[k[0]]['think'])][ newthk ]
					oggs[k[1]]['hear'] = oggs[k[0]]['say']
					#sys.exit()
				adm.recordState(oggs,stateDict, f)
				if full_log: adm.prOggs(oggs, f)
				out, klis, yy = adm.chkForCycle(stateDict,seed, seedno,prob,bb,len(oggs))
				if out : return
				f=f+1	
				if self.endRun(f,max_iter,adm,bb,seed,seedno, prob, klis,yy,len(oggs)) :
					continue
				else: 
						return

	def endRun(self,f,max_iter,adm, bb, seed, seedno,prob, klis, yy, num_orgs):
		if f >= max_iter:
			adm.record_cycle_info(bb, prob, klis - yy, yy, True,seedno,seed,num_orgs)
			if full_log:
				fout = open(full_log_file, 'a')
				fout.write('\n\nIteration: ' + str(f))
				fout.write('\nNo cycles detected for seed: ' + str(seed))
				fout.write('\nSeed number: ": ' + str(seed)+'\n')
				fout.write('\nProbability ": ' + str(prob) + '\n')
				fout.close()
			return 0
		return 1

def main():
	bb= proby()
	bb.getSeeds()
	ad = admin()
	ad.setit()
	cc = sim()
	for ut in range(len(ad.card)):
		for s in range(totalSeeds):
			bb.seedr(bb.seeds[s])
			for orr in bb.organ_dit.keys():
				bb.fillTranRand(ad.rows[ut], ad.card[ut])
				connectionmat = ad.createXmat(orr)
				for pr in bb.probray:
					oggs = bb.makeOrgs(orr, ad.card[ut])
					bb.genInter(connectionmat,orr,pr)
					ad.spanList(connectionmat)			
					cc.doSim(max_iterations,oggs,bb.tranT, ad,bb.seeds[s],s,pr,bb)
					count_organisms = max(list(oggs.keys())) # orgnanisms are keyed by their integer enumeration
					# from one to the maximum in the global variable orgs. If gradualPop is True, count_organisms
					# will be less than orgs - it will step up to orgs by the global stepPop.
					if full_log or log_tables:ad.outMats(connectionmat, bb.tranT, ad.card[ut],pr,count_organisms)

	if tally_by_prob: ad.tally_by_probf(bb)
				#if tally_by_prob:ad.tally_by_probf(bb)

if full_log: open(full_log_file, 'w') # Empty the full log file if it exists, else create it.
if log_tables: open(logarunfile, 'w')
if tally_by_prob: open(tally_by_prob_file, 'w') # Empty the cycle_log_file if it exists, else create it.
if write_summary: open(write_summary_file, 'w')
if write_csvs:
	open(write_cycle_csv_file, 'w')
	open(write_b4_csv_file, 'w')
main()




	

