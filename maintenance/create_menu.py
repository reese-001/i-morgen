import os

from bs4 import BeautifulSoup

top_dir = 'C:\\Users\\erees\\OneDrive\\Documents\\development\\i-morgen\\management\\'


# Define the paths to the directory containing HTML files and the common template file
# html_dir = 'C:\\Users\\erees\\OneDrive\\Documents\\development\\i-morgen\\aws\\code_build_copy\\'
template_menu_file = 'templates\menu.html'
template_head_file = 'templates\head.html'
temp = input(top_dir)
# Read in the contents of the common template file
with open(template_menu_file, 'r') as f:
    template_menu_contents = f.read()

with open(template_head_file, 'r') as f:
    template_head_contents = f.read()


for dirpath, dirnames, filenames in os.walk(top_dir):
    # Loop through each HTML file in the directory
    for filename in os.listdir(dirpath):
        if filename.endswith('.html'):
            # Read in the contents of the HTML file
            with open(os.path.join(dirpath, filename), 'r') as f:
                html_contents = f.read()

            soup_text = html_contents

            # Add tags to top
            # Find the position of the opening <body> tag
            body_tag_start = soup_text.find('<body>')
            soup_text = soup_text[:body_tag_start+6] + \
            """
            <nav class="menu">
                <ul>
                <li><a href="#">Home</a></li>
                <li><a href="#">About</a></li>
                <li><a href="#">Contact</a></li>
                </ul>
            </nav>
            <div id="content" class="content">
            """ + soup_text[body_tag_start+6:]

            # Add tags to bottom
            # Find the positions of the last two tags
            last_tag = soup_text.rfind('</html>')   
            second_last_tag = soup_text.rfind('</body>', 0, last_tag)

            print(last_tag, second_last_tag)
            # Remove the last two tags and replace them with new content
            soup_text = soup_text[:second_last_tag] + \
            """
                </div>
                    <script src="https://cpwebassets.codepen.io/assets/common/stopExecutionOnTimeout-2c7831bb44f98c1391d6a4ffda0e1fd302503391ca806e7fcc7b9b87197aec26.js"></script>
                    <script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.0/jquery.min.js'></script>
                    <script src='https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.1.3/css/bootstrap.min.css'></script>
                    <script src="../../javascript/script.js"></script>
                </body>
            </html>"""



            # Parse the HTML contents using BeautifulSoup
            soup = BeautifulSoup(soup_text, 'html.parser')

            # Find the existing menu element in the HTML file
            existing_menu = soup.find('nav', {'class': 'menu'})
            existing_head = soup.find('head')

            # Replace the existing menu element with the contents of the template file
            if existing_menu:
                new_menu = BeautifulSoup(template_menu_contents, 'html.parser').find('div', {'class': 'page-header-fixed page-sidebar-fixed'})
                print("found menu")
                if new_menu:
                    print("in_menu")
                    existing_menu.replace_with(new_menu)

            if existing_head:
                new_head = BeautifulSoup(template_head_contents, 'html.parser').find('head')
                print("found head")
                if new_head:
                    print("in_head")
                    existing_head.replace_with(new_head)



            # Save the updated HTML file to disk
            with open(os.path.join(dirpath, filename), 'w') as f:
                print("saving", dirpath, filename)
                f.write(str(soup))
