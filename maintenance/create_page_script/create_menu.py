from bs4 import BeautifulSoup

# Define the HTML contents of the <head> element
head_contents_filename   = "templates\head.html"
js_contents_filename     = "templates\js.html"
menu_contents_filename   = "templates\menu_stub.html"

with open(head_contents_filename, encoding='utf-8') as f:
    head_contents = f.read()

with open(js_contents_filename, encoding='utf-8') as f:
    js_contents = f.read()

with open(menu_contents_filename, encoding='utf-8') as f:
    menu_contents = f.read()


html = BeautifulSoup('', 'html.parser')

# Set the content type to "text/html"
html['content-type'] = 'text/html'



# Create a new <head> element and append it to the <html> element
head = html.new_tag('head')
head.append(BeautifulSoup(head_contents, 'html.parser'))
html.append(head)

body = html.new_tag('body')
html.append(body)
body.append(BeautifulSoup(js_contents, 'html.parser'))

# Save the HTML document to a file
with open('my_new_page.html', 'w') as f:
    f.write(str(html))
