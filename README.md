# rbxmodule-upload

A python script to upload MainModules to Roblox

```text
usage: upload.py [-h] [-a COOKIE] [-d UPLOADURI] [-O OUTPUT] source

positional arguments:
  source                the source folder to be written as XML output

optional arguments:
  -h, --help            show this help message and exit
  -a COOKIE, --auth COOKIE
                        authorization cookie to provide when uploading the asset to destination
  -d UPLOADURI, --dest UPLOADURI
                        request destination - defaults to /Data/Upload.ashx?json=1&assetid=10
  -O OUTPUT, --output OUTPUT
                        output XML file destination
```
