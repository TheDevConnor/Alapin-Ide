from pathlib import Path # Python 3.4+ only
import sys
import os

import keyword
import pkgutil

from PyQt5.Qsci  import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow):

    def __init__(self):
        super(QMainWindow, self).__init__()
        self.side_bar_color = "#d8dee9"
        self.window_color = "#2e3440"
        self.text_color = "#fff"
        self.init_ui()

        self.current_file = None

    def init_ui(self):
        self.setWindowTitle("Alapin")
        self.setWindowIcon(QIcon("src/icons/Alpine.png"))
        self.resize(1050, 550)

        self.setStyleSheet(open("src/css/style.qss", "r").read())

        self.window_font = QFont("JetBrains Mono", 12, QFont.Normal, False)
        self.window_font.setPointSize(12)
        self.window_font.setWeight(50)
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

        cut_action = edit_menu.addAction("Cut")
        cut_action.setShortcut("Ctrl+X")
        cut_action.triggered.connect(self.cut)

        paste_action = edit_menu.addAction("Paste")
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self.paste)

        undo_action = edit_menu.addAction("Undo")
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.undo)

        redo_action = edit_menu.addAction("Redo")
        redo_action.setShortcut("Ctrl+Shift+Z")
        redo_action.triggered.connect(self.redo)

        edit_menu.addSeparator()

        select_all_action = edit_menu.addAction("Select All")
        select_all_action.setShortcut("Ctrl+A")
        select_all_action.triggered.connect(self.select_all)

        delete_action = edit_menu.addAction("Delete")
        delete_action.setShortcut("Del")
        delete_action.triggered.connect(self.delete)

        # View Menu
        view_menu = menu_bar.addMenu("View")

        run_action = view_menu.addAction("Run")
        run_action.setShortcut("Ctrl+R")
        run_action.triggered.connect(self.run)

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
        editor.setAutoCompletionSource(QsciScintilla.AcsAll)
        editor.setAutoCompletionThreshold(1)
        editor.setAutoCompletionCaseSensitivity(False)
        editor.setAutoCompletionUseSingle(QsciScintilla.AcusNever)

        # Caret
        # editor.setCaretForegroundColor(QColor("#2e3440"))
        editor.setCaretLineVisible(True)
        editor.setCaretWidth(4)
        # editor.setCaretLineBackgroundColor(QColor("#d8dee1"))

        # EDL
        editor.setEolMode(QsciScintilla.EolUnix)
        editor.setEolVisibility(False)
        
        # Lexer for syntax highlighting
        self.pyLexer = QsciLexerPython()
        self.htmlLexer = QsciLexerHTML()
        self.csharpLexer = QsciLexerCSharp()
        self.cppLexer = QsciLexerCPP()
        self.javaLexer = QsciLexerJava()
        self.jsLexer = QsciLexerJavaScript()
        self.luaLexer = QsciLexerLua()
        self.rubyLexer = QsciLexerRuby()
        self.xmlLexer = QsciLexerXML()
        self.yamlLexer = QsciLexerYAML()
        self.cmakeLexer = QsciLexerCMake()
        self.cssLexer = QsciLexerCSS()
        self.diffLexer = QsciLexerDiff()
        self.makefileLexer = QsciLexerMakefile()
        self.perlLexer = QsciLexerPerl()
        self.powershellLexer = QsciLexerPOV()
        self.povLexer = QsciLexerPOV()
        self.propertiesLexer = QsciLexerProperties()
        self.psLexer = QsciLexerPostScript()
        self.coffiescriptLexer = QsciLexerCoffeeScript()

        self.pyLexer.setDefaultFont(self.window_font)
        self.htmlLexer.setDefaultFont(self.window_font)
        self.csharpLexer.setDefaultFont(self.window_font)
        self.cppLexer.setDefaultFont(self.window_font)
        self.javaLexer.setDefaultFont(self.window_font)
        self.jsLexer.setDefaultFont(self.window_font)
        self.luaLexer.setDefaultFont(self.window_font)
        self.rubyLexer.setDefaultFont(self.window_font)
        self.xmlLexer.setDefaultFont(self.window_font)
        self.yamlLexer.setDefaultFont(self.window_font)
        self.cmakeLexer.setDefaultFont(self.window_font)
        self.cssLexer.setDefaultFont(self.window_font)
        self.diffLexer.setDefaultFont(self.window_font)
        self.makefileLexer.setDefaultFont(self.window_font)
        self.perlLexer.setDefaultFont(self.window_font)
        self.powershellLexer.setDefaultFont(self.window_font)
        self.povLexer.setDefaultFont(self.window_font)
        self.propertiesLexer.setDefaultFont(self.window_font)
        self.psLexer.setDefaultFont(self.window_font)
        self.coffiescriptLexer.setDefaultFont(self.window_font)

        # API
        self.api = QsciAPIs(self.pyLexer)
        self.api = QsciAPIs(self.htmlLexer)
        self.api = QsciAPIs(self.csharpLexer)
        self.api = QsciAPIs(self.cppLexer)
        self.api = QsciAPIs(self.javaLexer)
        self.api = QsciAPIs(self.jsLexer)
        self.api = QsciAPIs(self.luaLexer)
        self.api = QsciAPIs(self.rubyLexer)
        self.api = QsciAPIs(self.xmlLexer)  
        self.api = QsciAPIs(self.yamlLexer)
        self.api = QsciAPIs(self.cmakeLexer)
        self.api = QsciAPIs(self.cssLexer)
        self.api = QsciAPIs(self.diffLexer)
        self.api = QsciAPIs(self.makefileLexer)
        self.api = QsciAPIs(self.perlLexer)
        self.api = QsciAPIs(self.powershellLexer)
        self.api = QsciAPIs(self.povLexer)
        self.api = QsciAPIs(self.propertiesLexer)
        self.api = QsciAPIs(self.psLexer)
        self.api = QsciAPIs(self.coffiescriptLexer)

        for key in keyword.kwlist + dir(__builtins__):
            self.api.add(key)

        for _, name, _ in pkgutil.iter_modules():
            self.api.add(name)

        self.api.prepare()

        # Set the lexer
        editor.setLexer(self.pyLexer)
        editor.setLexer(self.htmlLexer)
        editor.setLexer(self.csharpLexer)
        editor.setLexer(self.cppLexer)
        editor.setLexer(self.javaLexer)
        editor.setLexer(self.jsLexer)
        editor.setLexer(self.luaLexer)
        editor.setLexer(self.rubyLexer)
        editor.setLexer(self.xmlLexer)
        editor.setLexer(self.yamlLexer)
        editor.setLexer(self.cmakeLexer)
        editor.setLexer(self.cssLexer)
        editor.setLexer(self.diffLexer)
        editor.setLexer(self.makefileLexer)
        editor.setLexer(self.perlLexer)
        editor.setLexer(self.powershellLexer)
        editor.setLexer(self.povLexer)
        editor.setLexer(self.propertiesLexer)
        editor.setLexer(self.psLexer)
        editor.setLexer(self.coffiescriptLexer)

        # Line Number
        editor.setMarginLineNumbers(0, True)
        editor.setMarginWidth(0, "0000")
        editor.setMarginsForegroundColor(QColor("#ff8888"))
        editor.setMarginsBackgroundColor(QColor("#3e3f40"))
        editor.setMarginsFont(self.window_font)

        # Folding
        editor.setFolding(QsciScintilla.BoxedTreeFoldStyle)
        editor.setFoldMarginColors(QColor("#3e3f40"), QColor("#3e3f40"))

        # Highlight current line
        editor.setCaretLineVisible(True)
        editor.setCaretLineBackgroundColor(QColor("#464a4c"))

        # Set the font
        editor.setFont(self.window_font)

        # Set the tab width
        editor.setTabWidth(4)

        # Set the tab indentation
        editor.setIndentationsUseTabs(False)

        # Key Press
        editor.keyPressEvent = self.handle_editor_press

        return editor

    def handle_editor_press(self, e: QKeyEvent):
        editor: QsciScintilla = self.tab_view.currentWidget()
        if e.modifiers() == Qt.ControlModifier and e.key() == Qt.Key_Space:
            editor.autoCompleteFromAll()
        else:
            QsciScintilla.keyPressEvent(editor, e)

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
                background-color: #6c7a87;
                border-radius: 1px;
                border: none;
                padding: 5px;
                color: #d8dee9;
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

        ################################################
        ###### SIDE BAR ##############################
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
        folder_label.setPixmap(QPixmap("src/icons/icons8-folder-64.png").scaled(QSize(40, 40)))
        folder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        folder_label.setFont(self.window_font)
        folder_label.mousePressEvent = self.show_hidden_tab
        side_bar_layout.addWidget(folder_label)

        search_label = QLabel()
        search_label.setPixmap(QPixmap("src/icons/icons8-search-50.png").scaled(QSize(30, 30)))
        search_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        search_label.setFont(self.window_font)
        search_label.mousePressEvent = self.show_hidden_tab
        side_bar_layout.addWidget(search_label)

        self.side_bar.setLayout(side_bar_layout)


        # split view
        self.hsplit = QSplitter(Qt.Horizontal)

        ################################################
        ###### FILE MANAGER ########################

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

        ###############################################
        ###### FILE VIEWER #############################
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

        ################################################
        ###### TAB WIDGETS ##########################

        self.tab_view = QTabWidget()
        self.tab_view.setContentsMargins(5, 10, 5, 0)
        self.tab_view.setTabsClosable(True)
        self.tab_view.setMovable(True)
        self.tab_view.setDocumentMode(True)
        self.tab_view.tabCloseRequested.connect(self.close_tab)
        self.tab_view.tabBar().setExpanding(False)

        ##################################################
        ###### SETUP WIDGETS ##########################

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
        # This is the about Menu
        QMessageBox.about(self, "About", "This is a simple text editor made by TheDevConnor on yt")

    def new_file(self):
        self.set_new_tab(None, is_new_file=True)

    def open_file(self):
        # Open a new file
        ops = QFileDialog.Options()
        ops |= QFileDialog.DontUseNativeDialog
        # I will add support for opening multiple files at the same time later on. Just going simple for now
        new_file, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Python Files (*.py)", options=ops)
        if new_file:
            self.statusBar().showMessage(f"Opening Filed Cancelled")
            return
        p = Path(new_file)
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
        # TODO :: need to fix file save
        # Save the file
        if self.current_file is None and self.tab_view.count() > 0:
            self.save_as()

        editor = self.tab_view.currentWidget()
        self.current_file.write_text(editor.text())
        self.statusBar().showMessage(f"Saved file {self.current_file}", 2000)

    def save_as(self):
        # Save as file
        editor = self.tab_view.currentWidget()
        if editor is None:
            return

        file_path = QFileDialog.getSaveFileName(self, "Save File", os.getcwd())[0]
        if file_path == '':
            self.statusBar().showMessage(f"Save file cancelled", 2000)
            return

        path = Path(file_path)
        path.write_text(editor.text())
        self.tab_view.setTabText(self.tab_view.currentIndex(), path.name)
        self.statusBar().showMessage(f"Saved file {file_path}", 2000)
        self.current_file = path

    def copy(self):
        # This will copy the contents of the current tab
        editor = self.tab_view.currentWidget()
        if editor is not None:
            editor.copy()

    def cut(self):
        # This will cut the contents of the current tab
        editor = self.tab_view.currentWidget()
        if editor is not None:
            editor.cut()

    def paste(self):
        # This will paste the contents of the current tab
        editor = self.tab_view.currentWidget()
        if editor is not None:
            editor.paste()

    def undo(self):
        # This will undo the contents of the current tab
        editor = self.tab_view.currentWidget()
        if editor is not None:
            editor.undo()

    def redo(self):
        # This will redo the contents of the current tab
        editor = self.tab_view.currentWidget()
        if editor is not None:
            editor.redo()

    def select_all(self):
        # This will select all the contents of the current tab
        editor = self.tab_view.currentWidget()
        if editor is not None:
            editor.selectAll()

    def delete(self):
        ...

    def run(self):
        ...
    
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec_())
