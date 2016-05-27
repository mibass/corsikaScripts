#!/bin/bash
source grid_runs_inc.sh

outtar=$rundir/exec.tar
rm $outtar
mkdir /tmp/exectar
cd /tmp/exectar
cp ${pathtocorsikaconverter}/corsikaConverter ./
cp ${rundir}/sqShowers.py ./
tar cvf $outtar sqShowers.py corsikaConverter

cd $corsikarundir
ls -l | grep '^[^d]' | awk '{print $9}' | xargs tar cvf $outtar
tar rvf $outtar fluka/
gzip $outtar
mv ${outtar}.gz $outtar
