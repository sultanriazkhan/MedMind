# show_structure.py
"""Display complete folder and file structure of the project"""
import os
from pathlib import Path

def show_structure(start_path, indent="", exclude_folders=None, exclude_files=None):
    """
    Recursively display folder and file structure
    
    Args:
        start_path: Root path to start from
        indent: Current indentation string
        exclude_folders: List of folder names to exclude
        exclude_files: List of file patterns to exclude
    """
    if exclude_folders is None:
        exclude_folders = ['__pycache__', '.git', '.vscode', 'uploads', '.pytest_cache', 'venv', 'env', '.venv']
    
    if exclude_files is None:
        exclude_files = ['.pyc', '.db-shm', '.db-wal', '.DS_Store']
    
    start_path = Path(start_path)
    
    # Get all items in current directory
    items = list(start_path.iterdir())
    
    # Separate folders and files
    folders = [item for item in items if item.is_dir() and item.name not in exclude_folders]
    files = [item for item in items if item.is_file() and not any(item.name.endswith(ext) for ext in exclude_files)]
    
    # Sort alphabetically
    folders.sort(key=lambda x: x.name)
    files.sort(key=lambda x: x.name)
    
    # Display folders
    for i, folder in enumerate(folders):
        is_last = (i == len(folders) - 1 and len(files) == 0)
        prefix = "└── " if is_last else "├── "
        print(f"{indent}{prefix}{folder.name}/")
        
        # Recursively show subfolder structure
        new_indent = indent + ("    " if is_last else "│   ")
        show_structure(folder, new_indent, exclude_folders, exclude_files)
    
    # Display files
    for i, file in enumerate(files):
        is_last = (i == len(files) - 1)
        prefix = "└── " if is_last else "├── "
        print(f"{indent}{prefix}{file.name}")

def show_structure_simple(start_path):
    """Simple line-by-line structure without tree characters"""
    start_path = Path(start_path)
    
    for root, dirs, files in os.walk(start_path):
        # Skip excluded folders
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', '.vscode', 'uploads', '.pytest_cache']]
        
        # Get relative path
        rel_path = os.path.relpath(root, start_path)
        if rel_path == '.':
            print(f"\n📁 {os.path.basename(start_path)}/")
        else:
            indent = "  " * (rel_path.count(os.sep))
            print(f"{indent}📁 {os.path.basename(root)}/")
            
            # Print files
            for file in sorted(files):
                if not file.endswith(('.pyc', '.db-shm', '.db-wal')):
                    print(f"{indent}  📄 {file}")
    
    print("\n" + "="*60)

def create_file_structure_report(start_path, output_file="structure_report.txt"):
    """Create a text report of folder structure"""
    start_path = Path(start_path)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write(f"PROJECT STRUCTURE REPORT\n")
        f.write(f"Root: {start_path.absolute()}\n")
        f.write("="*60 + "\n\n")
        
        for root, dirs, files in os.walk(start_path):
            # Skip excluded folders
            dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', '.vscode', 'uploads', '.pytest_cache']]
            
            # Get relative path
            rel_path = os.path.relpath(root, start_path)
            if rel_path == '.':
                f.write(f"📁 {os.path.basename(start_path)}/\n")
            else:
                indent = "  " * (rel_path.count(os.sep))
                f.write(f"{indent}📁 {os.path.basename(root)}/\n")
                
                # Write files
                for file in sorted(files):
                    if not file.endswith(('.pyc', '.db-shm', '.db-wal')):
                        f.write(f"{indent}  📄 {file}\n")
        
        f.write("\n" + "="*60 + "\n")
        f.write(f"Report generated on: {__import__('datetime').datetime.now()}\n")
        f.write("="*60 + "\n")
    
    print(f"\n✅ Structure report saved to: {output_file}")

if __name__ == "__main__":
    # Get current directory (where script is run from)
    current_dir = Path.cwd()
    
    print("\n" + "="*60)
    print("📁 PROJECT STRUCTURE DISPLAY")
    print("="*60)
    print(f"Current Directory: {current_dir}")
    print("="*60 + "\n")
    
    # Option 1: Tree-like display
    print("🌲 TREE VIEW:\n")
    show_structure(current_dir)
    
    print("\n" + "="*60 + "\n")
    
    # Option 2: Simple line-by-line display
    print("📋 SIMPLE VIEW:\n")
    show_structure_simple(current_dir)
    
    # Option 3: Save to file
    create_file_structure_report(current_dir, "structure_report2.txt")
    
    print("\n✅ Done!")
    print("   - Tree view shown above")
    print("   - Simple view shown above")
    print("   - Full report saved to: structure_report.txt")