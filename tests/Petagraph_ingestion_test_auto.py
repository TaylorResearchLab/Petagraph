#!/usr/bin/env python
# coding: utf-8

# # Petagraph ingestion tests

# ### This is a copy of the umls_ingestion_test_queries-auto.ipynb notebook, which was written for the Data Distillery graph. I removed dataset tests if the dataset isnt in Petagraph.

'''
author: @benstear
Date Created: 11/8/23
'''

import sys
import neo4j
from itertools import repeat
import pandas as pd
#import polars as pl
import numpy as np
from collections import Counter
from neo4j import GraphDatabase, basic_auth
#import argparse
import logging
logging.basicConfig(level=logging.DEBUG, filename="logfile.txt", filemode="a+",format='%(message)s')
logging.getLogger("neo4j").setLevel(logging.WARNING)



#uri='neo4j://example.com:7687'
#uri='bolt://localhost:7687'
uri='http://localhost:7474/'
user='neo4j'
#password='neo4j2020'
password='neo4j'
#password=args.NEO4J_PASSWORD


driver = GraphDatabase.driver(uri, auth=(user, password))


#pw_query='''ALTER CURRENT USER SET PASSWORD FROM "neo4j" TO "neo4j2020"'''
#with driver.session(default_access_mode=neo4j.WRITE_ACCESS) as session:
#        result = session.run(pw_query)

with driver.session(default_access_mode=neo4j.READ_ACCESS) as session:
        result = session.run('MATCH (n:Code) RETURN count(N); ')
        print(result)

def get_nodes(path: str):
    nodes_df = pd.read_csv(path+'/OWLNETS_node_metadata.txt',sep='\t')
    
    nodes_df['node_id'] = [i.replace('PUBCHEM_CID','PUBCHEM') for i in nodes_df['node_id']]
    nodes_df['node_id'] = [i.replace('HPO HP','HPO') for i in nodes_df['node_id']]
    nodes_df['node_id'] = [i.replace('HGNC HGNC','HGNC') for i in nodes_df['node_id']]
    nodes_df['node_id'] = [i.replace('EFO EFO','EFO') for i in nodes_df['node_id']]
    
    return nodes_df

def get_edges(path: str):
    # remove all '/' here
    df = pd.read_csv(path+'/OWLNETS_edgelist.txt',sep='\t')
    
    if 'evidence_class' in df.columns:
        df.drop('evidence_class',axis=1,inplace=True)
    return df

def get_sab_counts(nodes: pd.DataFrame()) -> dict():
    # must drop duplicates in the node_id column here before we count because 
    # we dont want to count the same node_id twice. It will only be in the graph once.
    # It can be in the nodes file more than once, ie if there are multiple terms for a single code
    
    nodes = nodes.drop_duplicates()
    nodes = nodes.to_frame()

    nodes_colon = pd.DataFrame([i for i in nodes['node_id'] if ':' in i ],columns=['node_id'])
    nodes_space = pd.DataFrame([i for i in nodes['node_id'] if ' ' in i ],columns=['node_id'])
    
    nodes_colon = pd.DataFrame([i[0] for i in nodes_colon['node_id'].str.split(':')],columns=['node_id'])
    nodes_space = pd.DataFrame([i[0] for i in nodes_space['node_id'].str.split(' ')],columns=['node_id'])
    
    nodes = pd.concat([nodes_colon,nodes_space])
    
    return dict(Counter(nodes['node_id'].values))

def make_node_counts(SAB: str,path: str) -> pd.DataFrame():
    en = get_nodes(path)['node_id']
    node_counts = get_sab_counts(en)

    ndf =  pd.DataFrame(node_counts.items(),columns=['sab','nodes_files_count'])\
                                                .sort_values('nodes_files_count',ascending=False)\
                                                .reset_index(drop=True)
    ndf['sab'] = [i.upper()  for i in ndf['sab']]
    
    return ndf


def make_edge_counts(SAB: str, path: str) -> pd.DataFrame():
    e = get_edges(path)
    
    for col in e.columns:
        # MAKE fix_slashes() work w/o sets, so it presrves order so we can call it here too!!!!!!!!
        e[col]  = fix_slashes(SAB, e[col] )
        #e[col] = [s.split('/')[-1] if '/' in s else s for s in e[col]]
        
        if col in ['subject','object']:
            e[col]  = [s.split('_')[0] if 'UBERON_' in s or 'CLO_' in s or 'EFO_' in s \
                             or 'L_' in s or 'BTO_' in s else s for s in e[col]]
            
    e['subject_sab'] = [i.split(' ')[0] for i in e['subject']]
    e['object_sab'] = [i.split(' ')[0] for i in e['object']]
    
    e['subject_sab'] = [i.replace('PUBCHEM_CID','PUBCHEM') for i in e['subject_sab']]
    e['object_sab'] = [i.replace('PUBCHEM_CID','PUBCHEM') for i in e['object_sab']]
    
    e['predicate'] = [i.replace(':','_') for i in e['predicate']]
    
    col_counts = e.groupby(['subject_sab','predicate','object_sab']).size().reset_index().rename(columns={0:'edges_files_count'})
    col_counts_df = col_counts.sort_values('edges_files_count',ascending=False).reset_index(drop=True)
    
    col_counts_df['predicate'] = [ro_id_lbl_map[i] if 'RO_' in i or 'BFO_' in i else i for i in col_counts_df['predicate']]
    col_counts_df['predicate'] = [i.replace(' ','_') for i in col_counts_df['predicate'] ]
    
    col_counts_df['predicate'] = [i.replace('rdf-schema_member','member') for i in col_counts_df['predicate']]
    col_counts_df['predicate'] = [i.replace('rdf-schema_subClassOf','isa') for i in col_counts_df['predicate']]
    col_counts_df['predicate'] = [i.replace('faldo_','') for i in col_counts_df['predicate']]  
    col_counts_df = col_counts_df.sort_values('object_sab')
    col_counts_df['subject_sab'] = [i.upper() for i in col_counts_df['subject_sab']]
    col_counts_df['object_sab'] = [i.upper() for i in col_counts_df['object_sab']]
    
    return col_counts_df


# # fix_slashes w/o sets and use the ro.json file

# In[9]:


#import ssl
#ctx = ssl.create_default_context(capath="/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages/certifi")

import os
#os.environ["SSL_CERT_DIR"] = "/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages/certifi"
#os.environ["SSL_CERT_FILE"] = "/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages/certifi/cacert.pem"

dfro = pd.read_json("https://raw.githubusercontent.com/oborel/obo-relations/master/ro.json")

# Information on relationship properties (i.e., relationship property nodes) is in the node array.
dfnodes = pd.DataFrame(dfro.graphs[0]['nodes'])

# Information on edges (i.e., relationships between relationship properties) is in the edges array.
dfedges = pd.DataFrame(dfro.graphs[0]['edges'])

dfnodes['id'] = [i[-1] for i in dfnodes['id'].str.split('/')]
ro_id_lbl_map = dict(zip(dfnodes['id'],dfnodes['lbl']))


def compute_code_subsets(SAB: str, sab_counts_df: pd.DataFrame(), path: str) -> pd.DataFrame():
    '''
    Helper function for the query_nodes() function. This function is called when there are more codes in
    the graph than there are in the nodes.tsv file for a specific SAB. This fuction checks that the codes in
    the nodes.tsv file are a subset of the codes in the graph (for a specific SAB).
    sab_counts_df: Output of the query_nodes() function. It gets passed to this function, updated w/ subset data
    and returnedto the query_nodes() function.
    '''
    test_subsets_df = sab_counts_df[sab_counts_df['ratio']>1] # test these rows
    rest_of_df =  sab_counts_df[sab_counts_df['ratio']<=1]  # dont need to test these rows. concat at the end.

    if len(test_subsets_df) > 0:
        code_id_set = fix_slashes(SAB,list(set(get_nodes(path)['node_id']))) 
        
        code_id_set =  [i.replace(':',' ') for i in code_id_set]
        #print(code_id_set)
        graph_sab_codes = []
        nodes_file_sab_codes = [] # for storing sab-specific CODE_IDs from the graph/nodes_file

        with driver.session(default_access_mode=neo4j.WRITE_ACCESS) as session:
            for idx,row in test_subsets_df.iterrows():
                
                result = session.run(qstr_nodes_subset,sab=row[0])
                sc = [ dict(i) for i in result]

                # get list of sab-specific CODE_IDs from graph
                graph_sab_codes.append(set(sc[0]['sab_nodes']))

                # get list of sab-specific CODE_IDs from nodes file
                sab_specific_codes = [i for i in code_id_set if i.startswith(row[0])]

                # get just CODE, we dont need SAB here, and append to list
                nodes_file_sab_codes.append(set([i.split(' ')[-1] for i in sab_specific_codes]))
       
        #test_subsets_df['file_nodes_sets'] = nodes_file_sab_codes
        #test_subsets_df['graph_nodes_sets'] = graph_sab_codes
        test_subsets_df =test_subsets_df.assign(file_nodes_sets=nodes_file_sab_codes,graph_nodes_sets=graph_sab_codes)

        # check if the node file codes are a subset of the graph codes, on a per-sab level
        test_subsets_df['is_subset'] = test_subsets_df.apply(lambda x: x.file_nodes_sets.issubset(x.graph_nodes_sets), axis=1)
        #test_subsets_df['is_subset'] = [True for i in test_subsets_df['is_subset'] if i==1.0 else False]
        test_subsets_df['set_diff'] = test_subsets_df.apply(lambda x:  x.file_nodes_sets.difference(x.graph_nodes_sets), axis=1)
        test_subsets_df['set_diff_len'] = test_subsets_df['set_diff'].apply(len)
        # create code_ids using sab col
        
        sab_code_id_sets = []
        for row in test_subsets_df.itertuples():
            if len(row.set_diff) > 0: sab_code_id_sets.append([row.sab+' '+i for i in row.set_diff])
            else: sab_code_id_sets.append({})
        test_subsets_df['missing_sab_codes'] = sab_code_id_sets    
        #'file_nodes_sets','graph_nodes_sets', 'set_diff' 
        return pd.concat([test_subsets_df,rest_of_df],axis=0)[['sab','nodes_files_count','graph_count',
                                                'is_subset','ratio','set_diff_len','missing_sab_codes'
                                                              ]].reset_index(drop=True).sort_values('ratio',ascending=False)


# In[11]:


# qstr_nodes can be defined outside the function bc we update the sab in the session.run() call
# each time using neo4j's parameter passing convention '$'. The qstr_edges must be inside the for loop and function bc we need 
# to pass a python variable (pred) bc cypher doesnt support passing rel'ship names
# as parameters through session.run()
qstr_nodes = "match (cc:Code {SAB:$sab}) return count(distinct cc) as sab_cnt"
qstr_nodes_subset = "match (cc:Code {SAB:$sab}) return collect(cc.CODE) as sab_nodes"

def query_nodes(SAB: str, sab_counts_df: pd.DataFrame(), path: str) -> pd.DataFrame():
    results_Ls = []    
    # create is_subset and subset-related columns. These column will be populated to test whther rows where 
    # graph_count > nodes_files_count (aka ratio>1) are subsets.
    # 'graph_nodes_sets' will store the CODE_IDs set for each row (aka for each SAB where ratio>1)
    # 'file_nodes_sets' will store the CODE_IDs set for each row (aka for each SAB where ratio>1)
    # is_subset will be boolean depending on if file_nodes_sets is a subset of graph_nodes_sets
    # the 2 sets cols will be dropped before returning the entire df
    sab_counts_df['graph_nodes_sets'] = sab_counts_df['file_nodes_sets'] = sab_counts_df['is_subset'] = np.nan  
    sab_counts_df['missing_sab_codes'] = sab_counts_df['set_diff_len'] = np.nan
    sab_counts_df['set_diff'] = list(repeat({},len(sab_counts_df))) # just make this col an empty set for now
       
    with driver.session(default_access_mode=neo4j.WRITE_ACCESS) as session:
        for idx,row in sab_counts_df.iterrows():
            logging.info(f'\tQuerying {row[0]} Nodes...'); print(f'\tQuerying {row[0]} Nodes...',end='')
            result = session.run(qstr_nodes,sab=row[0]); sc = [ dict(i) for i in result]
            results_Ls.append(sc[0]['sab_cnt'])
            
            score_for_log = np.round(sc[0]['sab_cnt']/row['nodes_files_count'],2)
            
            print(f'\t[{score_for_log}]\n'); logging.info(f'\t[{score_for_log}]\n')
            
        sab_counts_df['graph_count'] = results_Ls
        sab_counts_df['ratio'] = (sab_counts_df['graph_count']/sab_counts_df['nodes_files_count']).round(2)
        
        # if the ratio > 1 this means that there are more nodes in the graph than in our nodes file for that SAB.
        # This most likely means that another data source has been ingested that uses the same nodes 
        # and that they are already in the graph, plus how ever many more this earlier data source uses.
        # We want to make sure that the list of nodes in the nodes file is a subset of the group of nodes
        # in the graph. Because its possible that there are more nodes of a certain SAB in the graph
        # than there are in our file, but that there are still nodes in the nodes file that arent in the graph.
        subset_df = sab_counts_df[sab_counts_df['ratio']>1]
        
        if len(subset_df):
            #print(f'testing {len(subset_df)} code subsets.....')
            logging.info(f'(Testing {len(subset_df)} code subsets for {SAB} dataset...)')
            return compute_code_subsets(SAB,sab_counts_df,path).reset_index(drop=True)
         
        return sab_counts_df.reset_index(drop=True) # just return the df if theres no need to split and test for subsets.

    
    
def query_edges(SAB: str, col_counts_df: pd.DataFrame()) -> pd.DataFrame():
    '''
    col_counts_df:  A pandas dataframe containing unique subject_sab,predicate,object_sab triples,
                    along with a 4th column called counts representing how many times this triple
                    occurs in the edges.tsv file. 
    '''
    # list to store counts of subject_sab, predicate, object_sab triples in the graph
    results_Ls = []     
    
    with driver.session(default_access_mode=neo4j.WRITE_ACCESS) as session:
        for idx,row in col_counts_df.iterrows():
            
            # get the subject, object and predicate for the current row 
            subject_sab, predicate, object_sab = row[0], row[1], row[2]
            subject_sab = 'PUBCHEM' if subject_sab == 'PUBCHEM_CID' else subject_sab # fix PUBCHEM edgecase
            object_sab = 'PUBCHEM' if object_sab == 'PUBCHEM_CID' else object_sab # fix PUBCHEM edgecase

            print(f'QUERYING TRIPLE: ({subject_sab}) --- ({predicate} {{SAB:{SAB}}}) --- ({object_sab})',end='')
            # use cyphers wildcard symbol, {$}, to pass the parameters (subject_sab, predicate, object_sab)
            # for some reason cypher doesnt support passing relationship names as parameters
            # through the session.run() interface so just pass the predicate using f-string notation
            # Note parameters must be defined in session.run()
            
            qstr_edges = f"match (cc:Code {{SAB:$subject_sab}})-[x:CODE]-(c:Concept)-[b:{predicate} {{SAB:'{SAB}'}}]->(z:Concept)-[r:CODE]-(co:Code {{SAB:$object_sab}}) return count(b) as edge_cnt"
            logging.info(f'QUERYING TRIPLE: ({subject_sab}) --- ({predicate} {{SAB:{SAB}}}) --- ({object_sab})')
            
            # compute score here so we can log/print scores for each triple queried
            # we do the same thing below, its just column wise to save as a new col in the col_counts_df.

            # query graph and append edge_count results
            result = session.run(qstr_edges,subject_sab=subject_sab,object_sab=object_sab,SAB=SAB)
            sc = [ dict(i) for i in result]
            
            score_for_log = np.round(sc[0]['edge_cnt']/row['edges_files_count'],2)
            
            print(f' ... [{score_for_log}]'); logging.info(f'[{score_for_log}]')
            
            results_Ls.append(sc[0]['edge_cnt']) 
        
        col_counts_df['graph_count'] = results_Ls
        
        #print(f'col_count_df = {col_counts_df}',end='\n\n')

        # compute ratio column, makes it easy to see if the counts between the .tsv files
        # and the graph are close. closer to 1 the better
        col_counts_df['ratio'] = (col_counts_df['graph_count']/col_counts_df['edges_files_count']).round(2)
        
        return col_counts_df


# In[12]:


#q='match (cc:Code {SAB:$SAB}) return distinct cc.CodeID'

def nodes_edges_coverage(owlnets_path,codes_path,SAB=None,return_missing_codes=False):
    '''check that all codes in the edge file are either defined in the nodes file, or are already in the graph.
    Not part of the workflow, this is a stand-alone function'''
    
    # Read in  CODES.csv from Neo4j import dir
    codes = pl.read_csv(codes_path+'CODES.csv').select(['CodeID:ID','SAB']).unique()
    
    # OWLNETS_node_metadata.txt (aka nodes.tsv)
    nodes_codes = pl.read_csv(owlnets_path+'/OWLNETS_node_metadata.txt',separator='\t')\
                        .select('node_id').unique().with_columns(pl.col("node_id").str.split(" ").arr.get(0).alias("SAB"))
   
    # OWLNETS_edgelist.txt (aka edges.tsv)
    edges_codes = pl.read_csv(owlnets_path+'/OWLNETS_edgelist.txt',separator='\t').select(['subject','object']) 
        
    # combine subject/object col so we have all codes from edges file in one column
    edges_codes = pl.concat([edges_codes.select(pl.col('subject').alias('node_id')),
                                edges_codes.select(pl.col('object').alias('node_id'))],how='vertical').unique()\
                                 .with_columns(pl.col("node_id").str.split(" ").arr.get(0).alias("SAB"))

    if SAB is not None:  unique_sabs = [SAB] # search for specific SAB
    else: unique_sabs = edges_codes.select(pl.col('SAB')).unique().to_series() # do all SABs

    missing_codes_dict={}
    for CURRENT_SAB in list(unique_sabs):       
        # filter for CURRENT_SAB
        nodes_codes_sab = nodes_codes.filter(pl.col('SAB') == CURRENT_SAB).select(pl.col('node_id'))
        codes_sab = codes.filter(pl.col('SAB') == CURRENT_SAB).select(pl.col('CodeID:ID').alias('node_id'))
        edges_sab = edges_codes.filter(pl.col('SAB') == CURRENT_SAB).select('node_id')

        # combine the codes from the CODES.csv file and the OWLNETS_node_metadata.txt file
        codes_all_sab = pl.concat([nodes_codes_sab,codes_sab],how='vertical').unique()

        # find codes that are in edges but not CODES.csv or OWLNETS_node_metadata.txt files
        not_in = edges_sab.filter(~pl.col('node_id').is_in(codes_all_sab.to_series() ))    
        
        if return_missing_codes:
            missing_codes_dict[CURRENT_SAB] = not_in
        #print(f'{len(not_in)} missing Codes from {CURRENT_SAB}.')
        
    if return_missing_codes:
        return missing_codes_dict


# In[13]:


def fix_slashes(SAB: str,code_id_set: list()) -> list():        
    '''Remove slashes from a series and take whatever is to the right of it. 
      Example: 'http://purl.obolibrary.org/obo/UBERON_0001977' --> 'UBERON 0001977'   '''
    code_id_set = [i for i in code_id_set if type(i) == str] # drop float aka nan # only needed for 4DN nodes file
    df_codes = pd.DataFrame(code_id_set,columns=['codes'])
    df_codes['codes'] = [i.split('/')[-1].replace('_',' ').replace('#',' ') for i in df_codes['codes']]
    return df_codes['codes'].tolist()
    
    
# Wrappers
def compute_edge_counts(SAB,path) -> pd.DataFrame():
    col_counts_df = make_edge_counts(SAB,path)
    edge_counts_results = query_edges(SAB,col_counts_df)
    return edge_counts_results

def compute_node_counts(SAB,path) -> pd.DataFrame():
    sab_counts_df = make_node_counts(SAB,path)
    node_counts_results = query_nodes(SAB,sab_counts_df,path)
    return node_counts_results


# # Description of columns and how to interprete the nodes results dataframe
# - `sab`: The SAB of the Codes being searched for
# - `nodes_files_count`: How many unique Codes for the SAB are found in the OWLNETS_node_metadata.txt file
# - `graph_count`: How many unique Codes for the SAB are found in the graph (queried through Neo4j Python Driver)
# - `ratio`: (`graph_count`/`nodes_files_count`) this makes it easy to see what % of nodes made it into the graph.
# ##### There are 3 additional columns, only computed if `ratio` > 1 (meaning there were more nodes found in the graph than there was in the nodes file for any of the SABs. This happens when an ontology/dataset gets ingested and then another ontology uses the same Codes later on. )
# - `is_subset`: Whether or not the set of CodeIDs in the node_counts_file is a subset of the set of CodeIDs found in the graph (for the specific SAB). 1=subset (good),0=not a subset (bad), NaN=not computed.
# - `set_diff_len`: The number of Codes that are in nodes_files_count but not in the graph. 
# - `missing_sab_codes`: The set of Codes that are in nodes_files_count but not in the graph. 

# # Example:

# ## Interpretation
# -  `sab` shows that there were 7 unique sabs queried. The first 6 SABs were already in the graph as shown in the `graph_counts` column. 
# - The codes in the files for UBERON, EFO and HGNC are all subsets of the Codes in the graph (for the respective SABs) as shown in the `is_subset` column. 
# - As for CLO,BTO and CL, there are Codes for these SABs in the nodes files that are not in the graph, you can see the # of missing nodes in the `set_diff_len` column and you can see the actual set of missing codes in the `missing_sab_codes` column. 
# - The last SAB, SCREEN, was not found in the graph at all, as shown in the `graph_count` column, so there is some issue with these codes.   

# ## Interpretation Code for automated testing on github actions
# Helper scripts to automate tests on github actions, they evaluate the df that the other testing functions produce.

# In[14]:


def inteprete_node_count_results(df: pd.core.frame.DataFrame) -> bool:
    '''  There are 3 additional columns, only computed if `ratio` > 1 (meaning there were more nodes found in the graph than there was in the nodes file for any of the SABs. This happens when an ontology/dataset gets ingested and then another ontology uses the same Codes later on. )
   # `is_subset`: Whether or not the set of CodeIDs in the node_counts_file is a subset of the set of CodeIDs found in the graph (for the specific SAB). 1=subset (good),0=not a subset (bad), NaN=not computed.
   # `set_diff_len`: The number of Codes that are in nodes_files_count but not in the graph. 
   # `missing_sab_codes`: The set of Codes that are in nodes_files_count but not in the graph.  '''
    
    # test if subset related cols have been generated:    # could write this more succinctly....
    if 'is_subset' in df.columns:
        for idx,row in df.iterrows():
            # at least 75% of the nodes made it into the graph
            if row.is_subset == 1 or row.ratio > .75:   pass
            else: return 0  
        return 1
    else:
        for idx,row in df.iterrows():
            # at least 75% of the nodes made it into the graph
            if row.ratio > .75:  pass
            else: return 0
        return 1
    
def inteprete_edge_count_results(df: pd.core.frame.DataFrame) -> bool:
    for idx,row in df.iterrows():
        if row.ratio >= 1.0: pass
        else: return 0
    return 1


# In[15]:


path_sab_dict = {
    'LINCS':'LINCS',
'GTEX/gtex_exp':'GTEXEXP',
'4DN':'4DN',                    
'KidsFirst':'KF',
'CLINVAR':'CLINVAR',                   
'CMAP':'CMAP',               
'MSigDB':'MSIGDB',
'GENCODE_HSCLO':'GENCODEHSCLO',               
'STRING':'STRING',
#'GLYGEN': 'GLYGEN',                      
'human_genotype_phenotype':'HGNCHPO',
'GTEX/gtex_coexp_reduced':'GTEXCOEXP',
'GTEX/gtex_eqtl':'GTEXEQTL',
'human_mouse_orthologs':'HGNCHCOP',
'HPO_MP':'HPOMP',
'human_rat_ensembl_orthologs':'RATHCOP',
#'HSCLO':'HSCLO',                   
'mouse_genotype_phenotype':'HCOPMP',
'scHeart':'SCHEART',
'HUBMAP_AZ':'AZ'}


# In[16]:


def launch_tests(Datasets_path,path_sab_dict):
    
    logging.info('\n==============================\nComparing Node Counts\n==============================\n')
    print('\n==============================\nComparing Node Counts\n==============================\n')
    
    for path,SAB in path_sab_dict.items():
        print(f'Testing {SAB} node counts...\n'); logging.info(f'Testing {SAB} node counts...')
        inteprete_node_count_results(compute_node_counts(SAB,Datasets_path+path))
        #break
    
    logging.info('\n\n\n==============================\nComparing Edge Counts\n==============================')
    print('\n\n\n==============================\nComparing Edge Counts\n==============================')
    
    for path,SAB in path_sab_dict.items():    
        print(f'\nTesting {SAB} edge counts...\n'); logging.info(f'\nTesting {SAB} edge counts...\n')
        inteprete_edge_count_results(compute_edge_counts(SAB,Datasets_path+path))
    


# In[17]:


Datasets_path='/Users/stearb/Desktop/Petagraph_datasets/'
Datasets_path='Petagraph_datasets/'
launch_tests(Datasets_path=Datasets_path,path_sab_dict=path_sab_dict)


