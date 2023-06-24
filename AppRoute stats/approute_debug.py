"""
import all the reqiured librariers
"""
import requests
import json
from itertools import zip_longest
import difflib
import sys
import os
import time
import logging
import re
from tabulate import tabulate
import yaml
import json
from smtplib import SMTP
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pretty_html_table import build_table
from datetime import datetime, timedelta
import urllib.parse
from IPython.display import display
import matplotlib.pyplot as plt



from auth_header import Authentication as auth
from operations import Operation 





def url(vmanage_host,vmanage_port,api):
    """ return the URL for the privide API ENDpoint """
    """ function to get the url provide api endpoint """
    
    return f"https://{vmanage_host}:{vmanage_port}{api}"



def post_events(header, data):
    """ return the sla events """
    """  function to get the SLA events from the vmanage """
   

    api_events = '/dataservice/statistics/approute'
    url_events = url(vmanage_host,vmanage_port,api_events)
    events = Operation.post_method(url_events, header, data)

    return events['data']

def send_email(sender_email, mail_passwd, receiver_email, body):
    
    """ return if email is sent successful or not"""
    """ function to sent email """

    
    message = MIMEMultipart()
    message['Subject'] = "SLA EVENTS"

    body_content = body
    message.attach(MIMEText(body_content, "html"))
    msg_body = message.as_string()

    server = SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, mail_passwd)
    try:
        server.sendmail(sender_email, receiver_email, msg_body)
        return ('email sent')
    except:
        return ('error sending mail')

    server.quit()




if __name__=='__main__':

    while True:

        """ open the yaml file where the constant data is stored"""

        with open("approute.yaml") as f:
            config = yaml.safe_load(f.read())
        
        
        """ extracting info from Yaml file"""

        vmanage_host = config['vmanage_host']
        vmanage_port = config['vmanage_port']
        username = config['vmanage_username']
        password = config['vmanage_password']

        time_delta = config['time_delta']
        
        print("local_system_ip = ")
        local_system_ip = input()
        print("remote_system_ip = ")
        remote_system_ip = input()
        print("color = ")
        color = input()


        """ get current time and data and use time_delta to subract the time by delta minutes """
        date_time = datetime.utcnow()
        end_time = date_time.strftime("%Y-%m-%dT%H:%M:%S UTC")
        delta = date_time - timedelta( minutes = time_delta)
        start_time = delta.strftime("%Y-%m-%dT%H:%M:%S UTC")
        """print(start_time)
        print(end_time)"""


        """ Creted dataset"""
        approute_dataset = {"time":[],"local_Device_Name":[],"remote_Device_IP":[],"color":[],"loss":[],"latency":[],"jitter":[]}
        

    
        """  Calling the header function from Auth to get 
                'Content-Type': "application/json", 
                'Accept': '*/*', 'Cookie': session_id, 
                'X-XSRF-TOKEN': token_id}  """
        
        header = auth.get_header(vmanage_host, vmanage_port,username, password)



        """ Creating the request payload 
            since nested dict is not execpt in requests we used a str """
        data= '{\"query\":{\"condition\":\"AND\",\"rules\":[{\"value\":[\"'+start_time+'\",\"'+end_time+'\"],\"field\":\"entry_time\",\"type\":\"date\",\"operator\":\"between\"},{\"value\":[\"'+local_system_ip+'\"],\"field\":\"local_system_ip\",\"type\":\"string\",\"operator\":\"in\"},{\"value\":[\"'+remote_system_ip+'\"],\"field\":\"remote_system_ip\",\"type\":\"string\",\"operator\":\"in\"},{\"value\":[\"'+color+'\"],\"field\":\"local_color\",\"type\":\"string\",\"operator\":\"in\"}]}}'
        
        
        """ Caling the API ('/dataservice/statistics/approute') call with POST request """
        stats_data = post_events(header, data)
        
        
        """ parsing the returned data """
        for approute_data in stats_data:
            """print(sla_event_data)"""
            """approute_details = re.split('\=|;',stats_data['details'])"""
            approute_dataset["time"].append(time.strftime('%H:%M:%S', time.localtime(approute_data['entry_time']//1000)))
            approute_dataset["local_Device_Name"].append(approute_data['host_name'])
            approute_dataset["remote_Device_IP"].append(approute_data['remote_system_ip'])
            approute_dataset["color"].append(approute_data['local_color'])
            approute_dataset["loss"].append(approute_data['loss_percentage'])
            approute_dataset["latency"].append(approute_data['latency'])
            approute_dataset["jitter"].append(approute_data['jitter'])
       
                    
        """ Converting Dataset to Dataframe using pandas"""
        approute_dataframe = pd.DataFrame(approute_dataset)
        approute_dataframe_reverse = approute_dataframe[::-1]


        """ Convert pandas dataframe to HTML table """
        """ https://pypi.org/project/pretty-html-table/ """
        body = build_table(approute_dataframe, 'red_dark')
        

        """ extracting info from Yaml file"""
        """sender_email = config['sender_email']
        receiver_email = config['receiver_email']
        mail_password = config['mail_password']"""

        """ call send_email """
        """if sla_list_count >= 1:
            print(send_email(sender_email, mail_password, receiver_email, body))"""
        """sla_event_dataframe.to_csv('file1.csv')"""
        display(approute_dataframe_reverse)
        fig = plt.figure()
        plt.plot(approute_dataframe_reverse["time"],approute_dataframe_reverse["loss"],'r')
        plt.xlabel("Time")
        plt.ylabel("Loss")
        fig = plt.figure()
        plt.plot(approute_dataframe_reverse["time"],approute_dataframe_reverse["latency"],'g')
        plt.plot(approute_dataframe_reverse["time"],approute_dataframe_reverse["jitter"],'b')
        plt.legend(['Latency','Jitter'])
        plt.xlabel("Time")
        plt.ylabel("Latency and Jitter")
        
        """approute_dataframe.plot(x ='time', y='loss', kind='line')
        approute_dataframe.plot(x ='time', y='latency', kind='line')
        approute_dataframe.plot(x ='time', y='jitter', kind='line')"""
        plt.show()
        time.sleep(900)
