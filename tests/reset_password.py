#!/usr/bin/env python
# coding: utf-8

import neo4j
from neo4j import GraphDatabase, basic_auth

uri='bolt://localhost:7687'
user='neo4j'
#password=args.NEO4J_PASSWORD

driver = GraphDatabase.driver(uri, auth=(user, password))

pw_query=''' '''
with driver.session(default_access_mode=neo4j.WRITE_ACCESS) as session:
        result = session.run(pw_query)
