
This python code provides the algorithm and some of the code to accomplish the artificial
life modelling suggested in Andrew Digh's paper in the file Digh-Greek-Literacy.pdf. The file
digh_vocal.py uses the algorithm described in marnfix.pdf to simulate artificial humans
speaking Greek. After each simulation run completes, the transient length and the cycle length
are recorded. The transient length is the number of iterations before the state of all organism
together occurs that is eventually repeated to determine a cycle. The cycle length is the difference 
between the iteration numbers ofthe state that repeats to determine a cycle.The simulations do not 
include written Greek as Digh had hoped for.
 A finding of this experiement is that the transient lengths tend to be about twice as long
as cycle lengths for a given point on the x-axis partitions. In the higher population sizes, this is more
markedly true, more than twice as long. And generally along the x-axis partition, the higher the
connection probability, the more transient length exceeds cycle length. An abstract way to look
at this might be: once the pump is primed, once some work is done, the cycles come more easily.
   Real world analogs? Once someone learns to speak, various cyclic benefits accrue. Once one gets
that college degree, renumerative benefits recur. Once that bitcoin is mined, money has been added
to the money supply, which is usually only accomplished by bank lending or Treasury printing money:
cyclic benefits recur.
   I am looking for collaborators who might extend the results presented to include written Greek,
or also might have other uses for the code. The file simpleDigh.py is a simplified rendition
of the algorithm in marnfix as it does not include a spanning path and it uses only the single
transition table supplied in Digh's paper, and employs only three organisms.
As far as other uses of the code, please read writing-as-technolgy.pdf. This document 
identifies a missing mathematics of writing, but does not fully describe the missing
mathematics. A part of the missing math is the study of the dispersion of the technology 
with artificial life modeling, which this beginning code is intended to initiate.
This is part of the study of writing at a group level. Also missing is much work on characterisitcs
of writing within the individual. I have coded some of the models given in Eliasmith's 1991
"Neural Engineering" as a starting point in this regard.
   The results given in the graph are summed over multiple seeds, in this case 5 seeds for each
probability.
   I use kst2 for graphs, there is now a Windows version. Kst2 data wizard doesn't work unless
a parameter is passed to kst2: $ kst2 file_with_data.csv f= 360.
   There appear to be significant errors in Digh's computed results, details upon request.

![cycles](https://user-images.githubusercontent.com/24655619/122244785-261ed000-ce93-11eb-9d33-7ec9e77d8174.png)
![transient](https://user-images.githubusercontent.com/24655619/122244809-2c14b100-ce93-11eb-84b7-81cc86f0b7ec.png)
