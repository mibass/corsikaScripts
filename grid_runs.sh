#!/bin/bash
source grid_runs_inc.sh

#testrun
#DoRunSet 210001 210010 1000 14 1.3 1.72e4 corsika74003Linux_QGSJET_fluka #p

#FLUKA CMC RUNS #This set is down to 1.3 GeV/nucleon
AREA=853 #m^2  (2.56+20+3)*(10.36+20+3)
HIGHE=100000 #GeV (100 TeV)
T=7.2e-3 #s (7.2 ms is the total duration of a uboone spill=readout window + pre-readout window)

#proton only number of showers computation
ponlyshowers=$(./compute_NumShowers.py 1.8e4 1.3 $HIGHE $AREA $T)

#CMC model number of showers computations
pshowers=$(./compute_NumShowers.py 1.72e4 1.3 $HIGHE $AREA $T)
alphashowers=$(./compute_NumShowers.py 9.2e3 5.2 $HIGHE $AREA $T)
Nshowers=$(./compute_NumShowers.py 6.2e3 18.2 $HIGHE $AREA $T)
Mgshowers=$(./compute_NumShowers.py 9.2e3 31.2 $HIGHE $AREA $T)
Feshowers=$(./compute_NumShowers.py 9.2e3 72.8 $HIGHE $AREA $T)
echo $ponlyshowers, $pshowers, $alphashowers, $Nshowers, $Mgshowers, $Feshowers "showers (ponly, p, He, N, Mg, Fe)"
NSPILLS=10 # number of spills per run, adjust so that the max showers/job is around 1-1.5 million

#proton runs
#DoRunSet 110001 110001 $((${NSPILLS}*$ponlyshowers)) 14 1.3 1.8e4 corsika74003Linux_QGSJET_fluka #p

#CMC Runs
#DoRunSet 210001 210001 $((${NSPILLS}*$pshowers)) 14 1.3 1.72e4 corsika74003Linux_QGSJET_fluka #p
#DoRunSet 310001 310100 $((${NSPILLS}*$alphashowers)) 402 5.2 9.2e3 corsika74003Linux_QGSJET_fluka #alpha
#DoRunSet 410001 410100 $((${NSPILLS}*$Nshowers)) 1407 18.2 6.2e3 corsika74003Linux_QGSJET_fluka #N (14)
#DoRunSet 510001 510100 $((${NSPILLS}*Mgshowers)) 2412 31.2 9.2e3 corsika74003Linux_QGSJET_fluka #Mg (24)
#DoRunSet 610001 610100 $((${NSPILLS}*Feshowers)) 5626 72.8 6.2e3 corsika74003Linux_QGSJET_fluka #Fe (56)



#FLUKA p Runs with only hadronic LE tracking
#TEMPLATEFILE="keephads_corsika_input_TEMPLATE"
#NSPILLS=5 # number of spills per run
#USAGE_MODEL="OPPORTUNISTIC"
#DoRunSet 700001 701000 $((${NSPILLS}*1000000)) 14 1.3 1.8e4 corsika74003Linux_QGSJET_fluka #p



#GHEISHA CMC runs
#DoRunSet 220001 220100 $((${NSPILLS}*$pshowers)) 14 1.3 1.72e4 corsika74003Linux_QGSJET_gheisha #p
#DoRunSet 320001 320100 $((${NSPILLS}*$alphashowers)) 402 5.2 9.2e3 corsika74003Linux_QGSJET_gheisha #alpha
#DoRunSet 420001 420100 $((${NSPILLS}*$Nshowers)) 1407 18.2 6.2e3 corsika74003Linux_QGSJET_gheisha #N (14)
#DoRunSet 520001 520100 $((${NSPILLS}*Mgshowers)) 2412 31.2 9.2e3 corsika74003Linux_QGSJET_gheisha #Mg (24)
#DoRunSet 620001 620100 $((${NSPILLS}*Feshowers)) 5626 72.8 6.2e3 corsika74003Linux_QGSJET_gheisha #Fe (56)

echo 
echo Submitted $submittedJobs jobs.
