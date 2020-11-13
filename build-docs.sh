#! /usr/bin/env bash

set -e

( cd docs
# otherwise sphinx throws a warning about the missing directories
mkdir -p _static _build
# handle warnings as errors (usefull for travis ci)
sphinx-build -W . _build/html
if [ "$?" == "0" ]; then
  echo ""
  echo "html documentation can be found at:"
  echo $(pwd)/_build/html/index.html
fi
)
