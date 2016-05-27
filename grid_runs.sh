#!/bin/bash
source grid_runs_inc.sh

DoRunSet 210001 210001 1000 14 1.3 1.72e4 corsika74003Linux_QGSJET_fluka #p

#FLUKA CMC RUNS #This set is down to 1.3 GeV/nucleon
NSPILLS=2 # number of spills per run
#DoRunSet 210001 210001 $((${NSPILLS}*863301)) 14 1.3 1.72e4 corsika74003Linux_QGSJET_fluka #p
#DoRunSet 310011 310100 $((${NSPILLS}*44694)) 402 5.2 9.2e3 corsika74003Linux_QGSJET_fluka #alpha
#DoRunSet 410011 410100 $((${NSPILLS}*4501)) 1407 18.2 6.2e3 corsika74003Linux_QGSJET_fluka #N (14)
#DoRunSet 510011 510100 $((${NSPILLS}*3078)) 2412 31.2 9.2e3 corsika74003Linux_QGSJET_fluka #Mg (24)
#DoRunSet 610011 610100 $((${NSPILLS}*1332)) 5626 72.8 6.2e3 corsika74003Linux_QGSJET_fluka #Fe (56)

#FLUKA p Runs with only hadronic LE tracking
#TEMPLATEFILE="keephads_corsika_input_TEMPLATE"
#NSPILLS=5 # number of spills per run
#USAGE_MODEL="OPPORTUNISTIC"
#DoRunSet 700001 701000 $((${NSPILLS}*1000000)) 14 1.3 1.8e4 corsika74003Linux_QGSJET_fluka #p


echo 
echo Submitted $submittedJobs jobs.
