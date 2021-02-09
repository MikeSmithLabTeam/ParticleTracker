import sys
from PyQt5.QtCore import Qt, pyqtSignal, QRectF
from PyQt5.QtGui import QPixmap, QImage, QPainterPath, QCloseEvent, QWheelEvent, QColor
from PyQt5.QtWidgets import (QWidget, QSlider, QCheckBox, QHBoxLayout,
                             QLabel, QComboBox, QSizePolicy, QVBoxLayout,
                             QApplication, QGraphicsView, QGraphicsScene,
                             QLineEdit
                             )
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, \
    NavigationToolbar2QT
from matplotlib.figure import Figure

from qtwidgets import QCustomTextBox, SelectAreaWidget


class QModCustomTextBox(QCustomTextBox):
    returnPressed = pyqtSignal(str)

    def __init__(self, img_viewer, *args, **kwargs):
        self.img_viewer = img_viewer
        shapes = {'crop_box':['rect',QColor(250, 10, 10, 80)],
                  'mask_ellipse':['ellipse',QColor(10,10,250,80)],
                  'mask_polygon':['polygon',QColor(10,10,250,80)]
                  }
        title=kwargs['title']
        self.method = shapes[title][0]
        self.colour = shapes[title][1]
        self.hasbeenchecked = False#Stops the checkboxChanged fn firing on object creation.
        super(QModCustomTextBox, self).__init__(*args, **kwargs)
        self.checkbox.setChecked(False)
        
    def checkboxChanged(self) -> None:
        #Override checkboxChanged method
        check_state = self.checkbox.isChecked()
        if check_state:
            self.tool = SelectAreaWidget(shape=self.method, geometry=self.img_viewer.geometry, colour=self.colour)
            self.img_viewer.scene.addWidget(self.tool)
            self.hasbeenchecked = True
        else:
            if self.hasbeenchecked:
                self.textbox.setText(str(tuple(self.tool.points)))
                self.returnPressed.emit(str(tuple(self.tool.points)))
                self.tool.setParent(None)
                self.tool.deleteLater()
            self.hasbeenchecked = False

