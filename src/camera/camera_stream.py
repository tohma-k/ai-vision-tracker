import cv2
import threading

class CameraStream:
    def __init__(self, camera_index=1):
        self.cap = cv2.VideoCapture(camera_index)
        
        if not self.cap.isOpened():
            raise RuntimeError(
                f"Could not open webcam at index {camera_index}"
            )
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        self.ret = False
        self.frame = None
        
        self.running = True
        
        self.thread = threading.Thread(
            target=self.update,
            daemon=True
        )
        
    def start(self):
        self.thread.start()
        return self
    
    def update(self):
        while self.running:
            self.ret, self.frame = self.cap.read()
            
    def read(self):
        return self.ret, self.frame
    
    def stop(self):
        self.running = False
        self.thread.join()
        self.cap.release()