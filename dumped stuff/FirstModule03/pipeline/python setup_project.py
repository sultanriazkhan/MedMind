import os
from pathlib import Path

def create_healthcare_app_structure():
    # Define the base directory (relative to where you run this script)
    root = Path("healthcare_app")

    # Define all directories and files
    # Folders are keys, lists of files are values
    structure = {
        "app/static/css": ["main.css", "animations.css", "variables.css"],
        "app/static/js": ["main.js", "sidebar.js", "animations.js", "theme.js"],
        "app/static/images": [".gitkeep"],
        "app/static/icons": [".gitkeep"],
        "app/templates/layouts": ["base.html"],
        "app/templates/auth": ["login.html", "signup.html", "forgot_password.html"],
        "app/templates/home": ["landing.html"],
        "app/templates/dashboard": ["dashboard.html"],
        "app/templates/reports": [
            "upload_report.html", "processing.html", 
            "analysis_overview.html", "test_explanation.html", 
            "report_history.html"
        ],
        "app/templates/lifestyle": [
            "health_profile.html", "recommendations.html", 
            "diet.html", "exercise.html"
        ],
        "app/templates/ai_chat": ["health_chat.html", "report_aware_chat.html"],
        "app/templates/blogs": ["blog_listing.html", "blog_reading.html", "blog_search.html"],
        "app/templates/user": ["profile.html", "settings.html"],
        "app/routes": [
            "__init__.py", "auth.py", "home.py", "dashboard.py", 
            "reports.py", "lifestyle.py", "ai_chat.py", "blogs.py", "user.py"
        ],
        "app": ["__init__.py", "config.py", "models.py"],
        ".": ["run.py", "requirements.txt", "README.md"]
    }

    print(f"🚀 Creating project structure in: {root.absolute()}")

    for folder, files in structure.items():
        # Create the directory path
        target_dir = root / folder
        target_dir.mkdir(parents=True, exist_ok=True)

        for file in files:
            # Create the empty file
            file_path = target_dir / file
            file_path.touch()
            print(f"  ✅ Created: {folder}/{file}")

    print("\n✨ All done! Your healthcare app skeleton is ready.")

if __name__ == "__main__":
    create_healthcare_app_structure()