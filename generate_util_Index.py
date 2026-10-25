import os

# Define paths relative to this script
util_dir = os.path.join(os.path.dirname(__file__), 'util')
output_file = os.path.join(util_dir, 'index.html')

# Check if directory exists
if not os.path.exists(util_dir):
    print(f"Error: The directory '{util_dir}' does not exist.")
    print("Please make sure you run this script next to your 'util' folder.")
    exit(1)

try:
    # Scan directory and filter out index.html and hidden system files
    files = os.listdir(util_dir)
    file_list = [f for f in files if f != 'index.html' and not f.startswith('.')]
    
    # Sort files alphabetically
    file_list.sort()

    # Generate the <li> elements
    if file_list:
        list_items = "\n".join([f'            <li><a href="{f}" download class="download-link">{f}</a></li>' for f in file_list])
    else:
        list_items = '            <li style="color: #57606a; font-style: italic;">No tools found in this directory.</li>'

    # Build template with home link and custom title
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Useful Tools</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 40px; background: #f6f8fa; color: #24292f; }}
        .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; padding: 32px; border: 1px solid #d0d7de; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
        .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; padding-bottom: 8px; border-bottom: 1px solid #d0d7de; }}
        h1 {{ font-size: 24px; margin: 0; }}
        .home-link {{ text-decoration: none; color: #57606a; font-size: 14px; font-weight: 500; }}
        .home-link:hover {{ color: #0969da; text-decoration: underline; }}
        ul {{ list-style: none; padding: 0; margin: 0; }}
        li {{ padding: 12px 12px; border-bottom: 1px solid #d0d7de; display: flex; align-items: center; }}
        li:last-child {{ border-bottom: none; }}
        a.download-link {{ text-decoration: none; color: #0969da; font-weight: 500; word-break: break-all; }}
        a.download-link:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Useful Tools</h1>
            <a href="../" class="home-link">← Back to Home</a>
        </div>
        <ul>
{list_items}
        </ul>
    </div>
</body>
</html>'''

    # Write file out safely with UTF-8 encoding
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print(f"Success! Generated index.html inside '{util_dir}' with {len(file_list)} files.")

except Exception as e:
    print(f"An error occurred: {e}")
