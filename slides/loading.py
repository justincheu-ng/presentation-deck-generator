import time
import threading

class Loading:
    
    def __init__(self, task):
        def print_dots():
            while self.is_loading:
                print('.',  end='', flush=True)
                time.sleep(1)
    
        print(task, end='', flush=True)
        self.is_loading = True
        self.thread = threading.Thread(target=print_dots)
        self.thread.start()
        
    def complete(self):
        self.is_loading = False
        self.thread.join()
        print('Done ✅')
