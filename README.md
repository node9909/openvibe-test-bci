# openvibe-test-bci
An example of framework to run in mass EEG (Electroencephalography) files and BCI (Brain-Computer Interface) training on OpenVibe

A python code is used to run OpenVibe environments with variable setup parameters. Training information (mainly classifier accuracy) can be extracted from the log produced by OpenVibe Designer.

A folder containg a standalone project is provided, I used it to run multiple variants of the Regularized CSP Trainer box + LDA classifier and compare the resulting training accuracies with classical CSP trainer box + LDA. If you want to run your own environments, follow the steps below.

## Steps to run

1. Map .ov files (a .csv folder is input in the example, but you can change the code provided to input any format)
2. Setup OpenVibe environment and add ${variable_name} to every configuration parameter you want to make generic, and which can be input by the code
3. Add call to run environment in run_environment.py module
4. Use run_environment.py functions in main.py to create your own pipeline and extract informations from OpenVibe Designer log

## Pre-requisites

The following was used to produce the files: OpenVibe 2.1.0, Python 3, Microsoft Excel

Some expected knowledge:
- You should be familiar with [OpenVibe](http://openvibe.inria.fr/) software, if not, many tutorials are provided online and the software comes with example environments which can get you started
- Python language programming is used to implement the automatization so if you want to implement your own changes in the code, be sure to understand its syntax. The most important packages are [pandas](https://pandas.pydata.org/) and [subprocess](https://docs.python.org/3/library/subprocess.html)

I hope this project can be used as an inspiration to implement fast EEG files processing and reduce manual parameters settings

# TO DO
- (EASY) make all important static variables be read form a configFile
- (MEDIUM) rewrite main.py in batch mode
- (NEVER DID IT) try to implement it as a .exe ?
- (EASY) implement try-except logic for the processing pipeline (+ notify-run error message)

# Last Updates:
- (02/08/2019) Added notify-run, which can send you notifications through the [notify.run](https://notify.run/) service
