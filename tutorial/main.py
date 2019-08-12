# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 17:06:13 2019

@author: seidi
"""

# Deafult packages and my modules
import os
import pandas as pd
from time import time
from datetime import timedelta
import datetime
import notificator as nt
import run_environment as run_env
from my_config import params

import pickle

# Load parameters then save it for logging reasons
params = params()

flag_error = False

time_stamp = '{date:%Y_%m_%d_%H_%M_%S}'.format(date=datetime.datetime.now())

current_folder  = os.getcwd()
project_name    = current_folder.split('\\')[-1]
csp_scenario    = current_folder + '\\openvibe_scenarios\\16chan_train_CSP.xml'
class_scenario  = current_folder + '\\openvibe_scenarios\\16chan_train_classifier.xml'
rcsp_scenario   = current_folder + '\\openvibe_scenarios\\16chan_train_RCSP.xml'
online_scenario = current_folder + '\\openvibe_scenarios\\replay_online.xml'

# Folders to save generated files
new_folder       = current_folder + '\\architecture_uid_' + str(params.unique_id)
log_folder       = new_folder + '\\txt_logs\\'
csp_class_folder = new_folder + '\\csp_and_classifier'
csv_folder       = new_folder + '\\csv'
results_folder   = new_folder + '\\results'
params_folder    = new_folder + '\\params'

print('Generating new folders on',new_folder)
if not os.path.exists(new_folder):
    os.makedirs(log_folder)
    os.makedirs(csp_class_folder)
    os.makedirs(csv_folder)
    os.makedirs(results_folder)
    os.makedirs(params_folder)
else:
    print('It Already Exists!\n')
        
sessions_to_run  = current_folder + '\\list_bmi.xlsx'

# Read main table and get important indices
df_sessions     = pd.read_excel(sessions_to_run)
ind_process     = df_sessions['process'] == params.computer_name
ind_num_process = [i for i, x in enumerate(ind_process) if x]

inds_trn_all    = df_sessions['type'] == 'trn_legs_lda'
ind_trn         = ind_process*inds_trn_all

inds_bartrn_all = df_sessions['type'] == 'bartrn_legs_lda'
inds_bartrn     = ind_process&inds_bartrn_all

notificator = nt.notificator()

# Save parameters object
pickle_name = params_folder + '\\parameters_id' + str(params.unique_id) + '_' + params.computer_name + '.pckl'
f = open(pickle_name, 'wb')
pickle.dump(params, f)
f.close()

with open(new_folder + '\\' + params.computer_name + '_log_params.txt', 'w') as log_parameters:
    print("Parameters Used:\n \
        \tUnique Id          : {}\n \
        \tComputer Name      : {}\n \
        \tList Processed     : {}\n \
        \tInds processed     : {} - {}\n \
        \tTikhonov Coeffs    : {}\n \
        \tShrink Coeffs      : {}\n \
        \tFilename convention: {}\n \
        ".format(params.unique_id, params.computer_name, sessions_to_run, ind_num_process[0], ind_num_process[-1],
        params.tikh_coeff, params.shrink_coeff, params.file_filename_format), file=log_parameters)

# =============================================================================
# 1. Get accuracies by running CSP/RCSP then Classifier scenarios on every .ov file
# =============================================================================
acc_list = []
count_ind = 1
start_time = time()
      

time_to_finish = 12.9*len(params.tikh_coeff)*len(params.shrink_coeff)*sum(ind_process) # seconds
time_to_finish = timedelta(seconds=time_to_finish)
msg = 'Step 1/2: Now running CSPs and Classifiers\n \
    Estimated time to finish Step 1: ' + str(time_to_finish)
notificator.send_msg(msg)

for ind in range(len(df_sessions)):    
  try:    
    if ind_process[ind]:
        if ind_trn[ind]:
            typeTrn = 'trn'
        elif inds_bartrn[ind]:
            typeTrn = 'bar'
            
        file_dict = {}
        
        file_dict['trn']  = df_sessions['ov_file'][ind]
        file_dict['path'] = df_sessions['path_data'][ind]     
        bmi_id            = df_sessions['meas_bmi_id'][ind]   
            
        print('file {}/{} : {}'.format(count_ind,sum(ind_process), df_sessions['ov_file'][ind]))
        
        trn_acc = run_env.run_environment.run_csp_classifier(file_dict, csp_class_folder, log_folder, typeTrn,  bmi_id,
                                                             csp_scenario, class_scenario, rcsp_scenario, params)
        acc_list.append(trn_acc) 
        print('\trun time since start: {:<1.2f} seconds\n'.format(time() - start_time))     
        
        count_ind += 1
           
  except:
    notificator.send_msg('Step 1: Something went wrong at ind = ' + str(ind))
    flag_error = True
    break
    
df_accuracy = pd.DataFrame(acc_list)        
filename    = results_folder + '\\' + params.computer_name + '_accuracy_table_uid_' + str(params.unique_id) + '_' + time_stamp + '.csv'
df_accuracy.to_csv(filename)     

# =============================================================================
# 2. Produce confusion_matrix by running the replay_online.xml scenario
# ov_file is a bartraining
# csp and classifier comes from the trn on the same session
# =============================================================================
trn_to_test2 = []
count_trn = 1

time_to_finish = 7*len(params.tikh_coeff)*len(params.shrink_coeff)*sum(inds_bartrn) # seconds
time_to_finish = timedelta(seconds=time_to_finish)
msg = 'Step 2/2: Now running online simulations \n \
    Estimated time to finish Step 2: ' + str(time_to_finish)
notificator.send_msg(msg)

for ind in range(len(df_sessions)):
  try:
    if inds_bartrn[ind]:                
        tmp_dict = {}
        
        ov_file       = df_sessions['ov_file'][ind]
        ov_file_split = ov_file.split('_')
        stem = ov_file_split[0] + '_' + ov_file_split[1] + '_' +  ov_file_split[2] + '_Trn'
        ind_trn     = [i for i, elem in enumerate(df_accuracy['file']) if stem in elem]
        
        path        = df_sessions['path_data'][ind]        
        csp         = df_accuracy['csp_used'][ind_trn[0]]        
        classifier  = df_accuracy['class_used'][ind_trn[0]]        
        current_csv = 'confusion_matrix_uid' + str(csp.split('uid')[-1]) + '.csv'
        
        tmp_dict['file']             = ov_file
        tmp_dict['path']             = path
        tmp_dict['csp']              = csp
        tmp_dict['classifier']       = classifier
        tmp_dict['confusion_matrix'] = current_csv
        
        print('file {}/{} : {}'.format(count_trn,sum(inds_bartrn), ov_file))
        run_env.run_environment.run_online(csp_class_folder, csv_folder, tmp_dict, online_scenario, params)        
        
        confusion_matrix = run_env.run_environment.read_conf_mat(csv_folder, current_csv, params)
        trn_to_test2.append(confusion_matrix)
        confusion_matrix['file']             = ov_file
        confusion_matrix['path']             = path
        confusion_matrix['csp']              = csp
        confusion_matrix['classifier']       = classifier
        confusion_matrix['confusion_matrix'] = current_csv
        print('left correct:           ', confusion_matrix['l_correct_0'])
        print('left false:             ', confusion_matrix['l_false_0'])
        print('right correct:          ', confusion_matrix['r_correct_0'])
        print('right false:            ', confusion_matrix['r_false_0'])
        print('overall accuracy w csp: ', confusion_matrix['accuracy_0'])
        
        print('\trun time since start: {:<1.2f} seconds\n'.format(time() - start_time))
        count_trn += 1
        
  except:
    notificator.send_msg('Step 2: Something went wrong at ind = ' + str(ind))
    flag_error = True
    break    

if flag_error:
  notificator.send_msg('Something went wrong, read the log! Saving results until here...')  
else:
  notificator.send_msg('FINISHED!')
  
df_online_accuracy = pd.DataFrame(trn_to_test2)      
filename = results_folder + '\\' + params.computer_name + '_online_accuracy_table_uid_' + str(params.unique_id) + '_' + time_stamp + '.csv'
df_online_accuracy.to_csv(filename) 