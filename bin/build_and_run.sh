#!/bin/bash
#
#echo "Running pylint checks"
#pylint pc_builder_backend/

echo "Running python unit tests!!!"
python3 -m unittest

if [ $? = 0 ]; then
    echo "--------------------------------------"
    echo "Tests passed :) Flask Application can be built successfully"
    echo "--------------------------------------"
    echo "Running Flask Application..."
    python3 pc_builder_backend/app.py
else
    echo "Python unittests failed :( Please fix before building application"
fi
