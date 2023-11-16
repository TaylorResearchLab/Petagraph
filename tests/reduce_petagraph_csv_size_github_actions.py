#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
#import polars as pl
import pandas as pd
#import glob as glob
#from collections import Counter
#import matplotlib.pyplot as plt

import sys
import warnings
warnings.filterwarnings('ignore')
# In[2]:


#path='/Users/stearb/Desktop/DESKTOP_TRANSFER/R03_local/Petagraph_Sept2023/data/base_csvs/basecontext10Sep2023/'
path='/var/lib/neo4j/import/'

cuicodes = pd.read_csv(path+'CUI-CODEs.csv')

dropsabs = ['HSCLO','MSH','MEDCIN','LNC','MTH','NDC','ICD10PCS','MTHSPL','REFSEQ','RXNORM','ICD10CM','ICPC2ICD10ENG','MDR',
'MMSL','UWDA','CHV','CPT','SNOMEDCT_VET','GS','ORPHANET','NDDF','VANDF','UMD','MMX','ICD10AM','ICD9CM',
'HCPT','MTHICD9','PDQ','CSP','NIC','LCH_NW','ICD10','NOC','DRUGBANK']


# ## Reduce CUICODEs.csv 


cuicodes['sabs'] = [i.split(':')[0] for i in cuicodes[':END_ID']]
cuicodes_reduced = cuicodes[~cuicodes['sabs'].isin(dropsabs)].reset_index(drop=True)
print('CUI-CODEs.csv reduced by '+str(np.round(100*(len(cuicodes_reduced)/len(cuicodes))))+'%')

cuicodes_reduced.to_csv('/var/lib/neo4j/import/CUI-CODEs.csv',index=False)

del cuicodes

sys.exit()
'''
print('HEREEEEEEEE')
codes = pd.read_csv(path+'CODEs.csv')
codes_reduced = codes[codes['SAB'].isin(cuicodes_reduced['sabs'].values)]

print('CODEs.csv reduced by '+str(np.round(100*(len(codes_reduced)/len(codes))))+'%')

del codes
print('HEREEEEEEEE')
codes_reduced.drop(['CODE','value:float','lowerbound:float','upperbound:float','unit'],axis=1,inplace=True)

codes_reduced.to_csv('/var/lib/neo4j/import/CODEs.csv',index=False)

del codes_reduced

print('------------------------------')
# ## Drop CUIs in the CUI-CODEs df from CUIs.csv and CUI-CUIs.csv file

# In[8]:


cuicodes_reduced.drop('sabs',axis=1,inplace=True)
'''

# In[9]:


cuis = pd.read_csv(path+'CUIs.csv')

cuis_reduced = cuis[cuis['CUI:ID'].isin(cuicodes_reduced[':START_ID'].values)].reset_index(drop=True)

print('CUIs.csv reduced by '+str(np.round(100*(len(cuis_reduced)/len(cuis))))+'%')

del cuis

cuis_reduced.to_csv('/var/lib/neo4j/import/CUIs.csv',index=False)

del cuis_reduced


# # CUI-CUIs

cuicuis = pd.read_csv(path+'CUI-CUIs.csv')

# DROP CUIs from START_ID and END_ID cols
cuicuis_reduced = cuicuis[cuicuis[':START_ID'].isin(cuicodes_reduced[':START_ID'].values)]

cuicuis_reduced = cuicuis_reduced[cuicuis_reduced[':END_ID'].isin(cuicodes_reduced[':START_ID'].values)]

del cuicuis
#print('CUI-CUIs.csv reduced by '+str(np.round(100*(len(cuicuis_reduced)/len(cuicuis))))+'%')

cuicuis_reduced.drop('evidence_class:string',axis=1,inplace=True)

cuis_reduced.to_csv('/var/lib/neo4j/import/CUI-CUIs.csv',index=False)

del cuicuis_reduced





