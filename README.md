# rbxmodule-upload

A python script to upload MainModules to Roblox

## Usage

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

## Getting Started

Create a folder with a file named `init.lua` - this is your MainModule file. Everything else inside this file will be children of the Module.  
Folders with `init.*` will become their respective `*Script` class in Roblox, imitating Rojo behaviour.

Only supports `*.lua`, `*.client.lua` and `*.server.lua` files  
See <https://rojo.space/docs/0.5.x/reference/sync-details/#overview> for more information.
