import argparse
import json
import io
import os

import lxml.etree as ET
import pip._vendor.requests as requests

parser = argparse.ArgumentParser()
parser.add_argument(
    "-a",
    "--auth",
    dest="cookie",
    help=
    "authorization cookie to provide when uploading the asset to destination")
parser.add_argument(
    "-d",
    "--dest",
    dest="uploadUri",
    default="https://data.roblox.com/Data/Upload.ashx?json=1&assetid=10",
    help="request destination - defaults to /Data/Upload.ashx?json=1&assetid=10"
)
parser.add_argument("source",
                    help="the source folder to be written as XML output")
parser.add_argument("-o",
                    "--output",
                    dest="output",
                    help="output XML file destination")

args = parser.parse_args()


def new_plain_rbxmx():
    root = ET.Element("roblox",
                      nsmap={
                          "xmime": "http://www.w3.org/2005/05/xmlmime",
                      },
                      )
    root.set("version", "4")

    external = ET.Element("External", {})
    external.text = "null"
    external2 = ET.Element("External", {})
    external2.text = "nil"

    root.append(external)
    root.append(external2)

    return root


def new_instance(className, parent):
    inst = ET.Element("Item")
    inst.set("class", className)

    parent.append(inst)

    return inst


def give_script_properties(element, obj_name, src):
    Properties = ET.Element("Properties")

    disabled = ET.Element("bool", {})
    disabled.text = "false"
    disabled.set("name", "Disabled")

    name = ET.Element("string")
    name.text = obj_name
    name.set("name", "Name")

    source = ET.Element("ProtectedString")
    source.text = ET.CDATA(src)
    source.set("name", "Source")

    content = ET.Element("Content")
    content.set("name", "LinkedSource")
    content.append(ET.Element("null"))

    Properties.append(disabled)
    Properties.append(name)
    Properties.append(source)
    Properties.append(content)

    element.append(Properties)

    return Properties


def uploadToRoblox(moduleXML):
    requests.post(args.uploadUri,
                  data=moduleXML,
                  headers={'Content-Type': 'application/xml'},
                  cookies={".ROBLOSECURITY": args.cookie})


def writeOutput(dest):
    tree = ET.ElementTree(root)
    tree.write(dest, encoding="UTF-8")


def fsToTree(folder):



root = new_plain_rbxmx()
give_script_properties(new_instance("ModuleScript", root), "main", "aaaaaa")

if (args.output):
    writeOutput(args.output)
