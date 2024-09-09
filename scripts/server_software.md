


## Download PIP
https://www.redhat.com/sysadmin/install-python-pip-linux

```
pip freeze > requirements.txt
cat requirements.txt | xargs -n 1 pip install     # this will continue if a package fails to install!
```

## Download Neo4j




## Download Ollama
curl -fsSL https://ollama.com/install.sh | sh
