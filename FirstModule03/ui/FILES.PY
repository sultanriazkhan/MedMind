import os

def create_folder_structure():
    backend_structure = {
        "backend": {
            "app": {
                "__init__.py": "",
                "config.py": "",
                "models": {
                    "__init__.py": "",
                    "user.py": "",
                    "report.py": "",
                    "token.py": "",
                    "health_profile.py": "",
                    "chat_session.py": "",
                    "recommendation.py": "",
                    "blog_post.py": "",
                    "blog_read.py": ""
                },
                "routes": {
                    "__init__.py": "",
                    "auth.py": "",
                    "reports.py": "",
                    "dashboard.py": "",
                    "chat.py": "",
                    "profile.py": "",
                    "recommendations.py": "",
                    "blog.py": ""
                },
                "services": {
                    "__init__.py": "",
                    "auth_service.py": "",
                    "report_analyzer.py": "",
                    "email_service.py": "",
                    "ai_service.py": "",
                    "recommendation_service.py": "",
                    "pdf_service.py": ""
                },
                "middleware": {
                    "__init__.py": "",
                    "auth_middleware.py": ""
                },
                "utils": {
                    "__init__.py": "",
                    "validators.py": ""
                }
            },
            "requirements.txt": "",
            ".env": "",
            "run.py": "",
            "uploads": {}
        }
    }
    
    frontend_structure = {
        "frontend": {
            "src": {
                "components": {
                    "ui": {
                        "Button.jsx": "",
                        "Card.jsx": "",
                        "Input.jsx": "",
                        "Modal.jsx": "",
                        "Skeleton.jsx": "",
                        "Badge.jsx": ""
                    },
                    "layout": {
                        "Sidebar.jsx": "",
                        "Header.jsx": "",
                        "ProtectedRoute.jsx": ""
                    },
                    "animations": {
                        "FadeIn.jsx": "",
                        "AnimatedContainer.jsx": ""
                    }
                },
                "pages": {
                    "Landing.jsx": "",
                    "SignUp.jsx": "",
                    "Login.jsx": "",
                    "ForgotPassword.jsx": "",
                    "Dashboard.jsx": "",
                    "UploadReport.jsx": "",
                    "ProcessingScreen.jsx": "",
                    "ReportAnalysis.jsx": "",
                    "TestExplanation.jsx": "",
                    "ReportHistory.jsx": "",
                    "HealthProfileSetup.jsx": "",
                    "LifestyleRecommendation.jsx": "",
                    "DietRecommendation.jsx": "",
                    "ExerciseRecommendation.jsx": "",
                    "HealthAIChat.jsx": "",
                    "ReportAwareChat.jsx": "",
                    "BlogListing.jsx": "",
                    "BlogReading.jsx": "",
                    "BlogSearch.jsx": "",
                    "UserProfile.jsx": "",
                    "Settings.jsx": ""
                },
                "stores": {
                    "authStore.js": "",
                    "reportStore.js": "",
                    "uiStore.js": "",
                    "profileStore.js": "",
                    "chatStore.js": "",
                    "recommendationStore.js": "",
                    "blogStore.js": "",
                    "settingsStore.js": "",
                    "themeStore.js": ""
                },
                "services": {
                    "api.js": "",
                    "authService.js": "",
                    "reportService.js": "",
                    "chatService.js": "",
                    "profileService.js": "",
                    "recommendationService.js": "",
                    "blogService.js": ""
                },
                "hooks": {
                    "useAuth.js": "",
                    "useToast.js": ""
                },
                "utils": {
                    "validators.js": ""
                },
                "App.jsx": "",
                "main.jsx": "",
                "index.css": ""
            },
            "index.html": "",
            "package.json": "",
            "vite.config.js": "",
            "tailwind.config.js": "",
            "postcss.config.js": "",
            ".env": "",
            ".gitignore": ""
        }
    }
    
    def create_structure(base_path, structure):
        for name, content in structure.items():
            path = os.path.join(base_path, name)
            
            if isinstance(content, dict):
                os.makedirs(path, exist_ok=True)
                print(f"📁 Created directory: {path}")
                create_structure(path, content)
            else:
                if not os.path.exists(path):
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"📄 Created file: {path}")
                else:
                    print(f"⚠️  File already exists: {path}")
    
    project_root = "healthcare-ai-app"
    os.makedirs(project_root, exist_ok=True)
    print(f"🏗️  Creating project in: {project_root}")
    print("-" * 50)
    
    print("\n🔧 Creating backend structure...")
    create_structure(project_root, backend_structure)
    
    print("\n🎨 Creating frontend structure...")
    create_structure(project_root, frontend_structure)
    
    root_files = {
        "README.md": "# Healthcare AI Application\n\n## Setup Instructions\n\n### Backend Setup\n```bash\ncd backend\npython -m venv venv\nsource venv/bin/activate\npip install -r requirements.txt\npython run.py\n```\n\n### Frontend Setup\n```bash\ncd frontend\nnpm install\nnpm run dev\n```\n\n## Features\n- AI-powered medical report analysis\n- Personalized health recommendations\n- AI chat assistant with report context\n- Diet and exercise planning\n- Blog system\n- User profile and settings\n",
        ".gitignore": "node_modules/\ndist/\n.env\n.DS_Store\n__pycache__/\n*.pyc\nvenv/\nenv/\nuploads/\n*.db\n*.sqlite\n*.sqlite3\n",
        "setup.sh": "#!/bin/bash\n\necho \"Setting up Healthcare AI Application...\"\n\ncd backend\npython3 -m venv venv\nsource venv/bin/activate\npip install --upgrade pip\npip install -r requirements.txt\ncd ..\n\ncd frontend\nnpm install\ncd ..\n\necho \"Setup complete!\"\necho \"To run backend: cd backend && source venv/bin/activate && python run.py\"\necho \"To run frontend: cd frontend && npm run dev\"\n",
        "setup.bat": "@echo off\necho Setting up Healthcare AI Application...\n\ncd backend\npython -m venv venv\ncall venv\\Scripts\\activate.bat\npip install --upgrade pip\npip install -r requirements.txt\ncd ..\n\ncd frontend\ncall npm install\ncd ..\n\necho Setup complete!\necho To run backend: cd backend && venv\\Scripts\\activate && python run.py\necho To run frontend: cd frontend && npm run dev\npause\n"
    }
    
    for filename, content in root_files.items():
        filepath = os.path.join(project_root, filename)
        if not os.path.exists(filepath):
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"📄 Created file: {filepath}")
    
    backend_env_example = """FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-super-secret-key-change-this
JWT_SECRET_KEY=your-jwt-secret-key-change-this
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=2592000
DATABASE_URL=sqlite:///healthcare.db
REDIS_URL=redis://localhost:6379
OPENAI_API_KEY=your-openai-api-key
SENDGRID_API_KEY=your-sendgrid-api-key
FRONTEND_URL=http://localhost:5173
"""
    
    frontend_env_example = """VITE_API_URL=http://localhost:5000/api
VITE_APP_NAME=MediScan AI
VITE_OPENAI_API_KEY=your-openai-api-key
"""
    
    env_example_path = os.path.join(project_root, "backend", ".env.example")
    if not os.path.exists(env_example_path):
        with open(env_example_path, 'w', encoding='utf-8') as f:
            f.write(backend_env_example)
        print(f"📄 Created file: {env_example_path}")
    
    env_example_path = os.path.join(project_root, "frontend", ".env.example")
    if not os.path.exists(env_example_path):
        with open(env_example_path, 'w', encoding='utf-8') as f:
            f.write(frontend_env_example)
        print(f"📄 Created file: {env_example_path}")
    
    package_json_content = """{
  "name": "healthcare-ai-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "axios": "^1.6.2",
    "zustand": "^4.4.7",
    "react-hook-form": "^7.48.2",
    "zod": "^3.22.4",
    "@hookform/resolvers": "^3.3.2",
    "framer-motion": "^10.16.16",
    "lucide-react": "^0.303.0",
    "@tanstack/react-table": "^8.11.2",
    "recharts": "^2.10.3",
    "react-dropzone": "^14.2.3",
    "sonner": "^1.3.1",
    "date-fns": "^3.0.6",
    "react-intersection-observer": "^9.5.3",
    "react-markdown": "^9.0.1"
  },
  "devDependencies": {
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32",
    "tailwindcss": "^3.3.6",
    "vite": "^5.0.8"
  }
}"""
    
    package_json_path = os.path.join(project_root, "frontend", "package.json")
    if not os.path.exists(package_json_path):
        with open(package_json_path, 'w', encoding='utf-8') as f:
            f.write(package_json_content)
        print(f"📄 Created file: {package_json_path}")
    
    requirements_content = """Flask==2.3.3
Flask-CORS==4.0.0
Flask-SQLAlchemy==3.0.5
Flask-Migrate==4.0.5
PyJWT==2.8.0
bcrypt==4.0.1
python-dotenv==1.0.0
Werkzeug==2.3.7
Pillow==10.0.0
PyPDF2==3.0.1
python-docx==1.0.0
redis==5.0.0
celery==5.3.1
sendgrid==6.10.0
openai==1.3.0
reportlab==4.0.4
"""
    
    requirements_path = os.path.join(project_root, "backend", "requirements.txt")
    if not os.path.exists(requirements_path):
        with open(requirements_path, 'w', encoding='utf-8') as f:
            f.write(requirements_content)
        print(f"📄 Created file: {requirements_path}")
    
    print("\n" + "="*50)
    print("✅ Complete folder structure created successfully!")
    print("="*50)
    print("\n📂 Total files created:")
    print("   - Backend: 30+ files")
    print("   - Frontend: 50+ files")
    print("\n🎯 Includes ALL screens (1-21):")
    print("   - Authentication (Login/Signup/Forgot Password)")
    print("   - Landing Page & Dashboard")
    print("   - Report Upload & Analysis")
    print("   - Health Profile Setup (Multi-step)")
    print("   - Lifestyle/Diet/Exercise Recommendations")
    print("   - AI Chat (Standard & Report-Aware)")
    print("   - Complete Blog System")
    print("   - User Profile & Settings")
    print("\n📂 Project created at:", os.path.abspath(project_root))
    print("\nNext steps:")
    print("1. cd healthcare-ai-app")
    print("2. Copy the code from the prompts into respective files")
    print("3. Run: ./setup.sh (Mac/Linux) or setup.bat (Windows)")
    print("\n🚀 Ready for production!")

if __name__ == "__main__":
    create_folder_structure()