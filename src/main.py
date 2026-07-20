"""Main entry point for the Abtin application."""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

from PyQt6.QtWidgets import QApplication
from src.config.logger_config import Logger
from src.config.settings import config
from src.ui.main_window import MainWindow

# Initialize logger
logger = Logger.get_logger(__name__)


def main() -> None:
    """Launch the Abtin application."""
    logger.info("Starting Abtin - Crypto Trading Analysis Platform")
    logger.info(f"Debug mode: {config.debug}")
    logger.info(f"Dark mode: {config.dark_mode}")

    # Create Qt application
    app = QApplication(sys.argv)

    # Set application properties
    app.setApplicationName(config.app_title)

    # Create and show main window
    window = MainWindow()
    window.show()

    logger.info("Application window created and displayed")

    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
