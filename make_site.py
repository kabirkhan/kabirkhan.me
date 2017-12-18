# Load library
import os

# Create path to content
path = 'content/'

# Find all jupyter notebooks in all content folders
all_ipynb_files = [os.path.join(root, name)
                   for root, dirs, files in os.walk(path)
                   for name in files
                   if name.endswith((".ipynb"))]

# Remove all notebooks from checkpoint folders
files = [ x for x in all_ipynb_files if ".ipynb_checkpoints" not in x ]

# For each file
for file in files:
    # Convert into markdown
    os.system('jupyter nbconvert --to markdown {file}'.format(file=file))
    
    # Open markdown, delete first row, save markdown
    markdown_file = file.replace('.ipynb', '.md')
    with open(markdown_file, 'r') as fin:
        data = fin.read().splitlines(True)
    with open(markdown_file, 'w') as fout:
        fout.writelines(data[1:])

# Compile site
generate_site = os.system('pelican content -o output -s pelicanconf.py')

# If no error:
if generate_site == 0:
    # Print action
    print('No errors found during site generation, deploying to Github Pages')
    
    # Publish site to github
    os.system('ghp-import output')
    os.system('git push origin gh-pages')
# Otherwise:
else:
    # Print error
    print('Error found during site generation, halting deployment')

