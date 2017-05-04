#!/bin/bash
source grid_runs_inc.sh

tmptar=/tmp/exec.tar

rm $outtar $tmptar

#create tar and add sqShowers.py
cd $rundir
tar cvf $tmptar sqShowers.py

#add corsikaConverter
cd $pathtocorsikaconverter
tar rvf $tmptar corsikaConverter

#add corsika run directory contents (top level only) and fluka directory
cd $corsikarundir
ls -l | grep '^[^d]' | awk '{print $9}' | xargs tar rvf $tmptar
tar rvf $tmptar fluka/

#gzip the thing, but keep the tar extension because that's what jobsub wants I think
gzip $tmptar
mv ${tmptar}.gz $outtar

