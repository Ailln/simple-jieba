#!/usr/bin/env bash

pip uninstall simjb -y

python setup.py clean
python setup.py install
