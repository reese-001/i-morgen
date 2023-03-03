import os
from bs4 import BeautifulSoup
import boto3
import codecs
from datetime import datetime


exclusion_list = ['menu.html', "status.html"]
s3 = boto3.client('s3')



def iterate_bucket_items(bucket):
    clear_failures(bucket)
    response = s3.list_objects_v2(Bucket=bucket)
    count = 0
    for obj in response['Contents']:
        key = obj['Key']
        template_menu_contents = get_template(bucket)
        if key.endswith('.html') and not key.startswith('templates') and key not in exclusion_list:

            print(key)
            obj = s3.get_object(Bucket=bucket, Key=key)
            body = obj['Body'].read().decode('utf-8')
            soup = BeautifulSoup(body, 'html.parser')
        
            existing_menu = soup.find('div', {'class': 'page-header-fixed page-sidebar-fixed'})

            new_menu = BeautifulSoup(template_menu_contents, 'html.parser').find('div', {'class': 'page-header-fixed page-sidebar-fixed'})
            if new_menu and existing_menu:
                existing_menu.replace_with(new_menu) 
                s3.put_object(Bucket=bucket, Key=key, Body=soup.prettify(formatter=None), ContentType='text/html')
     
                count += 1
            else:
                log_failures(bucket, key)
                
    update_history(bucket, count)

def get_template(bucket):

    template_menu_file = 'templates/menu.html'
    obj = s3.get_object(Bucket=bucket, Key=template_menu_file)
    return obj['Body'].read().decode('utf-8')

def update_history(bucket, count):
    key_status = "status.html"
    body_status = s3.get_object(Bucket=bucket, Key=key_status)
    body_status = body_status['Body'].read().decode('utf-8')
    soup_status = BeautifulSoup(body_status, 'html.parser')

    history = soup_status.find('div', {'class': 'history'})
    history.append("<a>" + str(datetime.now()) + ":  Files Updates: " + str(count) + "</a><br/>")
    s3.put_object(Bucket=bucket, Key=key_status, Body=soup_status.prettify(formatter=None), ContentType='text/html')      


def log_failures(bucket, key):
    key_status = "status.html"
    body_status = s3.get_object(Bucket=bucket, Key=key_status)

    body_status = body_status['Body'].read().decode('utf-8')

    soup_status = BeautifulSoup(body_status, 'html.parser')

    failed_menu_updates = soup_status.find('div', {'class': 'failed_menu_updates'})
    failed_menu_updates.append("<br/>" + key + " at " + str(datetime.now()))

    s3.put_object(Bucket=bucket, Key=key_status, Body=soup_status.prettify(formatter=None), ContentType='text/html')

def clear_failures(bucket):
    key_status = "status.html"
    body_status = s3.get_object(Bucket=bucket, Key=key_status)

    body_status = body_status['Body'].read().decode('utf-8')

    soup_status = BeautifulSoup(body_status, 'html.parser')

    failed_menu_updates = soup_status.find('div', {'class': 'failed_menu_updates'})
    failed_menu_updates.clear()

    s3.put_object(Bucket=bucket, Key=key_status, Body=soup_status.prettify(formatter=None), ContentType='text/html')