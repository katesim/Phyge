#!/bin/bash

mkdir -p $(pwd)/db
dump_path=$(pwd)/db/dump-$(date "+%d-%m-%Y")
echo "Save dump to $dump_path"
mongodump --out "$dump_path"
