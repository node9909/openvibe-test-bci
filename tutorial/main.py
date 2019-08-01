# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 17:06:13 2019

@author: seidi
"""

import os
import run_environment as run_env
import pandas as pd
from time import time

current_folder  = os.getcwd()
csp_scenario    = current_folder + '\\openvibe_scenarios\\16chan_train_CSP.xml'
class_scenario  = current_folder + '\\openvibe_scenarios\\16chan_train_classifier.xml'
rcsp_scenario   = current_folder + '\\openvibe_scenarios\\16chan_train_RCSP.xml'
online_scenario = current_folder + '\\openvibe_scenarios\\replay_online.xml'

# Put the path to the log file below
ov_log           = 'user path \\AppData\\Roaming\\openvibe-2.1.0\\log\\openvibe-designer.log'   

log_folder       = current_folder + '\\txt_logs\\'
files_folder     = current_folder + '\\ov_files'
csp_class_folder = current_folder + '\\csp_and_classifier'
csv_folder       = current_folder + '\\csv'
results_folder   = current_folder + '\\results'

sessions_to_run = current_folder + '\\list_bmi.xlsx'
accuracy_table  = results_folder + '\\accuracy_table.csv' # It is produced after running run_csp_classifier

df_sessions     = pd.read_excel(sessions_to_run)
inds_trn_all    = df_sessions['type'] == 'trn'
inds_bartrn_all = df_sessions['type'] == 'bartrn'

Thik_coeff = [1e-3,1e-2,1e-1,1]
variants = len(Thik_coeff)

# =============================================================================
# 1. Get accuracies by running CSP/RCSP then Classifier scenarios on every .ov file
# =============================================================================
acc_list = []
count_ind = 0
start_time = time()
      
print("Now running CSPs and Classifiers")
for ind in range(len(df_sessions)):
    file_dict = {}
    ov_file   = df_sessions['ov_file'][count_ind].split('_')
    
    file_dict['trn']     = df_sessions['ov_file'][count_ind]
    file_dict['path']    = df_sessions['path_data'][count_ind]     
        
    print('file {}/{} : {}'.format(count_ind + 1,len(df_sessions), df_sessions['ov_file'][count_ind]))
    
    trn_acc = run_env.run_environment.run_csp_classifier(file_dict, count_ind + 1, files_folder, csp_class_folder, ov_log,
                                                         log_folder, csp_scenario, class_scenario, rcsp_scenario, Thik_coeff)
    acc_list.append(trn_acc) 
    print('\trun time since start: {:<1.2f} seconds\n'.format(time() - start_time))        
    count_ind += 1
    
df_accuracy = pd.DataFrame(acc_list)        
filename = results_folder + '\\' + 'accuracy_table.csv'
df_accuracy.to_csv(filename)        

# =============================================================================
# 2. Produce confusion_matrix by running the replay_online.xml scenario
# ov_file is a bartraining
# csp and classifier comes from the trn on the same session
# =============================================================================
trn_to_tes2 = []
count_trn = 1

print("Now running online simulations")
for ind in range(len(df_sessions)):
    if inds_bartrn_all[ind]:                
        tmp_dict = {}
        
        ov_file       = df_sessions['ov_file'][count_trn]
        ov_file_split = ov_file.split('_')
        stem = ov_file_split[0] + '_' + ov_file_split[1] + '_trn'
        ind_trn     = [i for i, elem in enumerate(df_accuracy['file']) if stem in elem]
        
        path          = df_sessions['path_data'][count_trn]        
        csp           = df_accuracy['csp_used'][ind_trn[0]]        
        classifier    = df_accuracy['class_used'][ind_trn[0]]        
        current_csv   = 'confusion_matrix_' + str(csp.split('_')[-1]) + '.csv'
        
        tmp_dict['file']             = ov_file
        tmp_dict['path']             = path
        tmp_dict['csp']              = csp
        tmp_dict['classifier']       = classifier
        tmp_dict['confusion_matrix'] = current_csv
        
        print('file {}/{} : {}'.format(count_trn,sum(inds_bartrn_all), ov_file))
        run_env.run_environment.run_online(files_folder, csp_class_folder, csv_folder, tmp_dict, online_scenario, variants)
        
        
        confusion_matrix = run_env.run_environment.read_conf_mat(csv_folder, current_csv, variants)
        trn_to_tes2.append(confusion_matrix)
        print('left correct:     ', confusion_matrix['l_correct_0'])
        print('left false:       ', confusion_matrix['l_false_0'])
        print('right correct:    ', confusion_matrix['r_correct_0'])
        print('right false:      ', confusion_matrix['r_false_0'])
        print('overall accuracy: ', confusion_matrix['accuracy_0'])
        
        count_trn += 1
        print('\trun time since start: {:<1.2f} seconds\n'.format(time() - start_time))

df_online_accuracy = pd.DataFrame(trn_to_tes2)      
filename = results_folder + '\\' + 'online_accuracy_table.csv'
df_online_accuracy.to_csv(filename) 