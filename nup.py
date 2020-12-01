import sys

from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtWidgets import QWidget, QApplication

app = QApplication(sys.argv)

w = QWidget()
palette = QPalette()
pix = QPixmap("ui/login.jpg")
pix = pix.scaled(w.width(), w.height())
palette.setBrush(QPalette.Background, QBrush(pix))
w.setPalette(palette)
w.show()

sys.exit(app.exec())
