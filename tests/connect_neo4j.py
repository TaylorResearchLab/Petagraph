#!/usr/bin/env python
# coding: utf-8

from neo4j import GraphDatabase, basic_auth

uri='bolt://localhost:7687'
user='neo4j'
password='neo4j2020'

driver = GraphDatabase.driver(uri, auth=(user, password))


print('done)
