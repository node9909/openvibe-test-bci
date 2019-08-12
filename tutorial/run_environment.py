# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 17:17:47 2019

@author: Seidi
"""
import datetime
import subprocess
import pandas as pd
import os
      
class run_environment():  
  
  def __init__(self):
    print('runModified Initialized')
    
  # This function takes the CSP, classifier, number of channels, and folder with the file to run's 
  #location, as well as the degrees of freedom required for the classifier
  def run_csp_classifier(file_dict, csp_class_folder, log_folder, typeTrn, bmi_id,
                         csp_scenario, class_scenario, rcsp_scenario, params):          
       
      tmp_dict = {}
      
      unique_id_str = 'uid_' + str(params.unique_id) + '_' + str(bmi_id)
      generated_csp =  typeTrn + '_csp_' + unique_id_str
      generated_classifier =  typeTrn + '_lda_' + unique_id_str
      
      ov_filename = file_dict['path'] + '\\' + file_dict['trn']
      #ov_filename = files_folder + '\\' + file_dict['trn']    
      ov_filename = ov_filename.replace('\\','\\\\')          
      
      csp_filename = csp_class_folder + '\\' + generated_csp       
      csp_filename = csp_filename.replace('\\','//')    
      
      classifier_filename = csp_class_folder + '\\' + generated_classifier       
      classifier_filename = classifier_filename.replace('\\','//')
      
      print('CSP filename:        {}'.format(generated_csp))
      print('Classifier filename: {}'.format(generated_classifier))
      
      # tell which file's CSP is running and then run it
      runCSP = 'call "C:\Program Files (x86)\openvibe-2.1.0\openvibe-designer.cmd" --no-visualization --no-gui \
      --define file "{}" --define version {} --define generated_csp "{}" \
      --play-fast "{}"'.format(ov_filename, 2, csp_filename, csp_scenario)
      #print(runCSP)
      p = subprocess.Popen(runCSP, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
      p.communicate()
  
      # tell which file's classifier is running and then run it
      runClass = 'call "C:\Program Files (x86)\openvibe-2.1.0\openvibe-designer.cmd" --no-visualization --no-gui \
      --define file "{}" --define version {}  --define generated_csp "{}" --define generated_classifier "{}"\
      --play-fast "{}"'.format(ov_filename, 2, csp_filename, classifier_filename, class_scenario)
      #print(runClass)
      p = subprocess.Popen(runClass, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
      p.communicate()          
  
      # after both are ran, get openvibe log from AppData\Roaming folder, copy it, and append to my own log for safekeeping
      oldLog = open(params.ov_log,'r')
      logInfo = oldLog.read()
      oldLog.close()
      
      os.remove(params.ov_log)
      
# =============================================================================
#       newLog = open(log_folder + 'withIndividualCSP.txt','a+')
#       newLog.write('_' * 80)
#       newLog.write('Now running file {}, time {}'.format(ov_filename, str(datetime.datetime.now())) + '\n\n')
#       newLog.write(logInfo)
#       newLog.close()
# =============================================================================
      
      # get accuracy from the log
      l = logInfo.split()
      for x in range(0, len(l)):
        if l[x] == 'Training' and l[x+1] == 'set' and l[x+2] == 'accuracy' and l[x+3] == 'is':
            accuracy = l[x+4]
    
      tmp_dict['file']       = ov_filename.replace('\\','/')
      tmp_dict['csp_used']   = generated_csp
      tmp_dict['class_used'] = generated_classifier
      tmp_dict['acc_csp']    = float(accuracy.replace('%',''))
      print('\taccuracy: ' + accuracy)
      
      count_tikh = 1
      for tikh_coeff in params.tikh_coeff:
          count_shrink = 1
          for shrink_coeff in params.shrink_coeff:
              unique_id_str = 'uid_' + str(params.unique_id) + '_' + str(bmi_id) + '_' + str(count_tikh) + '_' + str(count_shrink)
              generated_rcsp       = typeTrn + '_csp_' + unique_id_str
              generated_classifier = typeTrn + '_lda_' + unique_id_str
          
              rcsp_filename = csp_class_folder + '\\' + generated_rcsp       
              rcsp_filename = rcsp_filename.replace('\\','//')    
              
              classifier_filename = csp_class_folder + '\\' + generated_classifier       
              classifier_filename = classifier_filename.replace('\\','//')
              
              print('Now running RCSP ' + unique_id_str + ' and Classifier')
              print('RCSP filename (tikh = {}, shrink = {}): {}'.format(tikh_coeff,shrink_coeff,generated_rcsp))
              print('Classifier filename:                  {} '.format(generated_classifier))
                  
              # tell which file's RCSP is running and then run it
              runRCSP = 'call "C:\Program Files (x86)\openvibe-2.1.0\openvibe-designer.cmd" --no-visualization --no-gui \
              --define file "{}" --define version {} --define generated_csp "{}" --define shrink_coeff {} --define tikh_coeff {}\
              --play-fast "{}"'.format(ov_filename, 2, rcsp_filename, shrink_coeff, tikh_coeff, rcsp_scenario)
              #print(runCSP)
              p = subprocess.Popen(runRCSP, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
              p.communicate()              
      
              # tell which file's classifier is running and then run it
              runClass = 'call "C:\Program Files (x86)\openvibe-2.1.0\openvibe-designer.cmd" --no-visualization --no-gui \
              --define file "{}" --define version {}  --define generated_csp "{}" --define generated_classifier "{}"\
              --play-fast "{}"'.format(ov_filename, 2, rcsp_filename, classifier_filename, class_scenario)
              #print(runClass)
              p = subprocess.Popen(runClass, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
              p.communicate()          
                        
# =============================================================================
#               newLog = open(log_folder + 'withIndividualCSP.txt','a+')
#               newLog.write('_'*80)
#               newLog.write('Now running file {}, time {}'.format(ov_filename, str(datetime.datetime.now())) + '\n\n')
#               newLog.write(logInfo)
#               newLog.close()
# =============================================================================
              
              oldLog = open(params.ov_log,'r')
              logInfo = oldLog.read()
              oldLog.close()
              os.remove(params.ov_log)
              
              # get accuracy from the log
              l = logInfo.split()
              for x in range(0, len(l)):
                if l[x] == 'Training' and l[x+1] == 'set' and l[x+2] == 'accuracy' and l[x+3] == 'is':
                    accuracy = l[x+4]
              
              suffix = str(count_tikh) + '_' + str(count_shrink)
              tmp_dict['acc_csp_' + suffix]  = float(accuracy.replace('%',''))
              print('\taccuracy: ' + accuracy)
              
              count_shrink += 1  
          count_tikh += 1  
          
      return tmp_dict  
      
  def run_online(csp_class_folder, csv_folder, file_dict, online_scenario, params): 
      ov_filename = file_dict['path'] + '\\' + file_dict['file']
      #ov_filename = files_folder + '\\' + file_dict['file']      
      ov_filename = ov_filename.replace('\\','\\\\')       
      
      classifier_filename = csp_class_folder + '\\' + file_dict['classifier']       
      classifier_filename = classifier_filename.replace('\\','//')   
      
      csp_filename = csp_class_folder + '\\' + file_dict['csp']     
      csp_filename = csp_filename.replace('\\','//')    
      
      csv_filename = csv_folder + '\\' + file_dict['confusion_matrix']       
      csv_filename = csv_filename.replace('\\','//')      
      
      csp_to_use   = csp_filename
      csv_to_use   = csv_filename
      class_to_use = classifier_filename
      
      #tell which file's CSP is running and then run it
      run_online = 'call "C:\Program Files (x86)\openvibe-2.1.0\openvibe-designer.cmd" --no-visualization --no-gui \
      --define file "{}" --define version {} --define generated_csp "{}" --define generated_classifier "{}"\
      --define confusion_matrix "{}" \
      --play-fast "{}"'.format(ov_filename,2,csp_to_use, class_to_use, csv_to_use, online_scenario)
      p = subprocess.Popen(run_online, stdin=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
      stdout, stderr = p.communicate()
              
      csv_filename_split = csp_filename.split('uid')
      
      suffix = 'uid' + csv_filename_split[-1] + '_'
      rcsp_filename_stem  = csp_class_folder + '\\trn_csp_'          + suffix
      class_filename_stem = csp_class_folder + '\\trn_lda_'          + suffix
      csv_filename_stem   = csv_folder       + '\\confusion_matrix_' + suffix
      
      count_tikh   = 1      
      for itikh in range(len(params.tikh_coeff)):
          count_shrink = 1 
          for ishrink in range(len(params.shrink_coeff)):
              suffix = str(count_tikh) + '_' + str(count_shrink)
              csp_to_use   = rcsp_filename_stem.replace('\\','//')  + suffix
              class_to_use = class_filename_stem.replace('\\','//') + suffix
              csv_to_use   = csv_filename_stem.replace('\\','//')   + suffix + '.csv'   
              
              #tell which file's CSP is running and then run it
              run_online = 'call "C:\Program Files (x86)\openvibe-2.1.0\openvibe-designer.cmd" --no-visualization --no-gui \
              --define file "{}" --define version {} --define generated_csp "{}" --define generated_classifier "{}"\
              --define confusion_matrix "{}" \
              --play-fast "{}"'.format(ov_filename,2,csp_to_use, class_to_use, csv_to_use, online_scenario)
              p = subprocess.Popen(run_online, stdin=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
              stdout, stderr = p.communicate()              
              count_shrink += 1 
          count_tikh   += 1
          
  def read_conf_mat(csv_folder, csv_file, params):      
      tmp_dict = {}          
      
      filename = csv_folder + '\\' + csv_file          
      names_conf_mat = ['timea','timeb','l_correct','l_false','r_false','r_correct','ignore1','ignore2','ignore3']
      
      df_conf_mat = pd.read_csv(filename, sep=',', header=10, names = names_conf_mat)
      tmp_dict['l_correct_0'] = df_conf_mat['l_correct'].iloc[-1]
      tmp_dict['l_false_0']   = df_conf_mat['l_false'].iloc[-1]
      tmp_dict['r_correct_0'] = df_conf_mat['r_correct'].iloc[-1]
      tmp_dict['r_false_0']   = df_conf_mat['r_false'].iloc[-1]
      tmp_dict['accuracy_0']  = (tmp_dict['l_correct_0'] + tmp_dict['r_correct_0'])/ \
        (tmp_dict['l_correct_0'] + tmp_dict['l_false_0'] + tmp_dict['r_correct_0'] + tmp_dict['r_false_0'])        
        
      csv_file_split = csv_file.split('.')      
      count_tikh   = 1       
      for itikh in range(len(params.tikh_coeff)):
          count_shrink = 1 
          for ishrink in range(len(params.shrink_coeff)):   
              suffix = '_' + str(count_tikh) + '_' + str(count_shrink)      
              filename = csv_folder + '\\' + csv_file_split[0] + suffix + '.csv' 
              df_conf_mat = pd.read_csv(filename, sep=',', header=10, names = names_conf_mat)
              tmp_dict['l_correct' + suffix] = df_conf_mat['l_correct'].iloc[-1]
              tmp_dict['l_false'   + suffix] = df_conf_mat['l_false'].iloc[-1]
              tmp_dict['r_correct' + suffix] = df_conf_mat['r_correct'].iloc[-1]
              tmp_dict['r_false'   + suffix] = df_conf_mat['r_false'].iloc[-1]
              tmp_dict['accuracy'  + suffix] = (tmp_dict['l_correct' + suffix] + tmp_dict['r_correct' + suffix])/ \
                (tmp_dict['l_correct' + suffix] + tmp_dict['l_false' + suffix] + 
                          tmp_dict['r_correct' + suffix] + tmp_dict['r_false' + suffix])                
              count_shrink += 1  
          count_tikh += 1                  

      return tmp_dict
