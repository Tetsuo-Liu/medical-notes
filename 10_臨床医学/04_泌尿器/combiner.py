import os
import glob

# Define the target directory
target_dir = '.'
base_dir = os.path.abspath(target_dir)
output_file = 'combined.txt'

# Find all markdown files recursively
md_files = glob.glob(os.path.join(target_dir, '**', '*.md'), recursive=True)

# Sort files alphabetically for consistent order
md_files.sort()

final_content = []

for file_path in md_files:
    # Make the path relative to the base directory
    relative_path = os.path.relpath(file_path, base_dir)
    
    # Skip the script itself if it happens to be a markdown file
    if os.path.basename(file_path) == 'combiner.py':
        continue

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Use forward slashes for path in the header, as in the example
        header = f"================================================\nFILE: {relative_path.replace(os.sep, '/')}\n================================================\n"
        final_content.append(header + content)
        
    except Exception as e:
        error_message = f"================================================\nERROR PROCESSING FILE: {relative_path.replace(os.sep, '/')}\n{e}\n================================================\n"
        final_content.append(error_message)

# Write the combined content to the output file
try:
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(final_content))
    print(f"Successfully combined {len(md_files)} files into {output_file}")
except Exception as e:
    print(f"Error writing to {output_file}: {e}")