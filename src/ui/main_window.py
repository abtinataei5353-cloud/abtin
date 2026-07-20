"""Main application window for Abtin."""

from pathlib import Path
from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QProgressBar,
    QTextEdit,
    QScrollArea,
    QFrame,
)

from src.config.settings import config
from src.config.logger_config import Logger
from src.utils.validators import ImageValidator

logger = Logger.get_logger(__name__)


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self) -> None:
        """Initialize main window."""
        super().__init__()
        self.setWindowTitle(config.app_title)
        self.setGeometry(100, 100, config.window_width, config.window_height)

        # Apply styling
        self._apply_style()

        # Create UI
        self._create_ui()

        logger.info("Main window initialized")

    def _apply_style(self) -> None:
        """Apply application stylesheet."""
        if config.dark_mode:
            stylesheet = self._get_dark_stylesheet()
        else:
            stylesheet = self._get_light_stylesheet()

        self.setStyleSheet(stylesheet)

    def _get_dark_stylesheet(self) -> str:
        """Get dark theme stylesheet."""
        return """
            QMainWindow {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QPushButton {
                background-color: #0d47a1;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                padding: 5px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
            QPushButton:pressed {
                background-color: #0d3f87;
            }
            QTextEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #404040;
                border-radius: 4px;
                padding: 5px;
                font-family: 'Courier New';
                font-size: 10px;
            }
            QLabel {
                color: #ffffff;
            }
            QProgressBar {
                background-color: #2d2d2d;
                border: 1px solid #404040;
                border-radius: 4px;
            }
            QProgressBar::chunk {
                background-color: #4caf50;
            }
            QScrollArea {
                background-color: #1e1e1e;
                border: none;
            }
        """

    def _get_light_stylesheet(self) -> str:
        """Get light theme stylesheet."""
        return """
            QMainWindow {
                background-color: #ffffff;
                color: #000000;
            }
            QWidget {
                background-color: #f5f5f5;
                color: #000000;
            }
            QPushButton {
                background-color: #0d47a1;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                padding: 5px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
        """

    def _create_ui(self) -> None:
        """Create user interface."""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QHBoxLayout(central_widget)

        # Left panel - Image display
        left_panel = QFrame()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(10, 10, 10, 10)

        # Image label
        self.image_label = QLabel("No image loaded")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("border: 2px dashed #404040; padding: 20px;")
        self.image_label.setMinimumSize(600, 400)
        left_layout.addWidget(self.image_label)

        # Upload button
        upload_btn = QPushButton("📁 Upload Chart Image")
        upload_btn.clicked.connect(self._on_upload_image)
        left_layout.addWidget(upload_btn)

        # Right panel - Analysis results
        right_panel = QFrame()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(10, 10, 10, 10)

        # Title
        title = QLabel("Analysis Results")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        right_layout.addWidget(title)

        # Analysis output
        self.analysis_text = QTextEdit()
        self.analysis_text.setReadOnly(True)
        self.analysis_text.setPlaceholderText(
            "Upload a cryptocurrency chart to begin analysis.\n\n"
            "The analysis will include:\n"
            "• Support & Resistance Levels\n"
            "• Smart Money Concepts (FVG, Order Blocks, BOS, CHoCH)\n"
            "• RTM Concepts (Base, Rally, Drop, Quasimodo, etc.)\n"
            "• Entry & Exit Levels\n"
            "• Risk-Reward Analysis\n"
            "• Confidence Score"
        )
        right_layout.addWidget(self.analysis_text)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        right_layout.addWidget(self.progress_bar)

        # Add panels to main layout
        main_layout.addWidget(left_panel, 2)
        main_layout.addWidget(right_panel, 1)

        logger.info("UI created successfully")

    def _on_upload_image(self) -> None:
        """Handle image upload."""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self,
            "Select Cryptocurrency Chart",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.webp)",
        )

        if file_path:
            self._load_image(file_path)

    def _load_image(self, file_path: str) -> None:
        """Load and display image.

        Args:
            file_path: Path to image file
        """
        if not ImageValidator.validate_file(file_path):
            self.analysis_text.setText(
                "❌ Error: Invalid image file.\n\n"
                "Please ensure:\n"
                "• File format is PNG, JPG, BMP, or WebP\n"
                "• File size is less than 50MB\n"
                "• Image dimensions are at least 400x300 pixels"
            )
            return

        # Load image
        pixmap = QPixmap(file_path)
        if pixmap.isNull():
            self.analysis_text.setText("❌ Error: Could not load image.")
            return

        # Scale image for display
        scaled_pixmap = pixmap.scaledToWidth(
            600, Qt.TransformationMode.SmoothTransformation
        )
        self.image_label.setPixmap(scaled_pixmap)

        logger.info(f"Image loaded: {file_path}")

        # Show progress
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.analysis_text.setText("🔄 Analyzing chart...\n\nProcessing image and detecting patterns...")

        # TODO: Trigger analysis in separate thread
        self._run_analysis(file_path)

    def _run_analysis(self, file_path: str) -> None:
        """Run technical analysis on image.

        Args:
            file_path: Path to image file
        """
        try:
            # TODO: Implement analysis pipeline
            sample_report = (
                "✅ Analysis Complete\n\n"
                "📊 Signal: BUY\n"
                "📈 Confidence: 75%\n\n"
                "🎯 Entry Zone: $42,500 - $42,800\n"
                "🛑 Stop Loss: $42,100\n"
                "💰 Take Profit 1: $43,500\n"
                "💰 Take Profit 2: $44,200\n\n"
                "📋 Analysis Factors:\n"
                "✓ Support level at $42,500\n"
                "✓ Order block confluence\n"
                "✓ Bullish divergence on RSI\n"
                "✓ Fair Value Gap (FVG) below current price\n"
                "✓ Base formation confirmed\n\n"
                "⚠️ Risk Factors:\n"
                "• Volume declining into entry\n"
                "• Resistance at $43,200\n\n"
                "Risk-Reward Ratio: 1:2.5"
            )

            self.analysis_text.setText(sample_report)
            self.progress_bar.setValue(100)
            self.progress_bar.setVisible(False)

        except Exception as e:
            logger.error(f"Analysis error: {str(e)}")
            self.analysis_text.setText(f"❌ Analysis Error:\n\n{str(e)}")
            self.progress_bar.setVisible(False)
