import json
import boto3

cW = boto3.client('cloudwatch')
def lambda_handler(event, context):

    alarmList = getAllAlarms()
    
    
    #print(findAllAlarmsWithFilePath(alarmList))
    
    deleteAlarms(findAllAlarmsWithFilePath(alarmList))

def getAllAlarms():
    alarms = cW.describe_alarms(MaxRecords=100)
    allAlarms = alarms['MetricAlarms']
    while(alarms.get('NextToken')):
        nextAlarms = cW.describe_alarms(MaxRecords=100, NextToken=alarms['NextToken'])
        allAlarms = allAlarms + nextAlarms['MetricAlarms']
        alarms = nextAlarms
    return allAlarms

def findAllAlarmsWithFilePath(listOfAlarms):
    foundAlarms = set()
    for alarm in listOfAlarms:
        alarmName = alarm['AlarmName']
        name_first5 = alarmName[0:5].lower()
        if (name_first5 == '/aws/'):
            foundAlarms.add(alarm['AlarmName'])
    return list(foundAlarms)
    
def deleteAlarms(listOfAlarmNames):
    alarmNamePages = [listOfAlarmNames[x:x+50] for x in range(0, len(listOfAlarmNames), 50)]
    for page in alarmNamePages:
        cW.delete_alarms(AlarmNames=page)
    print('Done')