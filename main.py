import time
import threading
import schedule

from Play_Script import run_game
from WebServer import run_website

def job():
    run_game()

# Schedule the scraper job
schedule.every().day.at("02:00").do(job)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    # The web server is the primary service keeping the container alive
    web_server_thread = threading.Thread(target=run_website)
    web_server_thread.start()

    # Start the scheduler loop in the main thread
    run_scheduler()