@echo off
echo Setting up Healthcare AI Application...

echo Setting up backend...
cd backend
python -m venv venv
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
cd ..

echo Setting up frontend...
cd frontend
call npm install
cd ..

echo Setup complete!
echo To run backend: cd backend && venv\Scripts\activate && python run.py
echo To run frontend: cd frontend && npm run dev
pause
