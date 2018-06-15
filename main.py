import sys
from gui import GUI
from PyQt5.QtWidgets import QApplication

def main():
    app = QApplication(sys.acfgv)
    window = GUI()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()