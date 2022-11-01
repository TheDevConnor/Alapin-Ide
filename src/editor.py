import keyword
import pkgutil

from PyQt5.Qsci  import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Editor(QsciScintilla):

    def __init__(self, parent=None):
        
        super(Editor, self).__init__(parent)

        # Encoding the self
        self.setUtf8(True)
        # Set the font
        self.window_font = QFont("JetBrains Mono", 12, QFont.Normal, False)
        self.window_font.setPointSize(12)
        self.window_font.setWeight(50)
        self.setFont(self.window_font)

        # Brace matching
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        # Indentation
        self.setIndentationGuides(True)
        self.setTabWidth(4)
        self.setIndentationsUseTabs(False)
        self.setAutoIndent(True)

        # Autocomplete
        self.setAutoCompletionSource(QsciScintilla.AcsAll)
        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionCaseSensitivity(False)
        self.setAutoCompletionUseSingle(QsciScintilla.AcusNever)

        # Caret
        # self.setCaretForegroundColor(QColor("#2e3440"))
        self.setCaretLineVisible(True)
        self.setCaretWidth(4)
        # self.setCaretLineBackgroundColor(QColor("#d8dee1"))

        # EDL
        self.setEolMode(QsciScintilla.EolUnix)
        self.setEolVisibility(False)
        
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
        self.setLexer(self.pyLexer)
        self.setLexer(self.htmlLexer)
        self.setLexer(self.csharpLexer)
        self.setLexer(self.cppLexer)
        self.setLexer(self.javaLexer)
        self.setLexer(self.jsLexer)
        self.setLexer(self.luaLexer)
        self.setLexer(self.rubyLexer)
        self.setLexer(self.xmlLexer)
        self.setLexer(self.yamlLexer)
        self.setLexer(self.cmakeLexer)
        self.setLexer(self.cssLexer)
        self.setLexer(self.diffLexer)
        self.setLexer(self.makefileLexer)
        self.setLexer(self.perlLexer)
        self.setLexer(self.powershellLexer)
        self.setLexer(self.povLexer)
        self.setLexer(self.propertiesLexer)
        self.setLexer(self.psLexer)
        self.setLexer(self.coffiescriptLexer)

        # Line Number
        self.setMarginLineNumbers(0, True)
        self.setMarginWidth(0, "0000")
        self.setMarginsForegroundColor(QColor("#ff8888"))
        self.setMarginsBackgroundColor(QColor("#464a4d"))
        self.setMarginsFont(self.window_font)

        # Current Line
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#282c34"))

        # Selection
        self.setSelectionBackgroundColor(QColor("#4d12a2"))
        self.setSelectionForegroundColor(QColor("#6c7a87"))

        # White Space
        self.setWhitespaceVisibility(QsciScintilla.WsVisible)
        self.setWhitespaceForegroundColor(QColor("#4c566a"))

        # Indentation Guide
        self.setIndentationGuides(True)
        self.setIndentationGuidesForegroundColor(QColor("#4F56Ba"))

        # Wrap Mode
        self.setWrapMode(QsciScintilla.WrapWord)

        # Zoom
        self.zoomTo(0)

        # Set the default text
        self.setText("")

    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.modifiers() == Qt.ControlModifier and e.key() == Qt.Key_Space:
            self.autoCompleteFromAll()
        else:
            return super().keyPressEvent(e)