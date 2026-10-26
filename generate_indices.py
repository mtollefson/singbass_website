import os

# Script Version
VERSION = "1.2.0"

# File extensions natively displayable by modern web browsers
NATIVE_DISPLAYABLE = {
    '.txt', '.md', '.html', '.htm', '.css', '.js', '.json', 
    '.png', '.jpg', '.jpeg', '.gif', '.svg', '.pdf', '.csv', '.xml'
}

# File extensions supported by Google Docs Viewer (.docx, .xlsx, etc.)
GDOCS_DISPLAYABLE = {
    '.docx', '.doc', '.xlsx', '.xls', '.pptx', '.ppt'
}

def generate_link_lines(filename):
    """
    Separate function to generate the HTML link string(s) for a given file.
    - Natively viewable files get a direct 'View' and 'Download' link.
    - Google Docs compatible files get a 'View (Google Docs)' and 'Download' link.
    - Other files get ONLY a 'Download' link.
    """
    _, ext = os.path.splitext(filename.lower())
    
    # Every file gets a download link
    download_link = f'<a href="{filename}" download class="btn-download">Download</a>'
    
    if ext in NATIVE_DISPLAYABLE:
        view_link = f'<a href="{filename}" target="_blank" class="btn-view">View</a>'
        return f'{view_link} {download_link}'
    elif ext in GDOCS_DISPLAYABLE:
        # Uses data-file so JavaScript can dynamically construct the absolute Google Docs URL
        gdocs_link = f'<a href="#" class="btn-gdocs dynamic-gdocs" data-file="{filename}">View (Google Docs)</a>'
        return f'{gdocs_link} {download_link}'
    else:
        return download_link

def create_directory_indexes(root_dir):
    """
    Walks through all subdirectories, skipping the root directory itself,
    hidden subdirectories (like .git), and builds an index.html file for each valid subdirectory.
    """
    root_dir = os.path.abspath(root_dir)
    
    for current_path, dirs, files in os.walk(root_dir):
        # Prune hidden subdirectories (e.g., .git, .vscode) in-place so os.walk ignores them entirely
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        # 1. Do not modify or create an index.html in the root (current) directory
        if current_path == root_dir:
            continue
            
        rel_path = os.path.relpath(current_path, root_dir)
        
        # 2. Check if the subdirectory contains the exclusion flag file
        if 'donotchangeindex.txt' in files:
            print(f"Skipping (found donotchangeindex.txt): {rel_path}")
            continue
            
        subdir_name = os.path.basename(current_path)
        print(f"Processing subdirectory: {rel_path}")
        
        # Filter out system files so they don't list themselves
        files_to_list = [f for f in files if f.lower() not in ('index.html', 'donotchangeindex.txt')]
        files_to_list.sort()
        
        # Construct the HTML structure
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{subdir_name}</title>
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon.png">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f9f9f9; color: #333; }}
        .nav-up {{ margin-bottom: 20px; display: inline-block; text-decoration: none; color: #007bff; font-weight: bold; }}
        .nav-up:hover {{ text-decoration: underline; }}
        h2 {{ border-bottom: 2px solid #ddd; padding-bottom: 10px; margin-top: 0; }}
        table {{ width: 100%; border-collapse: collapse; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        th, td {{ padding: 12px 15px; border-bottom: 1px solid #eee; text-align: left; }}
        th {{ background-color: #f4f4f4; }}
        .actions a {{ 
            text-decoration: none; 
            padding: 6px 12px; 
            border-radius: 4px; 
            font-size: 14px; 
            margin-right: 6px; 
            display: inline-block;
        }}
        .btn-view {{ background-color: #007bff; color: white; }}
        .btn-view:hover {{ background-color: #0056b3; }}
        .btn-gdocs {{ background-color: #6c757d; color: white; }}
        .btn-gdocs:hover {{ background-color: #5a6268; }}
        .btn-download {{ background-color: #28a745; color: white; }}
        .btn-download:hover {{ background-color: #1e7e34; }}
    </style>
</head>
<body>

    <!-- Link to go up to the parent directory -->
    <a href="../index.html" class="nav-up">&larr; Up to Parent Directory</a>

    <!-- Display the subdirectory name at the top -->
    <h2>{subdir_name}</h2>

    <table>
        <thead>
            <tr>
                <th>File Name</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
"""
        
        # Populate table rows
        if not files_to_list:
            html_content += """            <tr>
                <td colspan="2" style="text-align: center; color: #777;">No files found in this directory.</td>
            </tr>
"""
        else:
            for file in files_to_list:
                action_links = generate_link_lines(file)
                html_content += f"""            <tr>
                <td>{file}</td>
                <td class="actions">{action_links}</td>
            </tr>
"""

        html_content += """        </tbody>
    </table>

    <!-- Script to dynamically generate Google Docs Viewer absolute URLs when hosted on GitHub Pages -->
    <script>
        document.querySelectorAll('.dynamic-gdocs').forEach(link => {
            const fileName = link.getAttribute('data-file');
            const absoluteUrl = new URL(fileName, window.location.href).href;
            link.href = `https://docs.google.com/viewer?url=${encodeURIComponent(absoluteUrl)}`;
            link.target = '_blank';
        });
    </script>

</body>
</html>
"""
        
        # Write the index.html file to the subdirectory with error handling
        index_file_path = os.path.join(current_path, 'index.html')
        try:
            with open(index_file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"  -> Created: {index_file_path}")
        except IOError as e:
            print(f"  [Error] Could not write index.html in {current_path}: {e}")

if __name__ == '__main__':
    current_dir = os.getcwd()
    print(f"=== GitHub Subdirectory Index Generator v{VERSION} ===")
    print(f"Starting script in root directory: {current_dir}")
    print("Safeguard active: root index.html and hidden directories (like .git) will NOT be modified/indexed.\n")
    
    try:
        create_directory_indexes(current_dir)
        print("\nProcess completed successfully!")
    except Exception as e:
        print(f"\n[Fatal Error] An unexpected error occurred: {e}")
        