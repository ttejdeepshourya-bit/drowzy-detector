import re

with open('app.py', encoding='utf-8') as f:
    content = f.read()

# Find start of HTML_CONTENT triple-quoted string
start_marker = 'HTML_CONTENT = """'
end_marker = '"""\n'

start_idx = content.find(start_marker)
if start_idx == -1:
    print("ERROR: HTML_CONTENT marker not found")
    exit(1)

html_start = start_idx + len(start_marker)
# Find the closing triple quote after the HTML
html_end = content.find('\n"""', html_start)
if html_end == -1:
    print("ERROR: closing triple-quote not found")
    exit(1)

html = content[html_start:html_end]

with open('index.html', 'w', encoding='utf-8') as out:
    out.write(html)

print(f"SUCCESS: index.html written ({len(html)} characters)")
