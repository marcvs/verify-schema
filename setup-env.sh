#!/bin/bash

git submodule init
git submodule update
# Apply patch to allow parsing without core schema
patch -p1 < scimschema.patch
export PYTHONPATH=`pwd`/scimschema
echo "export PYTHONPATH=`pwd`/scimschema"
