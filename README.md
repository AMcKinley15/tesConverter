##Requirements for installation: 

###Python 3: [Installtion Guide](https://docs.python.org/3/using/index.html)
###Google API Library: 

####Use this [guide](https://developers.google.com/api-client-library/python/start/installation) or run

```
pip install --upgrade google-api-python-client oauth2clien
```


##To Run the Converter: 

```
python3 converter.py [path to source file] [path to destination file]
```

The converter will read the source file and look for strings that match the following pattern: [[Card Name]]. It will look them up against the spreadsheet and replace [[Card Name]] with the hover link.

If you would like to be specific, [[Card Name|image]] and [[Card Name|link]] can also be used.

Be careful, the card names are case sensative. The program should output and quit if it runs into a name it can't find. 