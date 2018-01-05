import Ui_interface
from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import yolo_detection
import os, sys

class img2emoji():
    def __init__(self):
        self.Form=QtWidgets.QWidget()
        self.ui = Ui_interface.Ui_Form()
        self.ui.setupUi(self.Form)
        self.videoCapture=cv2.VideoCapture()
        self.timer=QtCore.QTimer()
        self.ui.pushButton.clicked.connect(self.openImage)
        self.ui.pushButton_2.clicked.connect(self.captureImage)
        self.ui.pushButton_3.clicked.connect(self.detection)

        self.ui.pushButton.setIconSize(QtCore.QSize(40,40))
        self.ui.pushButton.setIcon(QtGui.QIcon("icon/folder.png"))
        self.ui.pushButton.setFlat(True)
        self.ui.pushButton.setText("")

        self.ui.pushButton_2.setIconSize(QtCore.QSize(40,40))
        self.ui.pushButton_2.setIcon(QtGui.QIcon("icon/Camera.png"))
        self.ui.pushButton_2.setFlat(True)
        self.ui.pushButton_2.setText("")

        self.ui.pushButton_3.setText("detecter")
        self.net, self.meta=yolo_detection.load_detector()

        self.mode = 'image'


    def openImage(self):
        if self.mode == 'camera':
            self.videoCapture.release()
            self.timer.stop()
        self.mode = 'image'
        fileName1, filetype = QtWidgets.QFileDialog.getOpenFileName(self.Form,  "choose a file",  "",  "Image Files (*.png *.bmp *.jpg *.tif *.GIF)")
        self.ui.label_4.setPixmap(QtGui.QPixmap(fileName1).scaled(320, 240))

    def captureImage(self):
        if self.mode == 'image':
            self.mode = 'camera'
            if self.videoCapture.open(0):
                self.timer.timeout.connect(self.updateFrame)
                self.timer.start(1000/25)
            else:
                print("camera configuration failed")

    def updateFrame(self):
        ret, srcMat=self.videoCapture.read()
        srcMat=cv2.resize(srcMat, (320, 240), interpolation=cv2.INTER_CUBIC)
        srcMat=cv2.flip(srcMat, 1)
        cv2.cvtColor(srcMat, cv2.COLOR_BGR2RGB,srcMat)
        height, width, bytesPerComponent= srcMat.shape
        bytesPerLine = bytesPerComponent* width
        srcQImage= QtGui.QImage(srcMat.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        srcQPix=QtGui.QPixmap.fromImage(srcQImage)
        self.ui.label_4.setPixmap(srcQPix)

    def detection(self):
        img_detc=self.ui.label_4.pixmap()
        try:
            img_detc.save("temp.jpg")
            results = yolo_detection.detec_img_with_preloaded_detector("temp.jpg", self.net, self.meta)
            scene = QtWidgets.QGraphicsScene()
            for i, result in enumerate(results):
                filename='emojis/{}'.format(result)
                item=QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap(filename).scaled(64,64))
                scene.addItem(item)
                lig = i/3
                col = i%3
                item.setPos(col*64,lig*64)
            self.ui.graphicsView.setScene(scene)
            os.system('rm temp.jpg')
        except:
            print("detection failed")



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    interfaceFun=img2emoji()
    interfaceFun.Form.show()
    sys.exit(app.exec_())
