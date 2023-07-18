import threading
import time
 
# Set the resource to False initially
shared_resource = False
 # A lock for the shared resource
lock = threading.Lock()
 
def perform_computation():
     
    # Thread A will call this function and manipulate the resource
    print(f'Thread {threading.currentThread().name} - performing some computation....')
    shared_resource = True
    print(f'Thread {threading.currentThread().name} - set shared_resource to True!')
    print(f'Thread {threading.currentThread().name} - Finished!')
    time.sleep(1)
 
def monitor_resource():
    # Thread B will monitor the shared resource
    while shared_resource == False:
        time.sleep(1)
    print(f'Thread {threading.currentThread().name} - Detected shared_resource = False')
    time.sleep(1)
    print(f'Thread {threading.currentThread().name} - Finished!')
 
 
if __name__ == '__main__':
    a = threading.Thread(target=perform_computation, name='A')
    b = threading.Thread(target=monitor_resource, name='B')
 
    # Now start both threads
    a.start()
    b.start()