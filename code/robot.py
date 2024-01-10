import time

class Robot:
    def __init__(self,screen):
        self.screen=screen
    
    def run_robot(self):
        self.screen.thread_screen_start()
        time.sleep(5)
        self.screen.thread_screen_stop()
                
