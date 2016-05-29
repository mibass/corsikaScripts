#!/bin/bash


#$1 is input card file
#$2 is the name of the corsika output dat file
#$3 is the K parameter to be passed to corsikaConverter
#$4 is the executable name to use
#$5 is the scratch directory full path
source /grid/fermiapp/products/common/etc/setups.sh
source /grid/fermiapp/products/uboone/setup_uboone.sh
source /cvmfs/oasis.opensciencegrid.org/fermilab/products/common/etc/setup
setup larsoft v05_10_00 -q e9:prof

SCRATCH_DIR=${5}/
cd $_CONDOR_SCRATCH_DIR

#for log file
pwd
ls

#arrange input files
#unpack tar file containing executables
echo "unpacking tar file..." 
tar xzvf $CONDOR_DIR_INPUT/exec.tar
#cp coriska input card into current dir
cp $CONDOR_DIR_INPUT/$1 ./

#make sure dat file doesn't already exist, otherwise CORSIKA won't run
rm $2

#setup path to fluka
export FLUPRO=$_CONDOR_SCRATCH_DIR/fluka

#run corsika & corsikaConverter
./${4} < $1 > ${2}_corsikaOutput 2> ${2}_corsikaOutput
./corsikaConverter $3 $2 > ${2}_converterOutput 2> ${2}_converterOutput
echo ${2}_showers.root >flist.txt
python sqShowers.py flist.txt ${2}.db

#for log file
ls -alh
echo FLUPRO=$FLUPRO 
ls -alh $FLUPRO

#copy needed output files back to scratch dir
ifdh cp -D ${2}_corsikaOutput ${2}_converterOutput ${2}_showers.root ${2}.db $SCRATCH_DIR
#ifdh cp fluka11.out $SCRATCH_DIR/${2}_fluka11.out #this could be useful to trouble shoot fluka issues

