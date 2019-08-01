# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 17:17:47 2019

@author: Seidi
"""
import datetime
import subprocess
import pandas as pd
      
class run_environment():  
  
  def __init__(self):
    print('runModified Initialized')
    
  # This function takes the CSP, classifier, number of channels, and folder with the file to run's 
  #location, as well as the degrees of freedom required for the classifier
  def run_csp_classifier(count, files_folder, csp_class_folder, file_list, ov_log_folder,
                         log_folder, results_folder, csp_scenario, class_scenario, rcsp_scenario):          
       
      tmp_dict = {}
      generated_csp = 'csp_' + str(count)
      generated_classifier = 'classifier_with_csp_' + str(count)
      
      #ov_filename = file_list['path'][ind] + '\\' + file_list['trn'][ind]
      ov_filename = files_folder + '\\' + file_list['trn']    
      ov_filename = ov_filename.replace('\\','\\\\')          
      
      csp_filename = csp_class_folder + '\\' + generated_csp       
      csp_filename = csp_filename.replace('\\','//')    
      
      classifier_filename = csp_class_folder + '\\' + generated_classifier       
      classifier_filename = classifier_filename.replace('\\','//')
      
      print("Now running CSP and Classifier")
      print('CSP filename:        {}'.format(generated_csp))
      print('Classifier filename: {}'.format(generated_classifier))
      
      # tell which file's CSP is running and then run it
      runCSP = 'call "C:\Program Files (x86)\openvibe-2.1.0\openvibe-designer.cmd" --no-visualization --no-gui \
      --define file "{}" --define version {} --define generated_csp "{}" \
      --play-fast "{}"'.format(ov_filename, 2, csp_filename, csp_scenario)
      p = subprocess.Popen(runCSP, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
      # print(runCSP) # If any error, try to copy paste this print in cmd
      p.communicate()
  
      # tell which file's classifier is running and then run it
      runClass = 'call "C:\Program Files (x86)\openvibe-2.1.0\openvibe-designer.cmd" --no-visualization --no-gui \
      --define file "{}" --define version {}  --define generated_csp "{}" --define generated_classifier "{}"\
      --play-fast "{}"'.format(ov_filename, 2, csp_filename, classifier_filename, class_scenario)
      p = subprocess.Popen(runClass, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
      p.communicate()          
  
      # after both are ran, get openvibe log from AppData\Roaming folder, copy it, and append to my own log for safekeeping
      oldLog = open(ov_log_folder,'r')
      logInfo = oldLog.read()
      oldLog.close()
      
      newLog = open(log_folder + 'withIndividualCSP.txt','a+')
      newLog.write('_' * 80)
      newLog.write('Now running file {}, time {}'.format(ov_filename, str(datetime.datetime.now())) + '\n\n')
      newLog.write(logInfo)
      newLog.close()
      
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
      
      count_rcsp = 1
      coeff = 1e-2
      while coeff <= 1:
          generated_rcsp = 'rcsp_' + str(count) + '_' + str(count_rcsp)
          generated_classifier = 'classifier_with_rcsp_' + str(count) + '_' + str(count_rcsp)  
      
          rcsp_filename = csp_class_folder + '\\' + generated_rcsp       
          rcsp_filename = rcsp_filename.replace('\\','//')    
          
          classifier_filename = csp_class_folder + '\\' + generated_classifier       
          classifier_filename = classifier_filename.replace('\\','//')
          
          reg_coeff = coeff
          print("Now running RCSP" + str(count_rcsp) + " and Classifier")
          print('RCSP filename (gamma = {}): {}'.format(reg_coeff,generated_rcsp))
          print('Classifier filename:         {} '.format(generated_classifier))
              
          # tell which file's RCSP is running and then run it
          runCSP = 'call "C:\Program Files (x86)\openvibe-2.1.0\openvibe-designer.cmd" --no-visualization --no-gui \
          --define file "{}" --define version {} --define generated_csp "{}" --define reg_coeff {}\
          --play-fast "{}"'.format(ov_filename, 2, rcsp_filename, reg_coeff, rcsp_scenario)
          p = subprocess.Popen(runCSP, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
          # print(runCSP) # If any error, try to copy paste this print in cmd
          p.communicate()
  
          # tell which file's classifier is running and then run it
          runClass = 'call "C:\Program Files (x86)\openvibe-2.1.0\openvibe-designer.cmd" --no-visualization --no-gui \
          --define file "{}" --define version {}  --define generated_csp "{}" --define generated_classifier "{}"\
          --play-fast "{}"'.format(ov_filename, 2, rcsp_filename, classifier_filename, class_scenario)
          p = subprocess.Popen(runClass, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
          p.communicate()          
                    
          newLog = open(log_folder + 'withIndividualCSP.txt','a+')
          newLog.write('_' * 80)
          newLog.write('Now running file {}, time {}'.format(ov_filename, str(datetime.datetime.now())) + '\n\n')
          newLog.write(logInfo)
          newLog.close()
          
          oldLog = open(ov_log_folder,'r')
          logInfo = oldLog.read()
          oldLog.close()
          
          # get accuracy from the log
          l = logInfo.split()
          for x in range(0, len(l)):
            if l[x] == 'Training' and l[x+1] == 'set' and l[x+2] == 'accuracy' and l[x+3] == 'is':
                accuracy = l[x+4]
          
          tmp_dict['acc_rcsp' + str(count_rcsp)]   = float(accuracy.replace('%',''))
          print('\taccuracy: ' + accuracy)
          
          count_rcsp += 1       
          coeff *= 10
          
      return tmp_dict              

      
  def run_online(files_folder, csp_class_folder, csv_folder, file_list, online_scenario): 
      #ov_filename = file_list['path'][ind] + '\\' + file_list['file'][ind]
      ov_filename = files_folder + '\\' + file_list['file']      
      ov_filename = ov_filename.replace('\\','\\\\')          
      
      csp_filename = csp_class_folder + '\\' + file_list['csp']     
      csp_filename = csp_filename.replace('\\','//')    
      
      classifier_filename = csp_class_folder + '\\' + file_list['classifier']       
      classifier_filename = classifier_filename.replace('\\','//')
      
      csv_filename = csv_folder + '\\' + file_list['confusion_matrix']       
      csv_filename = csv_filename.replace('\\','//')
      
      print("Now running online simulation")
      tmp_dict = {}
      
      #tell which file's CSP is running and then run it
      run_online = 'call "C:\Program Files (x86)\openvibe-2.1.0\openvibe-designer.cmd" --no-visualization --no-gui \
      --define file "{}" --define version {} --define generated_csp "{}" --define generated_classifier "{}"\
      --define confusion_matrix "{}" \
      --play-fast "{}"'.format(ov_filename,2,csp_filename,classifier_filename, csv_filename, online_scenario)
      p = subprocess.Popen(run_online, stdin=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
      stdout, stderr = p.communicate()
      print(run_online)          
              
      count_rcsp = 1
      coeff = 1e-3
      while coeff <= 1:
          count_rcsp += 1       
          coeff *= 10
      
      return tmp_dict
          
  def read_conf_mat(csv_folder, csv_file):      
      tmp_dict = {}
      
      filename = csv_folder + '\\' + csv_file
      df_conf_mat = pd.read_csv(filename, sep=',', header=10, names=['timea','timeb','left_correct','left_false',
        'right_correct','right_false','ignore1','ignore2','ignore3'])
      tmp_dict['left_correct']  = df_conf_mat['left_correct'].iloc[-1]
      tmp_dict['left_false']    = df_conf_mat['left_false'].iloc[-1]
      tmp_dict['right_correct'] = df_conf_mat['right_correct'].iloc[-1]
      tmp_dict['right_false']   = df_conf_mat['right_false'].iloc[-1]
      tmp_dict['accuracy']      = (tmp_dict['left_correct'] + tmp_dict['right_correct'])/ \
        (tmp_dict['left_correct'] + tmp_dict['left_false'] + tmp_dict['right_correct'] + tmp_dict['right_false'])
      return tmp_dict

