import json
from xml.etree import ElementTree as ET

from sigla.classes.ImportNode import ImportNode


def load_xml_from_file(filename):
    return ET.parse(filename).getroot()


def load_string(str):
    return ET.fromstring(str).getroot()


def load_xml_string_into_nodes(s) -> ImportNode:
    obj: ET = ET.fromstring(s)
    node = process_xml(obj)
    return node


def process_xml(obj) -> ImportNode:
    attributes = obj.attrib.copy()
    new_attributes = {}

    for k, v in attributes.items():
        if k.endswith("-int"):
            new_key = k.replace("-int", "")
            new_attributes[new_key] = int(attributes[k])
        elif k.endswith("-float"):
            new_key = k.replace("-float", "")
            new_attributes[new_key] = float(attributes[k])
        elif k.endswith("-json"):
            new_key = k.replace("-json", "")
            new_attributes[new_key] = json.loads(attributes[k])
        else:
            new_attributes[k] = attributes[k]

    node = ImportNode(obj.tag, attributes=new_attributes, children=[])
    for child in obj:
        node.children.append(process_xml(child))
    return node
