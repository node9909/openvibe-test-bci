import math
import itertools
import numpy as np
import operator

class parser():
    
  def __init__(self):
    print('PArser initialized')
    
      
  ####get channel combinations#####
  def channelCombos(channelNum): #assumes we always keep Cz + laplacian (4,5,8,11,12) electrodes
      n = itertools.combinations([1,2,3,6,7,9,10,13,14,15,16],channelNum)
      combos = []
      for x in n:
          combos.append(list(x))
      for x in range(0,len(combos)):
          for y in [4,5,8,11,12]:
              combos[x].append(y)
      return combos
  
  def OVify(l):                    
      string = ""
      for x in range(0,len(l)):
          string += str(l[x])
          if x != len(l)-1:
              string+=";"
      return string
  
  
  def getInfo(s):
      x = 0
      name = ''
      number = ''
      date = ''
      while s[x] != '_':
          name += s[x]
          x += 1
      x += 1
      while s[x] != '_':
          x += 1
      x += 1
      while s[x] != '_':
          number += s[x]
          x += 1
      x += 1
      while s[x] != '_':
          date += s[x]
          x += 1
      return [name, number, date]
  
  def findAcc(s,fileList):
      chNum = {}
      chCombos = {}
      d = {}
      dCount = 0
      chCount = 0
      chNumCount = 0
      channels = channelCombos(chNumList[chNumCount])
      l = s.split()
      for x in range(0, len(l)):
          if l[x] == 'Training' and l[x+1] == 'set' and l[x+2] == 'accuracy' and l[x+3] == 'is':
              #print(l[x+4])
              info = getInfo(fileList[dCount])
              acc = ""
              for y in l[x+4]:
                  if y != '%':
                      acc+=y
              info.append(acc)
              d[fileList[dCount]] = info
              dCount += 1
          if dCount == len(fileList):
              chCombos[OVify(channels[chCount])] = d
              chCount += 1
              d = {}
              dCount = 0
          if chCount == len(channels):
              chNum[chNumList[chNumCount]] = chCombos
              chCombos = {}
              chNumCount += 1
              if(chNumCount == len(chNumList)):
                  return chNum
              d = {}
              dCount = 0
              chCount = 0
              channels = channelCombos(chNumList[chNumCount])
          
          
      return chNum
  
  def saveDict(d,name):
      np.save(name, d)
  
  ##############analysis##############
  def findCHNumAverage(d,df,chNum, fileList): ####implement df later
      count = 0
      add = 0
      channels = channelCombos(chNum)
      for ch in channels:
          ch=OVify(ch)
          for f in fileList:
              add += float(d[chNum][ch][f][3])
              count += 1
      return add/count
  
  def findDFAverage(d,df,chNumList):
      count = 0
      add = 0
      for chNum in chNumList:
          channels = channelCombos(chNum)
          for ch in channels:
              ch=OVify(ch)
              for f in fileList:
                  #print(float(d[chNum][ch][f][3]))
                  add += float(d[chNum][ch][f][3])
                  count += 1
      return add/count
  
  
  def findCHComboAverage(d,df,chCombo):
      return
  
  def findDFVariance(d,df,chNumList, fileList):
      count = 0
      summation = 0
      for chNum in chNumList:
          channels = channelCombos(chNum)
          for ch in channels:
              ch=OVify(ch)
              for f in fileList:
                  summation += float(d[chNum][ch][f][3])**2
                  count += 1
      return summation/count-findDFAverage(d,df,chNumList)**2
  
  def findCHNumVariance(d,df,chNum, fileList):
      count = 0
      summation = 0
      channels = channelCombos(chNum)
      for ch in channels:
          ch=OVify(ch)
          for f in fileList:
              summation += float(d[chNum][ch][f][3])**2
              count += 1
      return summation/count-findCHNumAverage(d,df,chNum)**2
  
  def findCHNumSignificant(d,df,chNum, fileList):
      channels = channelCombos(chNum)
      significant = {}
      average = findCHNumAverage(d,df,chNum)
      variance = findCHNumVariance(d,df,chNum)
      for ch in channels:
          ch=OVify(ch)
          for f in fileList:
              if float(d[chNum][ch][f][3]) >= average + math.sqrt(variance)*2:
                  significant[f] = [ch,float(d[chNum][ch][f][3])]
      return significant
  
  def findDFSignificant(d,df,chNumList, fileList):
      significant = {}
      average = findDFAverage(d,df,chNumList)
      variance = findDFVariance(d,df,chNumList)
      for chNum in chNumList:
          channels = channelCombos(chNum)
          for ch in channels:
              ch=OVify(ch)
              for f in fileList:
                  if float(d[chNum][ch][f][3]) >= average + math.sqrt(variance)*2:
                      significant[ch] = [f,float(d[chNum][ch][f][3])]
      return significant
  
  ##for use with patientDictionary##
  def findPatientCHNumAverage(d, patient, chNum):
      count = 0
      add = 0
      channels = channelCombos(chNum)
      for ch in channels:
          ch=OVify(ch)
          for f in d[patient][chNum][ch]:
              add += float(d[patient][chNum][ch][f][3])
              count += 1
      return add/count
  
  def findPatientCHNumVariance(d,patient,chNum):
      count = 0
      summation = 0
      channels = channelCombos(chNum)
      for ch in channels:
          ch=OVify(ch)
          for f in d[patient][chNum][ch]:
              summation += float(d[patient][chNum][ch][f][3])**2
              count += 1
      return summation/count-findPatientCHNumAverage(d,patient,chNum)**2
  
  def findPatientCHNumSignificant(d,patient,chNum):
      channels = channelCombos(chNum)
      significant = {}
      average = findPatientCHNumAverage(d,patient,chNum)
      variance = findPatientCHNumVariance(d,patient,chNum)
      for ch in channels:
          ch=OVify(ch)
          for f in d[patient][chNum][ch]:
              if float(d[patient][chNum][ch][f][3]) >= average + math.sqrt(variance)*2:
                  significant[f] = [ch,float(d[patient][chNum][ch][f][3])]
      return significant
  
  
  
  def findPatientBestChannelCombo(d,patient,chNum):   
      channels = channelCombos(chNum)
      count = 0
      add = 0
      allCombos = {}
      bestCombos = {}
      if(chNum) == 11:
          for file in d[patient][chNum]['1;2;3;6;7;9;10;13;14;15;16;4;5;8;11;12']:
              add += float(d[patient][chNum]['1;2;3;6;7;9;10;13;14;15;16;4;5;8;11;12'][file][3])
              count += 1
          bestCombos['1;2;3;6;7;9;10;13;14;15;16;4;5;8;11;12'] = add/count
          return bestCombos
      for chCombo in d[patient][chNum]:
             for file in d[patient][chNum][chCombo]:
                 add += float(d[patient][chNum][chCombo][file][3])
                 count += 1
             allCombos[chCombo]=add/count
      while len(bestCombos) < 5:
          bestCombos[max(allCombos.items(), key=operator.itemgetter(1))[0]] = max(allCombos.items(), key=operator.itemgetter(1))[1]
          del allCombos[max(allCombos.items(), key=operator.itemgetter(1))[0]]
      return bestCombos
          
  def NormalizeMyData():
      patientD = np.load('patientDictionary.npy').item()
      masterD = np.load('CompletedRuns\df6ch2-3-4-6-7-8-9-10-11\df6ch2-3-4-6-7-8-9-10-11.npy').item()
      ###find max and min of each patient
      for patient in patientD:
          maxValue = 0
          minValue = 0
          for chNum in patientD[patient]:
              for combo in patientD[patient][chNum]:
                  for file in patientD[patient][chNum][combo]:
                      if float(patientD[patient][chNum][combo][file][3]) > maxValue:
                          maxValue = float(patientD[patient][chNum][combo][file][3])
                      if float(patientD[patient][chNum][combo][file][3]) < minValue:
                          minValue = float(patientD[patient][chNum][combo][file][3])
          ####then normalize the data in the master dictionary
          for chNum in masterD:
              for combo in masterD[chNum]:
                  for file in masterD[chNum][combo]:
                      ###check if it is the right patient
                      if masterD[chNum][combo][file][0] == patient:
                          masterD[chNum][combo][file][3] = str((float(masterD[chNum][combo][file][3]) - minValue)/(maxValue - minValue))
      return masterD
      
  def read(file, pNum):
      log = open(file,'r')
      s = log.read()
      log.close()
      result = findAccV2(s,[11],pNum)
      return result
  
  def findAccV2(s, chNumList, patientNum, fileList):
      chNum = {}
      chCombos = {}
      d = {}
      dCount = 0
      chCount = 0
      chNumCount = 0
      channels = channelCombos(chNumList[chNumCount])
      l = s.split()
      newFileList = []
      for x in fileList:
          if x[0:3] == patientNum:
              newFileList.append(x)
      for x in range(0, len(l)):
          if l[x] == 'Training' and l[x+1] == 'set' and l[x+2] == 'accuracy' and l[x+3] == 'is':
              #print(l[x+4])
              info = getInfo(newFileList[dCount])
              acc = ""
              for y in l[x+4]:
                  if y != '%':
                      acc+=y
              info.append(acc)
              d[newFileList[dCount]] = info
              dCount += 1
          if dCount == len(newFileList):
              chCombos[OVify(channels[chCount])] = d
              chCount += 1
              d = {}
              dCount = 0
          if chCount == len(channels):
              chNum[chNumList[chNumCount]] = chCombos
              chCombos = {}
              chNumCount += 1
              if(chNumCount == len(chNumList)):
                  return chNum
              d = {}
              dCount = 0
              chCount = 0
              channels = channelCombos(chNumList[chNumCount])

##################################

#log = open('CompletedRuns\df6ch2-3-4-6-7-8-9-10-11\logDF6Ch6.txt', 'r')
#string = log.read()
#log.close()
#chNum = findAcc(string,[6])
#saveDict(chNum, 'df6ch6.npy')
#####load with variable = np.load('file').item()

#print(findDFAverage(chNum,4,[0,1,2,10,11]))
#fileKeys = list(chNum[8]['1;2;3;6;7;9;10;13;4;5;8;11;12'])
#print(chNumKeys)
#print(chComboKeys)
#print(fileKeys)
#print(chNum[8]['1;2;3;6;7;9;10;13;4;5;8;11;12']['103CO_LSL_1288_Trn1_2017.06.14_15.35.00.ov'])



#create a dictionary to translate the returned dictionary from just having the
#number to having the file the accuracy belongs to
