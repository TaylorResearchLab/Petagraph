#!/usr/bin/env python
# coding: utf-8


from neo4j import GraphDatabase, basic_auth

uri='bolt://localhost:7687'
user='neo4j'
#password='neo4j2020'
password='neo4j'
#password=args.NEO4J_PASSWORD

driver = GraphDatabase.driver(uri, auth=(user, password))

pw_query='''ALTER CURRENT USER SET PASSWORD FROM "neo4j" TO "neo4j2020"'''
with driver.session(default_access_mode=neo4j.WRITE_ACCESS) as session:
        result = session.run(pw_query)
