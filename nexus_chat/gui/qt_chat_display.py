"""Qt-based chat display widget."""
import logging
import re
from typing import Optional

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QTextCharFormat, QSyntaxHighlighter, QColor, QTextCursor
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PyQt6.Qsci import QsciScintilla, QsciLexerPython

logger = logging.getLogger(__name__)

class CodeHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for code blocks."""
    
    def __init__(self, parent=None):
        """Initialize highlighter."""
        super().__init__(parent)
        self.code_format = QTextCharFormat()
        self.code_format.setFontFamily("Consolas")
        self.code_format.setFontPointSize(10)
        
        # Create formats for different syntax elements
        self.formats = {
            'keyword': self._create_format('#ff79c6', True),
            'string': self._create_format('#f1fa8c'),
            'comment': self._create_format('#6272a4', italic=True),
            'number': self._create_format('#bd93f9'),
            'function': self._create_format('#50fa7b'),
        }
        
        # Define regex patterns
        self.patterns = {
            'keyword': r'\b(def|class|import|from|return|if|else|elif|for|while|try|except|with|as|in|is|not|and|or)\b',
            'string': r'\".*?\"|\'.*?\'',
            'comment': r'#[^\n]*',
            'number': r'\b\d+\b',
            'function': r'\b\w+(?=\s*\()',
        }
        
    def _create_format(self, color: str, bold: bool = False, italic: bool = False) -> QTextCharFormat:
        """Create text format.
        
        Args:
            color: Color in hex format
            bold: Whether text should be bold
            italic: Whether text should be italic
            
        Returns:
            Text format
        """
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))
        fmt.setFontFamily("Consolas")
        fmt.setFontPointSize(10)
        if bold:
            fmt.setFontWeight(700)
        if italic:
            fmt.setFontItalic(True)
        return fmt
        
    def highlightBlock(self, text: str):
        """Highlight code block.
        
        Args:
            text: Text to highlight
        """
        # Apply base format
        self.setFormat(0, len(text), self.code_format)
        
        # Apply syntax highlighting
        for pattern_name, pattern in self.patterns.items():
            for match in re.finditer(pattern, text):
                start, end = match.span()
                self.setFormat(start, end - start, self.formats[pattern_name])

class ChatDisplay(QWidget):
    """Qt-based chat display widget."""
    
    def __init__(self):
        """Initialize chat display."""
        super().__init__()
        
        # Create layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Create text edit
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setMinimumSize(QSize(400, 300))
        
        # Set dark theme
        self.text_edit.setStyleSheet("""
            QTextEdit {
                background-color: #282a36;
                color: #f8f8f2;
                border: none;
                selection-background-color: #44475a;
                selection-color: #f8f8f2;
                font-family: 'Segoe UI', Arial;
                font-size: 12pt;
            }
        """)
        
        # Add to layout
        self.layout.addWidget(self.text_edit)
        
        # Initialize highlighter
        self.highlighter = CodeHighlighter(self.text_edit.document())
        
        # Store current response
        self.current_response = ""
        
    def append_message(self, role: str, content: str):
        """Append message to chat.
        
        Args:
            role: Message role (user/assistant)
            content: Message content
        """
        # Create cursor
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        
        # Add spacing if not first message
        if not cursor.atStart():
            cursor.insertBlock()
            cursor.insertBlock()
        
        # Insert role
        role_format = QTextCharFormat()
        role_format.setForeground(QColor("#6272a4"))
        role_format.setFontWeight(700)
        cursor.insertText(f"{role}:", role_format)
        cursor.insertBlock()
        
        # Process content
        self._insert_formatted_content(cursor, content)
        
        # Scroll to bottom
        self.text_edit.setTextCursor(cursor)
        self.text_edit.ensureCursorVisible()
        
    def update_last_message(self, content: str):
        """Update last message content.
        
        Args:
            content: New content
        """
        # Store content
        self.current_response = content
        
        # Find last message
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        
        # Move to start of last message content
        cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
        cursor.movePosition(QTextCursor.MoveOperation.PreviousBlock)
        cursor.movePosition(QTextCursor.MoveOperation.PreviousBlock)
        
        # Select to end
        cursor.movePosition(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.KeepAnchor)
        
        # Replace content
        cursor.removeSelectedText()
        self._insert_formatted_content(cursor, content)
        
        # Scroll to bottom
        self.text_edit.setTextCursor(cursor)
        self.text_edit.ensureCursorVisible()
        
    def _insert_formatted_content(self, cursor: QTextCursor, content: str):
        """Insert formatted content.
        
        Args:
            cursor: Text cursor
            content: Content to insert
        """
        # Split into code blocks and text
        parts = re.split(r'(```\w+\n.*?\n```)', content, flags=re.DOTALL)
        
        for part in parts:
            if part.startswith('```') and part.endswith('```'):
                # Extract language and code
                match = re.match(r'```(\w+)\n(.*?)\n```', part, re.DOTALL)
                if match:
                    lang, code = match.groups()
                    
                    # Create code block
                    code_format = QTextCharFormat()
                    code_format.setBackground(QColor("#1e1e1e"))
                    code_format.setFontFamily("Consolas")
                    code_format.setFontPointSize(10)
                    
                    # Insert code block
                    cursor.insertBlock()
                    cursor.insertText(code.strip(), code_format)
                    cursor.insertBlock()
            else:
                # Insert regular text
                if part.strip():
                    cursor.insertText(part.strip())
