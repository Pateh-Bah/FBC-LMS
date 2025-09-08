from waitress import serve
from library_system.wsgi import application
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Get port from environment or default to 8000
    port = int(os.getenv("PORT", "8000"))

    print(f"Starting production server on port {port}...")
    serve(application, host="127.0.0.1", port=port, threads=4)
