# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 23:35:55 2019

@author: wap
"""
import os

class params():
    
    def __init__(self):
        self.ov_log  = os.getenv('APPDATA') + '\\openvibe-2.1.0\\log\\openvibe-designer.log'
        
        self.shrink_coeff = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]   # gamma
        self.tikh_coeff   = [0, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1]             # alpha
        
        self.unique_id = 5
        
        self.computer_name = os.environ['COMPUTERNAME']
        
        self.file_filename_format = 'file_uniqueid_[unique_id]_[bmi_id]_[count_tikh]_[count_shrink]'