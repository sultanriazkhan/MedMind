import os

def list_healthcare_app_only():
    # Targets the healthcare_app folder relative to where you run the script
    target_folder = os.path.abspath('./healthcare_app')
    
    if not os.path.exists(target_folder):
        print(f"❌ Error: Could not find 'healthcare_app' folder at {target_folder}")
        return

    print(f"Scanning target directory: {target_folder}\n")
    print("=" * 60)

    for root, dirs, files in os.walk(target_folder):
        # Skip annoying python cache folders to keep the output clean
        if '__pycache__' in root:
            continue
            
        level = root.replace(target_folder, '').count(os.sep)
        indent = ' ' * 4 * level
        
        print(f"{indent}📁 Current Folder: {os.path.basename(root)}/")
        
        sub_indent = ' ' * 4 * (level + 1)
        if files:
            for file in files:
                print(f"{sub_indent}📄 {file}")
        else:
            print(f"{sub_indent}🔄 (No files in this folder)")
            
        print("-" * 60)

if __name__ == "__main__":
    list_healthcare_app_only()