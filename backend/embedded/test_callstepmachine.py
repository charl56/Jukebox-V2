import threading
from stepmachine import JukeboxStateMachine
import time

if __name__ == '__main__':
    jukebox = JukeboxStateMachine()
    jukebox_thread = threading.Thread(target=jukebox.transition)
    jukebox_thread.start()
    
    time.sleep(10)
    jukebox.nextCD = 1
    jukebox.set_state("GoToPos")
    
    time.sleep(10)
    jukebox.set_state("Close")
    
    jukebox_thread.join()  # Ensure the thread has completed before exiting
