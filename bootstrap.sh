#!/bin/bash

virtualenv --no-site-packages --distribute .
. bin/activate
pip install Flask==0.10.1 mock==1.0.1
