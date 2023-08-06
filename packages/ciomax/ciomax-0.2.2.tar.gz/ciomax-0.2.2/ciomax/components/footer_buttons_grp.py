
from PySide2 import QtWidgets


class FooterButtonsGrp(QtWidgets.QWidget):
 
    def __init__(self, **kwargs):
        super(FooterButtonsGrp, self).__init__()

        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)

        self.close_button = QtWidgets.QPushButton("Close")
        # self.validate_button = QtWidgets.QPushButton("Validate")
        self.submit_button = QtWidgets.QPushButton("Submit")
        
        self.close_button.setAutoDefault(False)
        self.submit_button.setAutoDefault(False)
        
        layout.addWidget(self.close_button)
        # layout.addWidget(self.validate_button)
        layout.addWidget(self.submit_button)
