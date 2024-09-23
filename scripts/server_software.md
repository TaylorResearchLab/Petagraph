
Notes on transferring files and downloading software on a RHEL (Red Hat linux) server

## Download PIP
https://www.redhat.com/sysadmin/install-python-pip-linux

```
pip freeze > requirements.txt
cat requirements.txt | xargs -n 1 pip install     # this will continue if a package fails to install!
```

## Download Ollama
`curl -fsSL https://ollama.com/install.sh | sh`

## Download Java
https://developers.redhat.com/products/openjdk/downloads/rhel
`sudo yum install java-17-openjdk`

To see Java version, do `java -version`.
Use `openjdk version "17.0.12" 2024-07-16 LTS`


## Download Neo4j
https://neo4j.com/docs/operations-manual/current/installation/linux/rpm

get tarball: https://neo4j.com/deployment-center/?gdb-selfmanaged
`tar  -xf neo4j-community-5.23.0-unix.tar`

(Permissions info: https://askubuntu.com/questions/528411/how-do-you-view-file-permissions)


## Create dump of database
https://neo4j.com/docs/operations-manual/current/kubernetes/operations/dump-load/

Troubleshoot database dump:
if you get permissions errors, you need to remove all permissions on `/etc/neo4j/neo4j.conf`, see https://neo4j.com/developer/kb/command-expansion-example-on-windows/

Do: `sudo chmod -R 400 /etc/neo4j/`

It should look like:
```
sudo ls -lah /etc/neo4j/neo4j-admin.conf 
-r--------. 1 neo4j neo4j 4.0K Apr 12 04:47 /etc/neo4j/neo4j-admin.conf
```
Create neo4j dump on taylor server:
**`sudo neo4j-admin database dump --expand-commands neo4j`**

On the taylor server if you dont specify a path to the save location of the dump it will be `/neo4j/5/data/dumps`

Send to new server:

change modifications of dump destinaton: `sudo chmod -R +666 /data/`

`sudo scp /neo4j/5/data/dumps/neo4j.dump stearb@reslngdb01.research.chop.edu:/data`


## Load new database
make sure to give proper permissions to the conf file on the new server, `sudo chmod -R 400 /path/to/neo4j.conf`

Load database dump:
```
rm -rf data/databases/*
rm -rf data/transactions/*
// neo4j.dump is located in /data/  directory
// MUST LOGIN AS root on the reslngdb01 server by doing sudo su
neo4j-admin database load --from-path=/data/ --overwrite-destination=true neo4j --verbose
```

## Configure/Start neo4j database
get plugin jars from taylor server

```
sudo scp /var/lib/neo4j/plugins/*.jar  stearb@reslngdb01:/home/stearb/graph_ml/
sudo mv /home/stearb/graph_ml/*.jar  /var/lib/neo4j/plugins
```
uncomment whitelist in config so apoc and gds work
`sudo vi /etc/neo4j/neo4j.conf`

use cypher-shell to create new password, or 
`bin/neo4j-admin dbms set-initial-password 'new_password'`

get memory recs
`sudo neo4j-admin server memory-recommendation`

server.memory.heap.initial_size=3400m
server.memory.heap.max_size=3400m
server.memory.pagecache.size=1800m












