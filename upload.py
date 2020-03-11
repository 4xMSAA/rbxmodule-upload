# a poorly made Python script meant for building a MainModule XML with Rojo-like structure

import argparse
import json
import os
import re

import lxml.etree as ET
import pip._vendor.requests as requests

from pathlib import Path

parser = argparse.ArgumentParser()

parser.add_argument("source",
                    help="the source folder to be written as XML output")
parser.add_argument(
    "-a",
    "--auth",
    dest="cookie",
    help=
    "authorization cookie to provide when uploading the asset to destination")
parser.add_argument(
    "-d",
    "--dest",
    dest="upload_uri",
    default="https://data.roblox.com/Data/Upload.ashx?assetid=0&type=Model&ispublic=True&name=Module&allowComments=False",
    help="request destination - defaults to https://data.roblox.com/Data/Upload.ashx?assetid=0&type=Model&ispublic=True&name=Module&allowComments=False"
)
parser.add_argument("-O",
                    "--output",
                    dest="output",
                    default="out.rbxmx",
                    help="output XML file destination")

args = parser.parse_args()


def new_plain_rbxmx():
    root = ET.Element(
        "roblox",
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


def set_name(element, obj_name):
    Properties = ET.Element("Properties")

    name = ET.Element("string")
    name.text = obj_name
    name.set("name", "Name")

    Properties.append(name)
    element.append(Properties)

    return Properties


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


def upload_to_roblox(xml_body):
    res = requests.post(args.upload_uri,
                  data=xml_body,
                  headers={'Content-Type': 'application/xml, charset=utf-8', 'User-Agent': ''},
                  cookies={".ROBLOSECURITY": args.cookie})

    print("Uploaded! Asset ID is:")
    print(res.text)


def write_output(root_element, dest):
    tree = ET.ElementTree(root_element)
    tree.write(dest, encoding="UTF-8")


def get_instance_type_from_extension(filename):
    if (filename.endswith(".client.lua")):
        return "LocalScript"
    elif (filename.endswith(".server.lua")):
        return "Script"
    elif (filename.endswith(".lua")):
        return "ModuleScript"


# really messy, could be cleaned up
def fs_to_tree(folder, root_element):
    element_roots = {str(folder): root_element}
    for root, dirs, files in os.walk(folder, topdown=True):
        print(root, dirs, files)
        dirname = os.path.basename(root)
        parent_basename = str(Path(root).parents[0]) if root != folder else os.path.basename(root)
        parent_element = element_roots[parent_basename]
        cur_element = None
        # check for init files first
        has_init = False
        for filename in files:
            if (filename.startswith("init")):
                cur_element = new_instance(
                    "ModuleScript" if root == folder else get_instance_type_from_extension(filename),
                    parent_element)
                give_script_properties(
                    cur_element,
                    "MainModule" if root == folder else dirname,
                    "".join(open(root + "/" + filename, "r").readlines()))
                element_roots[root] = cur_element
                has_init = True
                break
        if (not has_init):
            cur_element = new_instance("Folder", parent_element)
            set_name(cur_element, dirname)
            element_roots[root] = cur_element

        # now iterate through the files

        for filename in files:
            if (filename.startswith("init")):
                continue

            element = new_instance(
                "ModuleScript" if root == folder else get_instance_type_from_extension(filename),
                cur_element)
            give_script_properties(
                element,
                re.sub("(.client|.server)$", "", Path(filename).stem),
                "".join(open(root + "/" + filename, "r").readlines()))






rbxmx = new_plain_rbxmx()
fs_to_tree(args.source, rbxmx)

if (args.output):
    write_output(rbxmx, args.output)

if (args.cookie):
    res = requests.get("https://www.roblox.com/game/GetCurrentUser.ashx", cookies={".ROBLOSECURITY": args.cookie})
    if (res.status_code != 200):
        print(".ROBLOSECURITY Cookie is invalid")
        exit(code=-1)
    upload_to_roblox("".join(open(args.output, "r").readlines()))
