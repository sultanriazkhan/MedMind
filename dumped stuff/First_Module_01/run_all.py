import os
import webbrowser
import threading
import time
import uvicorn

def open_browser():
    time.sleep(3)
    webbrowser.open("http://localhost:8000/docs")

if __name__ == "__main__":

    print("\n" + "="*60)
    print("🧠 MedMind Starting...")
    print("="*60)

    threading.Thread(target=open_browser).start()

    uvicorn.run(
        "main:api_app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        workers=1
    )