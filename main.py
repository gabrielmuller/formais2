import sys
from gui.gui import GUI
from PyQt5.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    window = GUI()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()