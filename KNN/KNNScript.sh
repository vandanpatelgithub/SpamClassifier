#!/usr/bin/env bash

cd ..
cd Bayesian
python WriteToTrainingFile.py
cd ..
cd KNN
python KNNClassifier.py
