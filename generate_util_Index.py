#!/usr/bin/env python3
"""
Directory Index Generator for GitHub
Version: 1.2.0
Author: AI Assistant
Date: October 2026

Description:
This script recursively traverses down into all subdirectories and sub-subdirectories.
In each subdirectory, it generates an 'index.html' file listing its contents.

Updates in v1.2.0:
- Explicitly skips generating an index.html file in the root folder to protect your homepage.
"""

import os
import sys
import html
import logging

# Configure logging safely for all OS environments
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

VERSION = "1.2.0"

def should_ignore(name: str) -> bool:
    """
    Determines if a file or directory should be ignored.
    Filters out hidden files/folders (starting with '.') and common system artifacts.
    """
    if name.startswith('.'):
        return True
    
    ignored_names = {'node_modules', '__pycache__', 'Thumbs.db'}
    if name in ignored_names:
        return True
        
    return False

def generate_index_html(dir_path: str) -> None:
    """
    Generates an index.html file in a subdirectory containing links
    to non-hidden files and folders.
    """
    index_file_path = os.path.join(dir_path, "index.html")
    
    try:
        try:
            raw_items = os.listdir(dir_path)
        except PermissionError:
            logging.warning(f"Permission denied: {dir_path}. Skipping.")
            return
        except FileNotFoundError:
            logging.error(f"Directory not found: {dir_path}. Skipping.")
            return

        items = [item for item in raw_items if not should_ignore(item) and item != "index.html"]
        items.sort(key=lambda s: s.lower())

        display_name = html.escape(os.path.basename(os.path.abspath(dir_path)) or dir_path)
        
        html_content = [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            f"    <title>Index of {display_name}</title>",
            "    <meta charset='utf-8'>",
            "    <style>",
            "        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 40px; background-color: #f9f9f9; color: #333; }",
            "        h1 { font-size: 1.5rem; border-bottom: 1px solid #ccc; padding-bottom: 10px; }",
            "        ul { list-style-type: none; padding: 0; }",
            "        li { padding: 8px 0; border-bottom: 1px solid #eee; }",
            "        a { color: #0066cc; text-decoration: none; font-size: 1.1rem; }",
            "        a:hover { text-decoration: underline; }",
            "        .parent-dir { font-weight: bold; color: #d9534f; }",
            "    </style>",
            "</head>",
            "<body>",
            f"    <h1>Index of {display_name}</h1>",
            "    <ul>",
            "        <li><a class='parent-dir' href='..'>.. (Up one level)</a></li>" # Subdirectories always have a parent
        ]

        for item in items:
            full_item_path = os.path.join(dir_path, item)
            is_dir = os.path.isdir(full_item_path)
            display_item_name = f"{item}/" if is_dir else item
            
            escaped_href = html.escape(item)
            escaped_text = html.escape(display_item_name)
            
            download_attr = "" if is_dir else " download"
            html_content.append(f"        <li><a href='{escaped_href}'{download_attr}>{escaped_text}</a></li>")

        html_content.extend([
            "    </ul>",
            "</body>",
            "</html>"
        ])

        with open(index_file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(html_content))
            
        logging.info(f"Generated index: {index_file_path}")

    except Exception as e:
        logging.error(f"Error handling index in {dir_path}: {str(e)}")


def main() -> None:
    """
    Main directory crawler loop.
    """
    root_dir = os.getcwd()
    logging.info(f"Starting Subdirectory Index Generator v{VERSION}")
    logging.info(f"Targeting Subdirectories beneath: {root_dir}")

    for root, dirs, files in os.walk(root_dir, topdown=True):
        dirs[:] = [d for d in dirs if not should_ignore(d)]
        
        # Check if current folder is the main execution root directory
        if os.path.abspath(root) == os.path.abspath(root_dir):
            logging.info("Skipping root folder to preserve welcome homepage.")
            continue  # Do not generate an index.html here, proceed to sub-folders
            
        generate_index_html(root)

    logging.info("Process finished successfully.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.warning("\nProcess aborted by user.")
        sys.exit(1)
