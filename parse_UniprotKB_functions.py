# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:33:11 2022

@author: hbckleikamp
"""

import gzip


#First, Download these from uniprotKB FTP (requires at least 150 GB of space. Do not unzip, the scripts reads them in compressed state)
#https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.dat.gz
#https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_trembl.dat.gz

files=["path/to/uniprot_sprot.dat.gz",        #path to uniprot_sprot.dat
       "path/to/uniprot_trembl.dat.gz"]       #path to uniprot_trembl.dat

parsed=[]
counter=0
batch=0


with open("UniprotKB_functions.tsv","w") as w:
    
    #write columns
    w.write("\t".join(["Accession","Name","Taxid","KEGG","EC","GO","InterPro","Pfam"])+"\n")
    
    for file in files:
        with gzip.open(file,'r') as f:
            
            #initialize lists
            ACC=""  # accession
            NAME="" 
            OX=""   # organism_ID
            KEGG=[] 
            EC=[]
            GO=[]
            InterPro=[]
            PFAM=[]
        
            
            for ix,line in enumerate(f): 
                
                s=str(line)[2:]
                if s.startswith("AC   "): #triple space
                    
                    counter+=1 #for chekcing progress
                    batch+=1   #for writing in batches, which reduces RAM
                    print(counter)

                    #append first then define then re-initialize
                    
                    
                    parsed.append([ACC,
                                   NAME,
                                   OX,
                                   ", ".join(KEGG),
                                   ", ".join(EC),
                                   ", ".join(GO),
                                   ", ".join(InterPro),
                                   ", ".join(PFAM)])
                    
                    
                    #re-initialize lists
                    ACC=s.split("AC   ")[1].split(";")[0]
                    NAME=""
                    OX=""   #organism_ID
                    KEGG=[] 
                    EC=[]
                    GO=[]
                    InterPro=[]
                    PFAM=[]
                 
                    #batched write
                    if batch>10000:
                        #write tab delimited
                        w.write("\n".join(["\t".join(p) for p in parsed])+"\n")
      
                        #reset
                        batch=0
                        parsed=[]
        
        
            
                if s.startswith("OX   NCBI_TaxID="): 
                    OX=s.split("OX   NCBI_TaxID=")[1].split(";")[0]   
                if s.startswith("DE   RecName: Full="): 
                    NAME=s.split("DE   RecName: Full=")[1].split(";")[0]    
                    
                if "EC=" in s:
                    EC.append(s.split("EC=")[1].split()[0].split(";")[0])
                
                if s.startswith("DR   KEGG; "):
                    KEGG.append(s.split("DR   KEGG; ")[1].split("\\n")[0])
                if s.startswith("DR   GO; "):   
                    GO.append(s.split("DR   GO; ")[1].split("\\n")[0])
                if s.startswith("DR   InterPro; "):   
                    InterPro.append(s.split("DR   InterPro; ")[1].split("\\n")[0])
                if s.startswith("DR   Pfam; "): 
                    PFAM.append(s.split("DR   Pfam; ")[1].split("\\n")[0])
                    
                    
                    
    #write remainder
    w.write("\n".join(["\t".join(p) for p in parsed])+"\n")  
    

        
        

        
