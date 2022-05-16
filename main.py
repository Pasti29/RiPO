# importing required libraries
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
import os
import sys
import time
import cv2
import numpy as np

# Main window class
class MainWindow(QMainWindow):

    # constructor
    def __init__(self):
        super().__init__()

        # setting geometry
        self.setGeometry(100, 100, 800, 0)

        # setting style sheet

        # getting available cameras
        self.available_cameras = QCameraInfo.availableCameras()

        # if no camera found
        if not self.available_cameras:
            # exit the code
            sys.exit()

        # creating a status bar
        self.status = QStatusBar()

        # setting style sheet to the status bar

        # adding status bar to the main window
        self.setStatusBar(self.status)

        # path to save

        # creating a QCameraViewfinder object
        self.viewfinder = QCameraViewfinder()

        # showing this viewfinder
        self.viewfinder.show()

        # making it central widget of main window
        self.setCentralWidget(self.viewfinder)

        # Set the default camera.
        self.select_camera(0)

        # creating a tool bar
        toolbar = QToolBar("Camera Tool Bar")

        # adding tool bar to main window
        self.addToolBar(toolbar)

        # creating a combo box for selecting camera
        camera_selector = QComboBox()

        # adding status tip to it
        camera_selector.setStatusTip("Choose camera to take pictures")

        # adding tool tip to it
        camera_selector.setToolTip("Select Camera")
        camera_selector.setToolTipDuration(2500)

        # adding items to the combo box
        camera_selector.addItems(
            [camera.description() for camera in self.available_cameras]
        )

        # adding action to the combo box
        # calling the select camera method
        camera_selector.currentIndexChanged.connect(self.select_camera)

        # adding this to tool bar
        toolbar.addWidget(camera_selector)

        # setting tool bar stylesheet
        toolbar.setStyleSheet("background : white;")

        # setting window title
        self.setWindowTitle("Wybierz kamerę")

        # showing the main window
        self.show()

    # method to select camera
    def select_camera(self, i):
        self.run_main_window(i)
        pass

    # method for alerts
    def alert(self, msg):

        # error message
        error = QErrorMessage(self)

        # setting text to the error message
        error.showMessage(msg)

    def process_frame(self, frame):
        print(frame.shape)
        for i in range(0, frame.shape[0]):
            frame[i][0][2] = 255
            frame[i][0][1] = 0
            frame[i][0][0] = 0
        for i in range(0, frame.shape[1]):
            frame[0][i][2] = 255
            frame[0][i][1] = 0
            frame[0][i][0] = 0
        for i in range(0, frame.shape[0]):
            frame[i][frame.shape[1] - 1][2] = 255
            frame[i][frame.shape[1] - 1][1] = 0
            frame[i][frame.shape[1] - 1][0] = 0
        for i in range(0, frame.shape[1]):
            frame[frame.shape[0] - 1][i][2] = 255
            frame[frame.shape[0] - 1][i][1] = 0
            frame[frame.shape[0] - 1][i][0] = 0
        return frame

    def run_main_window(self, i):
        vid = cv2.VideoCapture(i)
        while True:
            ret, frame = vid.read()
            frame = self.process_frame(frame)
            cv2.imshow("frame", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        vid.release()
        cv2.destroyAllWindows()


# Driver code
if __name__ == "__main__":

    # create pyqt5 app
    App = QApplication(sys.argv)

    # create the instance of our Window
    window = MainWindow()

    # start the app
    sys.exit(App.exec())
