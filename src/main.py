import sys
import os
from pathlib import Path # Python 3.4+ only

from PyQt5.Qsci  import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow):

    def __init__(self):
        super(QMainWindow, self).__init__()
        self.side_bar_color = "#68717f"
        self.init_ui()

        self.current_file = None

    def init_ui(self):
        self.setWindowTitle("Alapin")
        self.setWindowIcon(QIcon("icons\Alpine.png"))
        self.resize(1050, 550)

        self.setStyleSheet(open(".\src\css\style.qss", "r").read())

        self.window_font = QFont("Consolas")
        self.window_font.setPointSize(10)
        self.setFont(self.window_font)

        self.set_up_menu()
        self.set_up_body()
        self.statusBar().showMessage("Hello! Welcome to Alapin")

        self.show()

    def set_up_menu(self):
        menu_bar = self.menuBar()

        # File Menu
        file_menu = menu_bar.addMenu("File")
        
        new_file = file_menu.addAction("New File")
        new_file.setShortcut("Ctrl+N")
        new_file.triggered.connect(self.new_file)

        open_file = file_menu.addAction("Open File")
        open_file.setShortcut("Ctrl+O")
        open_file.triggered.connect(self.open_file)

        open_folder = file_menu.addAction("Open Folder")
        open_folder.setShortcut("Ctrl+K")
        open_folder.triggered.connect(self.open_folder)

        file_menu.addSeparator()

        exit = file_menu.addAction("Exit")
        exit.setShortcut("Ctrl+Q")
        exit.triggered.connect(self.close)        

        # Edit menu
        edit_menu = menu_bar.addMenu("Edit")
        
        copy_action = edit_menu.addAction("Copy")
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy)

        # Help menu
        help_menu = menu_bar.addMenu("Help")

        about = help_menu.addAction("About")
        about.triggered.connect(self.about)
    
    def about(self):
        ...

    def new_file(self):
        ...

    def open_file(self):
        ...

    def open_folder(self):
        ...

    def copy(self):
        ...

    def get_Editor(self) -> QsciScintilla:
        pass

    def set_up_body(self):
        
        # The Body
        body_frame = QFrame()
        body_frame.setFrameShape(QFrame.NoFrame)
        body_frame.setFrameShadow(QFrame.Plain) 
        body_frame.setLineWidth(0)
        body_frame.setMidLineWidth(0)
        body_frame.setContentsMargins(0, 0, 0, 0)
        body_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        body = QVBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)
        body_frame.setLayout(body)

        # The Side Bar
        self.side_bar = QFrame()
        self.side_bar.setFrameShape(QFrame.StyledPanel)
        self.side_bar.setFrameShadow(QFrame.Plain)
        self.side_bar.setStyleSheet(f'''
            background-color: {self.side_bar_color};
        ''')
        side_bar_layout = QHBoxLayout()
        side_bar_layout.setContentsMargins(5, 10, 5, 0)
        side_bar_layout.setSpacing(0)
        side_bar_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        self.side_bar.setLayout(side_bar_layout)

        body.addWidget(self.side_bar)

        # Split View
        self.hsplit = QSplitter(Qt.Horizontal)

        # frame and layout to hold the tree view
        self.tree_frame = QFrame()
        self.tree_frame.setLineWidth(1)
        self.tree_frame.setMaximumWidth(600)
        self.tree_frame.setMinimumWidth(200)
        self.tree_frame.setBaseSize(100, 0)
        self.tree_frame.setContentsMargins(0, 0, 0, 0)
        tree_frame_layout = QVBoxLayout()
        tree_frame_layout.setContentsMargins(0, 0, 0, 0)
        tree_frame_layout.setSpacing(0)
        self.tree_frame.setStyleSheet('''
            QFrame {
                background-color: #282c34;
                border-radius: 5px;
                border: none;
                padding: 5px;
                color: #D4D4D4;
            }
            QFrame:hover {
                color: #D4D4B4; 
            }
        ''')

        # Create the tree view for the files
        self.model = QFileSystemModel()
        self.model.setRootPath(os.getcwd())
        # Filter out the files we don't want to see
        self.model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Files)

        # tree view
        self.tree_view = QTreeView()
        self.tree_view.setFont(QFont("Consolas", 13))
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(os.getcwd()))
        self.tree_view.setSelectionMode(QTreeView.SingleSelection)
        self.tree_view.setSelectionBehavior(QTreeView.SelectRows)
        self.tree_view.setEditTriggers(QTreeView.NoEditTriggers)
        # add custom context menu
        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.tree_view_context_menu)
        # Handling click
        self.tree_view.clicked.connect(self.tree_view_clicked)
        self.tree_view.setIndentation(10)
        self.tree_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # setup layout
        tree_frame_layout.addWidget(self.tree_view)
        self.tree_frame.setLayout(tree_frame_layout)

        # Add the tree view to the split view
        self.hsplit.addWidget(self.tree_frame)

        body.addWidget(self.hsplit)
        body_frame.setLayout(body)

        self.setCentralWidget(body_frame)

    def tree_view_context_menu(self, pos):
        ...

    def tree_view_clicked(self, index):
        ...

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec_())
