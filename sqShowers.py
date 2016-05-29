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

#adapated from corsika converter
def corsikaToHepevtID(corsikaID):			
		return {1:  22,			# gamma
		2:	  -11,		# e+
		3:	 11,			# e-
		5:  -13,			# mu+
		6:  13,			# mu-
		7:  111,			# pi0
		8:	 211,			# pi+
		9:  -211,		# pi-
		10:  130,		# K0_L
		11:  321,		# K+
		12:  -321,		# K-
		13:  2112,		# n
		14:  2212,		# p
		15:  -2212,		# pbar
		16:  310,		# K0_S
		17:  221,		# eta
		18:  3122,		# Lambda
		19:  3222,		# Sigma+
		20:  3212,		# Sigma0
		21:  3112,		# Sigma-
		22:  3322,		# Cascade0
		23:  3312,		# Cascade-
		24:  3334,		# Omega-
		25:  -2112,		# nbar
		26:  -3122,		# Lambdabar
		27:  -3112,		# Sigma-bar
		28:  -3212,		# Sigma0bar
		29:  -3222,		# Sigma+bar
		30:  -3322,		# Cascade0bar
		31:  -3312,		# Cascade+bar
		32:  -3334,		# Omega+bar
			
		50:  223,		# omega
		51:  113,		# rho0
		52:  213,		# rho+
		53:  -213,		# rho-
		54:  2224,		# Delta++
		55:  2214,		# Delta+
		56:  2114,		# Delta0
		57:  1114,		# Delta-
		58:  -2224,		# Delta--bar
		59:  -2214,		# Delta-bar
		60:  -2114,		# Delta0bar
		61:  -1114,		# Delta+bar
		62:  10311,		# K*0
		63:  10321,		# K*+
		64:  -10321,		# K*-
		65:  -10311,		# K*0bar
		66:  12,			# nu_e
		67:  -12,		# nu_ebar
		68:  14,			# nu_mu
		69:  -14,		# nu_mubar
			
		116:  421,		# D0
		117:  411,		# D+
		118:  -411,		# D-bar
		119:  -421,		# D0bar
		120:  431,		# D+_s
		121:  -431,		# D-_sbar
		122:  441,		# eta_c
		123:  423,		# D*0
		124:  413,		# D*+
		125:  -413,		# D*-bar
		126:  -423,		# D*0bar
		127:  433,		# D*+_s
		128:  -433,		# D*-_s
			
		130:  443,		# J/Psi
		131:  -15,		# tau+
		132:  15,		# tau-
		133:  16,		# nu_tau
		134:  -16,		# nu_taubar
			
		137:  4122,		# Lambda+_c
		138:  4232,		# Cascade+_c
		139:  4132,		# Cascade0_c
		140:  4222,		# Sigma++_c
		141:  4212,		# Sigma+_c
		142:  4112,		# Sigma0_c
		143:  4322,		# Cascade'+_c
		144:  4312,		# Cascade'0_c
		145:  4332,		# Omega0_c
		149:  -4122,		# Lambda-_cbar
		150:  -4232,		# Cascade-_cbar
		151:  -4132,		# Cascade0_cbar
		152:  -4222,		# Sigma--_cbar
		153:  -4212,		# Sigma-_cbar
		154:  -4112,		# Sigma0_cbar
		155:  -4322,		# Cascade'-_cbar
		156:  -4312,		# Cascade'0_cbar
		157:  -4332,		# Omega0_cbar
		161:  4224,		# Sigma*++_c
		162:  1214,		# Sigma*+_c
		163:  4114,		# Sigma*0_c
			
		171:  -4224,		# Sigma*--_cbar
		172:  -1214,		# Sigma*-_cbar
		173:  -4114,		# Sigma*0_cbar
		176:  511,		# B0
		177:  521,		# B+
		178:  -521,		# B-bar
		179:  -511,		# B0bar
		180:  531,		# B0_s
		181:  -531,		# B0_sbar
		182:  541,		# B+_c
		183:  -541,		# B-_cbar
		184:  5122,		# Lambda0_b
		185:  5112,		# Sigma-_b
		186:  5222,		# Sigma+_b
		187:  5232,		# Cascade0_b
		188:  5132,		# Cascade-_b
		189:  5332,		# Omega-_b
		190:  -5112,		# Lambda0_bbar
		191:  -5222,		# Sigma+_bbar
		192:  -5112,		# Sigma-_bbar
		193:  -5232,		# Cascade0_bbar
		194:  -5132,		# Cascade+_bbar
		195:  -5332		# Omega+_bbar
	}[corsikaID]
	
def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-b', '--batch', help="batch mode for root", action='store_true' )
  parser.add_argument('-o', '--onlyPopulated', help="only keep populated showers", action='store_true', default=False )
  parser.add_argument('-p', '--particleids', help="Comma separated list of corsika particle IDs to keep (empty=all).", default="" )
  parser.add_argument('filelist', help="File containing list of corsikeConverter showers outputs to process.")
  parser.add_argument('outputdb', help="Output db file to create.")
  args = parser.parse_args()
  if args.particleids!="":
    plist=tuple(int(x) for x in args.particleids.split(','))
  else:
    plist=tuple()
    
  #file='/uboone/data/users/mibass/corsika/ShowerInputTest/DAT020021_showers.root' #adds 10MeV cut
  files=data = [line.strip() for line in open(args.filelist, 'r')]
  f0 = TFile( files[0], 'r' )
  Inputs=f0.Get('Input')
  Showers=f0.Get('Events')
  Particles=f0.Get('Particles')
  print Showers.GetEntries(),"entries in shower tree"
  print Particles.GetEntries(),"entries in particles tree"
  print Inputs.GetEntries(),"entries in Inputs tree"

  #create sqlite db
  print "Creating database",args.outputdb
  conn = sqlite3.connect(args.outputdb)
  c=conn.cursor()
  c.execute('''CREATE TABLE input (runnr int, version float, nshow int, nshowsim int, model_high int, model_low int, eslope float, erange_high float, erange_low float, ecuts_hadron float, ecuts_muon float, ecuts_electron float, ecuts_photon float)''')
  c.execute('''CREATE TABLE showers (id int primary key, nparticles int)''')
  c.execute('''CREATE TABLE particles (shower int, pdg int, px float, py float, pz float, x float, z float, t float, e float)''')


  if len(plist):
    print "Will only keep particle ids:",plist

  if args.onlyPopulated:
    print "Will only store populated showers"

  Inputs.GetEntry(0)
  c.execute("INSERT INTO input(runnr,version,nshow,nshowsim,model_high,model_low,eslope,erange_high,erange_low,ecuts_hadron, ecuts_muon, ecuts_electron, ecuts_photon) VALUES (%d,%f,%d,%d,%d,%d,%f,%f,%f,%f,%f,%f,%f)" % (Inputs.RUNNR,Inputs.Version,Inputs.NSHOW,Inputs.NSHOW,Inputs.Model_High,Inputs.Model_Low,Inputs.ESLOPE, Inputs.ERANGE_High,Inputs.ERANGE_Low,Inputs.ECUTS_Hadron,Inputs.ECUTS_Muon,Inputs.ECUTS_Electron, Inputs.ECUTS_Photon))

  nshowers=Events.GetEntries()
  totalshowers=0
  f0.Close()

  for thisfile in files:
    f = TFile( thisfile, 'r' )
    Inputs=f.Get('Input')
    Showers=f.Get('Events')
    Particles=f.Get('Particles')
    print "open shower root file:",thisfile
    
    for i in xrange(Particles.GetEntries()):
      if totalshowers%100000: print "Processing %d ...\r"%i,
      nb = Particles.GetEntry(i)
      if nb<=0:
        continue
      np=0
      for j in xrange(len(Particles.ParticleID)):
        if Particles.ParticleID[j]==0:
          break
        else:
          if len(plist)==0 or Particles.ParticleID[j] in plist: np+=1
      
      if args.onlyPopulated and np==0: continue  
      c.execute("INSERT INTO showers(id,nparticles) VALUES (%d,%d)"%(totalshowers,np))
      
      for j in xrange(len(Particles.ParticleID)):
        if Particles.ParticleID[j]==0:
          break
        else:
          if len(plist)==0 or Particles.ParticleID[j] in plist:
            p=Particles
            c.execute("INSERT INTO particles VALUES (%d,%d,%f,%f,%f,%f,%f,%f,%f)"%(totalshowers, corsikaToHepevtID(p.ParticleID[j]),p.ParticlePx[j],p.ParticlePy[j],p.ParticlePz[j],p.ParticleX[j],p.ParticleZ[j],p.ParticleTime[j],p.ParticleEnergy[j]))

      totalshowers=totalshowers+1
      
    
    print "Total showers added to db:",totalshowers    
   
   
    conn.commit()
    f.Close()
  #update the number of showers to be the total in the input table
  c.execute("UPDATE input SET nshow=%d"%totalshowers)
  conn.commit()
  c.execute("VACUUM")

  conn.close()


if __name__ == "__main__":
    main()
    

