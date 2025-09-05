#!/usr/bin/env python3
"""script to verify a SCIM resource against a (set of) SCIM schemas"""

import os
import sys
import json
import argparse

sys.path.append(os.getcwd())
try:
    from scimschema import validate
    from scimschema._model.model import Model
except ImportError:
    print(
        """Unable to find python lib 'schimschema'
Please run these command from the folder that also contains the `.git` folder
for this repository:
        git submodule init
        git submodule update
        # Apply patch to allow parsing without core schema
        patch -p1 < scimschema.patch
        export PYTHONPATH=`pwd`/scimschema
"""
    )
    sys.exit(2)


def parseOptions():
    """parse commandline parameters"""
    parser = argparse.ArgumentParser(description="""verify_schema.py""")
    parser.add_argument("--schema", nargs='+',
                        default="eduperson_schema_parseable.json")
    parser.add_argument("--scim",
                        default="eduperson_SCIM_example_parseable.json")
    return parser.parse_args()


def load_json_schemas(filenames: list):
    """directly load a schema by filename"""
    retval = {}
    for filename in filenames:

        if not os.path.exists(filename):
            print(
                f"Cannot find {filename}.json."
            )
            sys.exit(3)

        with open(filename) as f:
            schema = Model.load(f)
            retval[schema.id] = schema
    return (retval)


def load_json_schema(filename):
    """directly load a schema by filename"""
    with open(filename) as f:
        schema = Model.load(f)
    return {schema.id: schema}


def load_json_data(filename):
    """load and parse json"""
    with open(filename) as f:
        data = f.read()
    try:
        obj = json.loads(data)
    except json.decoder.JSONDecodeError as ex:
        print(f"Error when decoding JSON:\n{ex}")
        sys.exit(4)
    return obj


args = parseOptions()

# print(F"schema file(s): {args.schema}")

schema_files = args.schema
scim_file = args.scim


scim_schema = load_json_schemas(schema_files)
scim_data = load_json_data(scim_file)
# print(F"Loaded SCIM data: {scim_file}")

try:
    validate(data=scim_data, extension_schema_definitions=scim_schema)
except Exception as e:
    print("\n--- Error: ----------------------------------------------")
    print(e)
    print("---------------------------------------------------------")
    sys.exit(1)
print("\nValidation success")
