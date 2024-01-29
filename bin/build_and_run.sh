#!/bin/bash

echo "Running pylint checks"
pylint pc_builder_backend/

echo "Running python unit tests!!!"
python3 -m unittest

if [ $? = 0 ]; # Checks that the return type is 0, if so continues to run the file
then
    echo "--------------------------------------"
    echo "Tests passed :) Flask Application Can be built in docker successfully"
    echo "--------------------------------------"
else # If the tests return 1 it indicates a fail, so the main file isn't run
    echo "Python unittests failed :( Please fix before building docker application"
fi