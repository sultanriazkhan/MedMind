# run_all.py
"""Start all services on correct ports"""
import subprocess
import time
import sys
import os
from pathlib import Path

def start_service(name, command, port, wait_time=3):
    """Start a service and wait"""
    print(f"\n🚀 Starting {name} on port {port}...")
    process = subprocess.Popen(command, shell=True)
    time.sleep(wait_time)
    print(f"   ✅ {name} started (PID: {process.pid})")
    return process

def main():
    print("="*60)
    print("🔧 Starting Pathology Report Processing System")
    print("="*60)
    
    processes = []
    base_dir = Path(__file__).parent
    
    # 1. Start AI Explainer on port 5001
    ai_path = base_dir / 'ai_explainer' / 'app.py'
    if ai_path.exists():
        processes.append(start_service("AI Explainer", f"python {ai_path}", 5001, 3))
    else:
        print(f"❌ AI Explainer not found at {ai_path}")
    
    # 2. Start Text Extractor on port 5000
    extractor_path = base_dir / 'text_extractor.py'
    if extractor_path.exists():
        processes.append(start_service("Text Extractor", f"python {extractor_path}", 5000, 3))
    else:
        print(f"❌ Text Extractor not found")
    
    # 3. Start Orchestrator on port 5002
    processes.append(start_service("Orchestrator", "python orchestrator.py", 5002, 3))
    
    print("\n" + "="*60)
    print("✅ ALL SERVICES STARTED")
    print("="*60)
    print("\n📍 Service Endpoints:")
    print("   📄 Text Extractor:    http://localhost:5000")
    print("   🤖 AI Explainer:      http://localhost:5001")
    print("   🚀 Orchestrator:      http://localhost:5002")
    print("\n📋 Test with curl:")
    print('   curl -X POST http://localhost:5002/process \\')
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{"text": "Hemoglobin 9.5 g/dL"}\'')
    print("\n🌐 Open browser: http://localhost:5000")
    print("="*60)
    print("\nPress Ctrl+C to stop all services\n")
    
    try:
        for p in processes:
            p.wait()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        for p in processes:
            p.terminate()
        print("✅ All services stopped")

if __name__ == "__main__":
    main()