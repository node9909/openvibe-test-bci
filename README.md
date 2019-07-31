# openvibe-test-bci
An example of framework to run in mass EEG files and BCI training on OpenVibe

A python code is used to run OpenVibe environments with variable setup parameters. Training information (mainly classifier accuracy) can be extracted from the log produced by OpenVibe Designer.

## Steps to run
A folder containg a standalone project is provided, I used it to run multiple variants of the Regularized CSP Trainer box + LDA classifier and compare the resulting training accuracies with classical CSP trainer box + LDA. If you want to run your own environments, follow the steps below:

1. Map .ov files (a .csv folder is input in the exmaple, but you can change the code provided to input any format)
2. Setup OpenVibe environment and add ${variable_name} to every configuration parameter you want to make generic, and which can be input by the code
3. Add call to run environment in run_environment.py module
4. Use run_environment.py functions in main.py to create your own pipeline and extract informations from OpenVibe Designer log

I hope this project can be used as an inspiration to implement fast EEG files processing and reduce manual parameters settings
