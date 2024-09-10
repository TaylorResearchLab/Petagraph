


## Download PIP
https://www.redhat.com/sysadmin/install-python-pip-linux

```
pip freeze > requirements.txt
cat requirements.txt | xargs -n 1 pip install     # this will continue if a package fails to install!
```


## Download Java
https://developers.redhat.com/products/openjdk/downloads/rhel
`sudo yum install java-17-openjdk`

To see Java version, do `java -version`.
Use `openjdk version "17.0.12" 2024-07-16 LTS`


## Download Neo4j
https://neo4j.com/docs/operations-manual/current/installation/linux/rpm

get tarball: https://neo4j.com/deployment-center/?gdb-selfmanaged
`tar  -xf neo4j-community-5.23.0-unix.tar`




## Download Ollama
curl -fsSL https://ollama.com/install.sh | sh
