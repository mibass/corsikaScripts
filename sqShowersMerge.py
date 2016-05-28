#!/usr/bin/env python
#script to copy all showers output (from corsikaConverter) into sqlite3 db
import os,sys,string
import ROOT
from math import *
from ROOT import TTree, TH1F, TCanvas, gROOT, TGaxis, gStyle, TColor, TLegend, THStack, TChain
from ROOT import *
from array import array
import sqlite3
import argparse
sys.path.insert(0, '/uboone/app/users/mibass/cosmics/MuCS/common/')
from flatttree import *


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-b', '--batch', help="batch mode for root", action='store_true' )
  parser.add_argument('filelist', help="File containing list of sqShowers outputs to process.")
  parser.add_argument('outputdb', help="Output db file to create.")
  parser.add_argument('outputroot', help="Output root file to create.")
  args = parser.parse_args()

  print "Creating output root file",args.outputroot
  tfout=TFile(args.outputroot, "recreate")
  particlestree=flatttree("Particles",["shower/I","pdg/I","px/F","py/F","pz/F","x/F","z/F","t/F","e/F"])
  
  print "Opening input db file list",args.filelist
  dbfiles = [line.strip() for line in open(args.filelist, 'r')]
  print "Found %d input db files"%len(dbfiles)
  
  #create sqlite db
  print "Creating database",args.outputdb
  conn = sqlite3.connect(args.outputdb)
  c=conn.cursor()
  c.execute('''CREATE TABLE input (runnr int, version float, nshow int, nshowsim int, model_high int, model_low int, eslope float, erange_high float, erange_low float, ecuts_hadron float, ecuts_muon float, ecuts_electron float, ecuts_photon float)''')
  c.execute('''CREATE TABLE showers (id int primary key, nparticles int)''')
  c.execute('''CREATE TABLE particles (shower int, pdg int, px float, py float, pz float, x float, z float, t float, e float)''')

  totalshowers=1
  inputfilled=False
  for thisdb in dbfiles:
    print "Opening db file: %s"%thisdb
    showeroffset=totalshowers
    tconn=sqlite3.connect(thisdb)
    tconn.row_factory = sqlite3.Row #use dictionaries
    tc=tconn.cursor()
    tc.row_factory = sqlite3.Row
    if not inputfilled:
      tc.execute("select * from input;")
      rinput=tc.fetchall()
      print rinput
      i=rinput[0]
      c.execute("INSERT INTO input(runnr,version,nshow,nshowsim,model_high,model_low,eslope,erange_high,erange_low,ecuts_hadron, ecuts_muon, ecuts_electron, ecuts_photon) VALUES (%d,%f,%d,%d,%d,%d,%f,%f,%f,%f,%f,%f,%f)" % (i['runnr'], i['version'], i['nshow'], i['nshow'], i['model_high'], i['model_low'], i['eslope'], i['erange_high'], i['erange_low'], i['ecuts_hadron'], i['ecuts_muon'], i['ecuts_electron'], i['ecuts_photon']))
      inputfilled=True
    
    tc.execute("select * from showers;")
    rshowers=tc.fetchall()
    for shower in rshowers:
      print "\tInserting shower %d"%(showeroffset+shower['id'])
      c.execute("INSERT INTO showers(id,nparticles) VALUES (%d,%d)"%(shower['id']+showeroffset,shower['nparticles']))
      tc.execute("select * from particles where shower=%d;"%shower['id'])
      rparticles=tc.fetchall()
      for p in rparticles:
        fields=(p['shower']+showeroffset, p['pdg'],p['px'],p['py'],p['pz'],p['x'],p['z'],p['t'],p['e'])
        c.execute("INSERT INTO particles VALUES (%d,%d,%f,%f,%f,%f,%f,%f,%f)"%fields)
        particlestree.fill(fields)
        
      totalshowers+=1
    
    tconn.close()
  
    print "\tTotal showers added to db:",totalshowers    
   
       
  #update the number of showers to be the total in the input table
  c.execute("UPDATE input SET nshow=%d,nshowsim=%d"%(totalshowers,totalshowers))
  conn.commit()
  c.execute("VACUUM")
  conn.close()
  
  particlestree.close(tfout)
  tfout.Close()

if __name__ == "__main__":
    main()
    

