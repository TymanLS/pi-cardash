#!/usr/bin/python3

############################################################
# pi-cardash: dashcam module
# Written by: Tyman Sin (ts835)
############################################################

### Import modules
import os
import datetime
import threading
import picamera

### Dashcam: a class to hold information about the camera module
class Dashcam:
    def __init__(self, width:int=800, height:int=480, resolution:tuple=(800, 480), framerate:int=30, cliplen:int=60, vid_dir=os.path.dirname(os.path.realpath(__file__))):
        self.__width = width
        self.__height = height
        self.__camera = picamera.PiCamera()
        self.__resolution = resolution
        self.__framerate = framerate
        self.__clip_len = cliplen
        self.__vid_dir = vid_dir
        self.__stop_flag = threading.Event()

    # Call __record in a thread
    def record(self):
        self.cam_thread = threading.Thread(target=self.__record, args=())
        self.cam_thread.start()

    # Set the __stop_flag
    def stop(self):
        self.__stop_flag.set()

    # Record dashcam footage into clips, should be called in a thread
    def __record(self):
        # Clear the __stop_flag
        self.__stop_flag.clear()

        # Determine the file name
        vid_name = datetime.datetime.now().isoformat(timespec='seconds')
        capture_dir = os.path.join(self.__vid_dir, vid_name)
        os.makedirs(capture_dir, exist_ok=True)
        clip = 1

        try:
            # Set camera params
            self.__camera.resolution = self.__resolution
            self.__camera.framerate = self.__framerate

            print("Dashcam: Started Recording")
            self.__camera.start_recording(os.path.join(capture_dir, f"{vid_name}_0.h264"))

            # Keep recording as long as __stop_flag is not set
            counter = 0
            while not self.__stop_flag.wait(timeout=0):
                # Count how long the clip is
                counter+=1
                self.__camera.wait_recording(1)
                print(f"Dashcam: Recording {counter}")

                # Cut the clip if it is longer than __clip_len
                if counter >= self.__clip_len:
                    print("Dashcam: Cutting clip")
                    self.__camera.split_recording(os.path.join(capture_dir, f"{vid_name}_{clip}.h264"))
                    clip+=1
                    counter = 0

            self.__camera.stop_recording()
            print("Dashcam: Stopped Recording")

        except:
            self.__camera.stop_recording()

        finally:
            self.__stop_flag.clear()
            if self.__camera.recording:
                print("Camera failed to stop recording...")

    # Show the camera preview with top-left at (x, y)
    def show(self, x:int, y:int):
        self.__camera.start_preview(fullscreen=False, window=(x, y, self.__width, self.__height))

    # Hide the camera preview
    def hide(self):
        self.__camera.stop_preview()

