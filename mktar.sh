#!/bin/bash
source grid_runs_inc.sh

outtar=$rundir/exec.tar

rm $outtar

#create tar and add sqShowers.py
cd $rundir
tar cvf $outtar sqShowers.py

#add corsikaConverter
cd $pathtocorsikaconverter
tar rvf $outtar corsikaConverter

#add corsika run directory contents (top level only) and fluka directory
cd $corsikarundir
ls -l | grep '^[^d]' | awk '{print $9}' | xargs tar rvf $outtar
tar rvf $outtar fluka/

#gzip the thing, but keep the tar extension because that's what jobsub wants I think
gzip $outtar
mv ${outtar}.gz $outtar

