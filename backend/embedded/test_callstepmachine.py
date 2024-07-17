import threading
from stepmachine import JukeboxStateMachine
import time

if __name__ == '__main__':
    jukebox = JukeboxStateMachine()
    jukebox_thread = threading.Thread(target=jukebox.transition)
    jukebox_thread.start()
    
    time.sleep(10)
    jukebox.nextCD = 1
    jukebox.set_state("GOTOPOS")
    
    time.sleep(10)
    jukebox.set_state("CLOSE")
    
    jukebox_thread.join()  # Ensure the thread has completed before exiting
