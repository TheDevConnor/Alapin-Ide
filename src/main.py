from pathlib import Path # Python 3.4+ only
import sys
import os

from PyQt5.Qsci  import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow):

    def __init__(self):
        super(QMainWindow, self).__init__()
        self.side_bar_color = "#d8dee9"
        self.window_color = "#000000"
        self.text_color = "#fff"
        self.init_ui()

        self.current_file = None

    def init_ui(self):
        self.setWindowTitle("Alapin")
        self.setWindowIcon(QIcon("src\icons\Alpine.png"))
        self.resize(1050, 550)

        self.setStyleSheet(open("src\css\style.qss", "r").read())

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
        new_file.setShortcut("Ctrl+Shift+N")
        new_file.triggered.connect(self.new_file)

        open_file = file_menu.addAction("Open File")
        open_file.setShortcut("Ctrl+O")
        open_file.triggered.connect(self.open_file)

        open_folder = file_menu.addAction("Open Folder")
        open_folder.setShortcut("Ctrl+K")
        open_folder.triggered.connect(self.open_folder)

        file_menu.addSeparator()

        save_file = file_menu.addAction("Save")
        save_file.setShortcut("Ctrl+S")
        save_file.triggered.connect(self.save_file)

        save_as = file_menu.addAction("Save As")
        save_as.setShortcut("Ctrl+Shift+S")
        save_as.triggered.connect(self.save_as)

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

    def close_tab(self, index):
        self.tab_view.removeTab(index)

    def get_Editor(self) -> QsciScintilla:
        # Initialize the editor
        editor = QsciScintilla()
        # Encoding the editor
        editor.setUtf8(True)
        # Set the font
        editor.setFont(self.window_font)

        # Brace matching
        editor.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        # Indentation
        editor.setIndentationGuides(True)
        editor.setTabWidth(4)
        editor.setIndentationsUseTabs(False)
        editor.setAutoIndent(True)

        # Autocomplete
        # TODO :: Add this later

        # Caret
        # TODO :: Add this later    

        # EDL
        editor.setEolMode(QsciScintilla.EolUnix)
        editor.setEolVisibility(False)
        
        # Lexer and Syntax Highlighting
        editor.setLexer(QsciLexerPython())
        editor.setFolding(QsciScintilla.BoxedTreeFoldStyle)

        # Line Number
        editor.setMarginLineNumbers(0, True)
        editor.setMarginWidth(0, "0000")

        # Current Line
        editor.setCaretLineVisible(True)
        editor.setCaretLineBackgroundColor(QColor("#d8dee9"))

        # Selection
        editor.setSelectionBackgroundColor(QColor("#4d12a2"))
        editor.setSelectionForegroundColor(QColor("#d8dee9"))

        # White Space
        editor.setWhitespaceVisibility(QsciScintilla.WsVisible)
        editor.setWhitespaceForegroundColor(QColor("#4c566a"))

        # Indentation Guide
        editor.setIndentationGuides(True)
        editor.setIndentationGuidesForegroundColor(QColor("#4F56Ba"))

        # Wrap Mode
        editor.setWrapMode(QsciScintilla.WrapWord)

        # Zoom
        editor.zoomTo(0)

        # Set the default text
        editor.setText("")
        return editor

    def is_binary(self, path: Path):
        '''Check if the file is binary or not'''
        with open(path, 'rb') as f:
            return b'\0' in f.read(1024)

    def set_new_tab(self, path: Path, is_new_file=False):
        # Create a new tab
        editor = self.get_Editor()

        if is_new_file:
            self.tab_view.addTab(editor, "Untitled")
            self.setWindowTitle("Alapin - Untitled")
            self.statusBar().showMessage("New File")
            self.tab_view.setCurrentIndex(self.tab_view.count() - 1)
            self.current_file = None
            return
        if not path.is_file():
            return
        if self.is_binary(path):
            self.statusBar().showMessage("Cannot open binary file", 2000)
            return

        # Check if the file is open
        for i in range(self.tab_view.count()):
            if self.tab_view.tabText(i) == path.name:
                self.tab_view.setCurrentIndex(i)
                self.current_file = path
                return

        self.tab_view.addTab(editor, path.name)
        editor.setText(path.read_text())
        self.current_file = path
        self.tab_view.setCurrentIndex(self.tab_view.count() - 1)
        self.statusBar().showMessage("Opened file: {}".format(path.name))

    def get_frame(self) -> QFrame:
        frame = QFrame()
        frame.setFrameShape(QFrame.NoFrame)
        frame.setFrameShadow(QFrame.Plain)
        frame.setContentsMargins(0, 0, 0, 0)
        frame.setStyleSheet('''
            QFrame {
                background-color: #d8dee1;
                border-radius: 1px;
                border: none;
                padding: 5px;
                color: #2e3440;
            }
            QFrame:hover {
                color: blue;
            }
        ''')
        return frame


    def set_up_body(self):
       # Body        
        body_frame = QFrame()
        body_frame.setFrameShape(QFrame.NoFrame)
        body_frame.setFrameShadow(QFrame.Plain)
        body_frame.setLineWidth(0)
        body_frame.setMidLineWidth(0)
        body_frame.setContentsMargins(0, 0, 0, 0)
        body_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)
        body_frame.setLayout(body)

        ##############################
        ###### SIDE BAR ##########
        self.side_bar = QFrame()
        self.side_bar.setFrameShape(QFrame.StyledPanel)
        self.side_bar.setFrameShadow(QFrame.Plain)
        self.side_bar.setStyleSheet(f'''
            background-color: {self.side_bar_color};
        ''')   
        side_bar_layout = QVBoxLayout()
        side_bar_layout.setContentsMargins(5, 10, 5, 0)
        side_bar_layout.setSpacing(0)
        side_bar_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        # Set up the labels for the side bar buttons
        folder_label = QLabel()
        folder_label.setPixmap(QPixmap("src\icons\icons8-folder-64.png").scaled(QSize(40, 40)))
        folder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        folder_label.setFont(self.window_font)
        folder_label.mousePressEvent = self.show_hidden_tab
        side_bar_layout.addWidget(folder_label)

        search_label = QLabel()
        search_label.setPixmap(QPixmap("src\icons\icons8-search-50.png").scaled(QSize(30, 30)))
        search_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        search_label.setFont(self.window_font)
        search_label.mousePressEvent = self.show_hidden_tab
        side_bar_layout.addWidget(search_label)

        self.side_bar.setLayout(side_bar_layout)


        # split view
        self.hsplit = QSplitter(Qt.Horizontal)

        ##############################
        ###### FILE MANAGER ##########

        # frame and layout to hold tree view (file manager)
        self.file_manager_frame = self.get_frame()
        self.file_manager_frame.setMaximumWidth(400)
        self.file_manager_frame.setMinimumWidth(200)
        tree_frame_layout = QVBoxLayout()
        tree_frame_layout.setContentsMargins(0, 0, 0, 0)
        tree_frame_layout.setSpacing(0)

        # Create file system model to show in tree view
        self.model = QFileSystemModel()
        self.model.setRootPath(os.getcwd())
        # File system filters
        self.model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Files)

        ##############################
        ###### FILE VIEWER ##########
        self.tree_view = QTreeView()
        self.tree_view.setFont(QFont("FiraCode", 13))
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(os.getcwd()))
        self.tree_view.setSelectionMode(QTreeView.SingleSelection)
        self.tree_view.setSelectionBehavior(QTreeView.SelectRows)
        self.tree_view.setEditTriggers(QTreeView.NoEditTriggers)
        # add custom context menu
        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.tree_view_context_menu)
        # handling click
        self.tree_view.clicked.connect(self.tree_view_clicked)
        self.tree_view.setIndentation(10)
        self.tree_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # Hide header and hide other columns except for name
        self.tree_view.setHeaderHidden(True) # hiding header
        self.tree_view.setColumnHidden(1, True)
        self.tree_view.setColumnHidden(2, True)
        self.tree_view.setColumnHidden(3, True)

        # setup layout
        tree_frame_layout.addWidget(self.tree_view)
        self.file_manager_frame.setLayout(tree_frame_layout)

        ##############################
        ###### TAB WIDGETS ##########

        self.tab_view = QTabWidget()
        self.tab_view.setContentsMargins(5, 10, 5, 0)
        self.tab_view.setTabsClosable(True)
        self.tab_view.setMovable(True)
        self.tab_view.setDocumentMode(True)
        # self.tab_view.tabCloseRequested.connect(self.close_tab)


        ##############################
        ###### SETUP WIDGETS ##########

        # add tree view and tab view
        self.hsplit.addWidget(self.file_manager_frame)
        self.hsplit.addWidget(self.tab_view)

        body.addWidget(self.side_bar)
        body.addWidget(self.hsplit)

        body_frame.setLayout(body)

        self.setCentralWidget(body_frame)

    def show_hidden_tab(self, event):
        ...

    def tree_view_context_menu(self, pos):
        ...

    def tree_view_clicked(self, index: QModelIndex):
        path = self.model.filePath(index)
        p = Path(path)
        self.set_new_tab(p)

    def about(self):
        ...

    def new_file(self):
        self.set_new_tab(None, is_new_file=True)

    def open_file(self):
        # Open a new file
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", os.getcwd(), 
                                             "All Files (*);;Python Files (*.py)")
        if file_name:
            p = Path(file_name)
            self.set_new_tab(p)

    def open_folder(self):
        # Open a new folder
        folder_name = QFileDialog.getExistingDirectory(self, "Open Folder", os.getcwd())
        if folder_name:
            p = Path(folder_name)
            self.model.setRootPath(folder_name)
            self.tree_view.setRootIndex(self.model.index(folder_name))
            self.statusBar().showMessage(f"Opened folder {folder_name}")

    def save_file(self):
        # Save the file
        if self.current_file is None and self.tab_view.count() > 0:
            self.save_as()

        editor = self.tab_view.currentWidget()
        self.current_file.write_text(editor.text())
        self.statusBar().showMessage(f"Saved {self.current_file.name}", 2000)

    def save_as(self):
        # Save as
        editor = self.tab_view.currentWidget()
        if editor is not None:
            return

        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*)")
        if file_name == "":
            self.statusBar().showMessage("Save cancelled", 2000)
            return
        path = Path(file_name)
        path.write_text(editor.text())
        self.tab_view.setTabText(self.tab_view.currentIndex(), path.name)
        self.statusBar().showMessage(f"Saved {path.name}", 2000)
        self.current_file = path

    def copy(self):
        # This will copy the contents of the current tab
        editor = self.tab_view.currentWidget()
        if editor is not None:
            return

        editor.copy()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec_())
