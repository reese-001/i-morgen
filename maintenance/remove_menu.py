import os
from bs4 import BeautifulSoup

top_dir = 'C:\\Users\\erees\\OneDrive\\Documents\\development\\i-morgen\\aws\\cicd\\'


# Define the paths to the directory containing HTML files and the common template file
# html_dir = 'C:\\Users\\erees\\OneDrive\\Documents\\development\\i-morgen\\aws\\code_build_copy\\'


# Read in the contents of the common template file


for dirpath, dirnames, filenames in os.walk(top_dir):
    print(dirpath)
    # Loop through each HTML file in the directory
    for filename in os.listdir(dirpath):
        print(filename)
        if filename.endswith('.html'):
            # Read in the contents of the HTML file
            with open(os.path.join(dirpath, filename), 'r') as f:
                html_contents = f.read()

            soup_text = html_contents

           


            # Parse the HTML contents using BeautifulSoup
            soup = BeautifulSoup(soup_text, 'html.parser')

            # Find the existing menu element in the HTML file
            existing_menu = soup.find('div', {'class': 'page-header-fixed page-sidebar-fixed'})

            existing_head = soup.find('head')

            # Replace the existing menu element with the contents of the template file
            if existing_menu:
                new_menu = BeautifulSoup("<div class='page-header-fixed page-sidebar-fixed'/>", 'html.parser').find('div', {'class': 'page-header-fixed page-sidebar-fixed'})
                print("found menu")
                if new_menu:
                    print("in_menu")
                    existing_menu.replace_with(new_menu)

            if existing_head:
                new_head = BeautifulSoup("""
                    <head>
                        <link rel='stylesheet' href='../styles.css'>
                        <title>i morgen</title>
                        <link rel='icon' href='../images/logo.png'>
                    </head>""", 'html.parser').find('head')
                print("found menu")
                if new_head:
                    print("in_menu")
                    existing_head.replace_with(new_head)

         



            # Save the updated HTML file to disk
            with open(os.path.join(dirpath, filename), 'w') as f:
                print("saving")
                f.write(str(soup))
