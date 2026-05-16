import os

def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        # Exclude hidden folders like .git or __pycache__
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print(f'{indent}{os.path.basename(root)}/')
        
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            # Exclude hidden files
            if not f.startswith('.'):
                print(f'{subindent}{f}')

if __name__ == "__main__":
    # '.' refers to the current directory where you run the script
    list_files('.')