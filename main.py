"""
Main entry point for the Lottery Scraper API
Combines FastAPI server with background scheduler
"""

import uvicorn
import os
from dotenv import load_dotenv
from scheduler import start_scheduler

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Start the background scheduler
    scheduler = start_scheduler()
    
    # Start the FastAPI server
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    
    print(f"\nStarting API server on http://{host}:{port}")
    print(f"API Documentation available at http://localhost:{port}/docs")
    print(f"Press Ctrl+C to stop the server\n")
    
    try:
        uvicorn.run(
            "api:app",
            host=host,
            port=port,
            reload=False  # Set to True for development
        )
    except KeyboardInterrupt:
        print("\nShutting down...")
        scheduler.shutdown()
        print("Scheduler stopped")
