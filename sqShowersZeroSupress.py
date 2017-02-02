#!/usr/bin/env python
#script to copy all showers output (from corsikaConverter) into sqlite3 db
import os,sys,string
from math import *
from array import array
import sqlite3
import argparse


def querySingleValue(qry,tc):
  tc.execute(qry)
  return tc.fetchall()[0][0]

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('filelist', help="File containing list of sqShowers outputs to process.")
  args = parser.parse_args()

  print "Opening input db file list",args.filelist
  dbfiles = [line.strip() for line in open(args.filelist, 'r')]
  print "Found %d input db files"%len(dbfiles)
  

  totalshowers=1
  inputfilled=False
  for thisdb in dbfiles:
    print "Opening db file: %s, "%thisdb,
    showeroffset=totalshowers
    tconn=sqlite3.connect(thisdb)
    tconn.row_factory = sqlite3.Row #use dictionaries
    tc=tconn.cursor()
    tc.row_factory = sqlite3.Row
    
    nGTZero=querySingleValue("select count(*) from showers where nparticles>0;",tc)
    nZero=querySingleValue("select count(*) from showers where nparticles=0;",tc)
    
    print "%d, %d, %f" % ( nGTZero, nZero, float(nGTZero)/(nZero+nGTZero))
    
    tconn.execute("delete from showers where nparticles=0");
    tconn.commit()
    tconn.close()
     
       

if __name__ == "__main__":
    main()
    

