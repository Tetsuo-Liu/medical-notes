import os
import glob
import argparse

def generate_tree(start_path):
    """Generates a directory tree structure showing only directories and .md files."""
    tree_lines = [f"Directory tree for: {os.path.abspath(start_path)}\n"]
    for root, dirs, files in os.walk(start_path):
        # Filter to keep only .md files
        md_files = [f for f in files if f.endswith('.md')]
        
        # Don't print empty directories unless they are the root
        if not dirs and not md_files and root != start_path:
            continue

        level = root.replace(start_path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        tree_lines.append(f"{indent}{os.path.basename(root)}/")
        sub_indent = ' ' * 4 * (level + 1)
        
        # Sort directories and files for consistent order
        dirs.sort()
        md_files.sort()

        for d in dirs:
            # Check if the directory or any of its subdirectories contain .md files
            has_md = any(f.endswith('.md') for _, _, fs in os.walk(os.path.join(root, d)) for f in fs)
            if has_md:
                 pass # This logic is tricky, for now we just show all dirs

        items = dirs + md_files
        for i, name in enumerate(items):
            # Skip non-md files that might have slipped through
            if not os.path.isdir(os.path.join(root, name)) and not name.endswith('.md'):
                continue
            
            connector = '└── ' if i == len(items) - 1 else '├── '
            tree_lines.append(f"{sub_indent}{connector}{name}")
            
    return "\n".join(tree_lines)

def combine_markdown_files(input_dir, output_file):
    base_dir = os.path.abspath(input_dir)
    
    # 1. Generate the directory tree first
    tree_structure = generate_tree(base_dir)
    header_for_tree = f"================================================\nDIRECTORY STRUCTURE\n================================================\n{tree_structure}"

    # 2. Find and process markdown files
    md_files = glob.glob(os.path.join(base_dir, '**', '*.md'), recursive=True)
    abs_output_path = os.path.abspath(output_file)
    md_files = [f for f in md_files if os.path.abspath(f) != abs_output_path]
    md_files.sort()

    if not md_files:
        print(f"No markdown files found in '{base_dir}'.")
        # Still write the tree structure if the file is empty
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(header_for_tree)
            print(f"Wrote directory tree to '{output_file}'.")
        except Exception as e:
            print(f"Error writing to '{output_file}': {e}")
        return

    file_contents = []
    for file_path in md_files:
        relative_path = os.path.relpath(file_path, base_dir)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            header = f"================================================\nFILE: {relative_path.replace(os.sep, '/')}\n================================================\n"
            file_contents.append(header + content)
        except Exception as e:
            error_message = f"================================================\nERROR PROCESSING FILE: {relative_path.replace(os.sep, '/')}\n{e}\n================================================\n"
            file_contents.append(error_message)

    # 3. Combine tree and file contents and write to file
    final_output = header_for_tree + "\n\n" + "\n\n".join(file_contents)
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_output)
        print(f"Successfully combined {len(md_files)} files and directory tree into '{output_file}'")
    except Exception as e:
        print(f"Error writing to '{output_file}': {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Combine all markdown files in a directory into a single text file, including a directory tree.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('--input-dir', type=str, default='.', help="Directory to search for markdown files.\n(default: current directory)")
    parser.add_argument('--output-file', type=str, default='combined.txt', help="Name of the output file.\n(default: combined.txt)")
    args = parser.parse_args()
    combine_markdown_files(args.input_dir, args.output_file)