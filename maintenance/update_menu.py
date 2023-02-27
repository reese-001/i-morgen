import os
from bs4 import BeautifulSoup

directory_list = ["aws", "devops", "data_science"]
top_dir = 'C:\\Users\\erees\\OneDrive\\Documents\\development\\i-morgen\\aws\\'


# Define the paths to the directory containing HTML files and the common template file
# html_dir = 'C:\\Users\\erees\\OneDrive\\Documents\\development\\i-morgen\\aws\\code_build_copy\\'
template_menu_file = 'templates\menu.html'


# Read in the contents of the common template file
with open(template_menu_file, 'r') as f:
    template_menu_contents = f.read()


for dirpath, dirnames, filenames in os.walk(top_dir):
    if dirnames in directory_list:
    # Loop through each HTML file in the directory
        for filename in os.listdir(dirpath):
            if filename.endswith('.html'):
                # Read in the contents of the HTML file
                with open(os.path.join(dirpath, filename), 'r') as f:
                    html_contents = f.read()

                soup_text = html_contents

            


                # Parse the HTML contents using BeautifulSoup
                soup = BeautifulSoup(soup_text, 'html.parser')

                # Find the existing menu element in the HTML file
                existing_menu = soup.find('div', {'class': 'page-header-fixed page-sidebar-fixed'})

                # Replace the existing menu element with the contents of the template file
                if existing_menu:
                    new_menu = BeautifulSoup(template_menu_contents, 'html.parser').find('div', {'class': 'page-header-fixed page-sidebar-fixed'})
                    print("found menu")
                    if new_menu:
                        print("in_menu")
                        existing_menu.replace_with(new_menu)

            

                # Save the updated HTML file to disk
                with open(os.path.join(dirpath, filename), 'w') as f:
                    print("saving")
                    f.write(str(soup))
