import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QProgressBar, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap

# Ensure the main application code can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import UpdateCheckerApp  # Import the main application class

class TestUpdateCheckerApp(UpdateCheckerApp):
    def start_progress(self):
        # Reset the progress bar and disable the button
        self.progress_bar.setValue(0)
        self.check_button.setEnabled(False)
        self.status_label.setText("Checking for updates...")
        self.mock_check_for_new_posts()

    def mock_check_for_new_posts(self):
        # Simulate finding new posts
        new_posts = ["Post 1", "Post 2", "Post 3"]
        url = "https://nullsignal.games/blog/category/news/product-announcements/"

        # Display icon and hyperlink for new posts
        icon_path = os.path.join(os.path.dirname(__file__), '..', 'icon.png')
        icon = QPixmap(icon_path)
        self.icon_label.setPixmap(icon)
        self.status_label.setText(f"<a href='{url}' style='color: #00f;'>New posts detected: {', '.join(new_posts)}</a>")
        self.status_label.setOpenExternalLinks(True)

        # Complete the progress bar
        self.progress_bar.setValue(100)
        self.check_button.setEnabled(True)  # Re-enable the button

# Main application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestUpdateCheckerApp()
    window.show()
    sys.exit(app.exec_())