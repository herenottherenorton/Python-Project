from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QProgressBar, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from playwright.sync_api import sync_playwright
import os
import json

class UpdateCheckerApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the GUI
        self.setWindowTitle("Page Update Checker")
        self.setGeometry(300, 300, 500, 300)

        self.layout = QVBoxLayout()

        # Header label styled to match the website
        self.header_label = QLabel("Null Signal Games - Product Announcements", self)
        self.header_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.header_label.setStyleSheet(
            "background-color: #000; color: #fff; padding: 10px; text-align: center;"
        )
        self.layout.addWidget(self.header_label)

        # Status label
        self.status_label = QLabel("Click the button to check for updates.", self)
        self.status_label.setWordWrap(True)
        self.layout.addWidget(self.status_label)

        # Progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet(
            "QProgressBar { border: 1px solid #000; text-align: center; }"
            "QProgressBar::chunk { background-color: green; }"
        )
        self.layout.addWidget(self.progress_bar)

        # Check button
        self.check_button = QPushButton("Check for Updates", self)
        self.check_button.clicked.connect(self.start_progress)
        self.layout.addWidget(self.check_button)

        self.setLayout(self.layout)

    def start_progress(self):
        # Reset the progress bar and disable the button
        self.progress_bar.setValue(0)
        self.check_button.setEnabled(False)
        self.status_label.setText("Checking for updates...")
        self.check_for_new_posts()

    def check_for_new_posts(self):
        # File to store the previous list of post titles
        posts_file = "posts.json"

        # Progress milestones
        with sync_playwright() as playwright:
            # Step 1: Launch browser
            browser = playwright.chromium.launch(headless=True)
            self.progress_bar.setValue(20)

            # Step 2: Open a new page
            page = browser.new_page()
            self.progress_bar.setValue(40)

            # Step 3: Navigate to the URL
            url = "https://nullsignal.games/blog/category/news/product-announcements/"
            page.goto(url)
            self.progress_bar.setValue(60)

            # Step 4: Extract the post titles (adjust selector based on page structure)
            posts = page.locator(".post-title").all_inner_texts()
            self.progress_bar.setValue(80)

            # Step 5: Compare posts and update status
            if os.path.exists(posts_file):
                with open(posts_file, "r") as file:
                    previous_posts = json.load(file)

                # Find new posts by comparing lists
                new_posts = [post for post in posts if post not in previous_posts]

                if new_posts:
                    self.status_label.setText(f"New posts detected:\n{', '.join(new_posts)}")
                else:
                    self.status_label.setText("No new posts detected.")
            else:
                self.status_label.setText("First-time check; saving current posts.")

            # Save the current posts to the file
            with open(posts_file, "w") as file:
                json.dump(posts, file)

            # Step 6: Complete the progress bar
            self.progress_bar.setValue(100)
            self.check_button.setEnabled(True)  # Re-enable the button

            # Close the browser
            browser.close()

# Main application
if __name__ == "__main__":
    app = QApplication([])
    window = UpdateCheckerApp()
    window.show()
    app.exec_()
