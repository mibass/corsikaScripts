#!/bin/bash

#Paths
SCRATCH_DIR=/pnfs/uboone/scratch/users/mibass/corsika #path where outputs will be stored
outdir=/uboone/data/users/mibass/corsika/runs #path where generated dag files are stored
rundir=/uboone/app/users/mibass/corsika/corsikaScripts #path to corsikaScripts
pathtocorsikaconverter=/uboone/app/users/mibass/corsika/corsikaConverter #path to corsikaConverter
corsikarundir=/uboone/app/users/mibass/corsika-74003/run #path to corsika's run directory

TEMPLATEFILE="corsika_input_TEMPLATE"
USAGE_MODEL="DEDICATED,OPPORTUNISTIC"

submittedJobs=0
seedIncrement=0 #number to increment random seed by, should be large to avoid overlapping with previous jobs during makeup, THIS SHOULD NOT BE USED UNLESS YOU KNOW WHAT IT IS DOING

pathtotar=${rundir}/exec.tar
runscript=${rundir}/grid_runOne.sh
outputStringTemplate=$SCRATCH_DIR/DAT%s_spills.root
cfgsdir=${rundir}/cfgs/

DAGHeader () {
  echo "<parallel>" > $1
}

DAGFooter () {
  echo "</parallel>" >> $1
}

DoARun () {
  outdagfile=$9
  seed1=$(expr $3 + $seedIncrement)
  seed2=$(expr $4 + $seedIncrement)
  
  sed -e "s/_RUNNR_/$5/" -e "s/_NSHOW_/$1/" -e "s/_PRMPAR_/$2/" -e "s/_SEED1_/$seed1/" -e "s/_SEED2_/$seed2/" -e "s/_ERANGELOW_/$6/" $TEMPLATEFILE > ${cfgsdir}/tempconf$5
  printf -v datfile "DAT%06d" $5
  
  echo jobsub -n -G uboone --OS=SL5,SL6 --resource-provides=usage_model=$USAGE_MODEL -f ${cfgsdir}/tempconf$5 -f ${pathtotar} file://${runscript} tempconf$5 $datfile $7 $8 $SCRATCH_DIR >> $outdagfile
  (( submittedJobs++ ))
}

DoRunSet () {
  #$1 = start number
  #$2 = end number
  #$the rest are parameters to DoARun
  outputfilename=""
  dagoutputfile=$outdir/Runs_$1_$2.dag
  echo "making dag file $dagoutputfile"
  
  DAGHeader $dagoutputfile
  
  #makeup missing files, only run if the output file doesn't exist
  for i in `seq $1 $2`; do
    printf -v outputfilename $outputStringTemplate $i
    if [ ! -f $outputfilename ]; then
      echo "*******Running $i"
      DoARun $3 $4 $i 100$i $i $5 $6 $7 $dagoutputfile
    fi
  done

  DAGFooter $dagoutputfile
  echo "wrote dag file $dagoutputfile"
  jobsub_submit_dag -G uboone file://$dagoutputfile
}


