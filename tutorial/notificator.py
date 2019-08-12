# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 19:35:06 2019

@author: seidi
"""
import os

# Must be installed
# notify_run will create a channel to post and receive quick text notifications
# You then open the link in a browswer to see the messages
# I'm using it in many computers, so code below doesn't register
from notify_run import Notify
      
class notificator():  
  
  def __init__(self):    
    self.notify = Notify()
    print(self.notify.info())
    self.project_name  = os.getcwd().split('\\')[-1] # Using the name of the parent folder
    self.computer_name = os.environ['COMPUTERNAME'] 
    
  # This function takes the CSP, classifier, number of channels, and folder with the file to run's 
  #location, as well as the degrees of freedom required for the classifier
  def send_msg(self, msg):       
    msg_to_send = '[{} - {}]\n' + msg
    msg_to_send = msg_to_send.format(self.computer_name, self.project_name)
    self.notify.send(msg_to_send)
