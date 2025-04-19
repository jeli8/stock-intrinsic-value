import schedule
import time
import subprocess
from datetime import datetime
import sys

def run_analysis():
    if datetime.now().weekday() < 5:  # Only run on weekdays
        print(f"Running stock analysis at {datetime.now()}")
        subprocess.run([sys.executable, "main.py"])
        print("Analysis complete")

def main():
    # Schedule job at 16:00 UTC (market close)
    schedule.every().day.at("16:00").do(run_analysis)
    
    print("Scheduler started. Will run stock analysis daily at 16:00 UTC on weekdays.")
    print("Keep this script running to maintain scheduling.")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main() 
