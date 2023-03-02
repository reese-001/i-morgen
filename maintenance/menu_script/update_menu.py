import os
from bs4 import BeautifulSoup
import boto3

exclusion_list = ['menu.html']
s3 = boto3.client('s3')



def iterate_bucket_items(bucket):

    response = s3.list_objects_v2(Bucket=bucket)

    for obj in response['Contents']:
        key = obj['Key']
        if key.endswith('.html') and not key.startswith('templates') and key not in exclusion_list:
            print(key)
            obj = s3.get_object(Bucket=bucket, Key=key)
            body = obj['Body'].read()

            s3.put_object(Bucket=bucket, Key=key, Body=str(body).encode('utf-8'))
            obj = s3.get_object(Bucket=bucket, Key=key)
            body = obj['Body'].read().decode('utf-8')
            
            # soup = BeautifulSoup(body, 'html.parser')
           
            # # Find the existing menu element in the HTML file
            # existing_menu = soup.find('div', {'class': 'page-header-fixed page-sidebar-fixed'})
            # # if key == 'app_dev/python/quick_commands.html': 
            # #     existing_menu = handle_failures(body, key, soup, bucket)
            # #     continue
            # # else:
            # print("outside")
            # new_menu = BeautifulSoup(template_menu_contents, 'html.parser').find('div', {'class': 'page-header-fixed page-sidebar-fixed'})
            # if new_menu:
            #     existing_menu.replace_with(new_menu) 
            #     s3.put_object(Bucket=bucket, Key=key, Body=str(soup).encode('utf-8'))


def get_template(bucket)         :

    template_menu_file = 'templates/menu.html'
    obj = s3.get_object(Bucket='test-340846', Key=template_menu_file)
    template_menu_contents = obj['Body'].read().decode('utf-8')

def handle_failures(body, key, soup, bucket):
    print("## FAILURE IN", key)
    dirpath = "C:\\Users\\erees\\OneDrive\\Documents\\development\\temp\\"
    filename = key.split('/')[-1]

    # save and reopen the file
    with open(os.path.join(dirpath, filename), 'w') as f:
        f.write(str(soup))
    with open(os.path.join(dirpath, filename), 'r', errors="ignore") as f:
        html_contents = f.read()

    # save and reopen the file from S3
    s3.put_object(Bucket=bucket, Key=key, Body=str(soup).encode('utf-8'))

    # parse the re-opened file   
    soup = BeautifulSoup(body, 'html.parser')
    existing_menu = soup.find('div', {'class': 'page-header-fixed page-sidebar-fixed'})

    new_menu = BeautifulSoup(template_menu_contents, 'html.parser').find('div', {'class': 'page-header-fixed page-sidebar-fixed'})
    existing_menu.replace_with(new_menu) 
    s3.put_object(Bucket=bucket, Key=key, Body=str(soup).encode('utf-8'))
    print("returning from failure")

