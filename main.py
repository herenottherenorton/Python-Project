from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QProgressBar, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
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
        self.status_label = QLabel("Checking for updates...", self)
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

        # Check updates button
        self.check_updates_button = QPushButton("Check for Updates", self)
        self.check_updates_button.clicked.connect(self.start_progress)
        self.layout.addWidget(self.check_updates_button)

        self.setLayout(self.layout)

        # Start the progress on startup
        self.start_progress()

    def start_progress(self):
        # Reset the progress bar
        self.progress_bar.setValue(0)
        self.status_label.setText("Checking for updates...")
        self.check_for_new_posts()

    def check_for_new_posts(self):
        # File to store the previous list of post titles
        posts_file = "posts.json"

        # Load the target URLs from the config file
        try:
            with open("config.json", "r") as config_file:
                config = json.load(config_file)
                urls = config["target_urls"]
        except (FileNotFoundError, KeyError) as e:
            self.status_label.setText(f"Configuration error: {e}")
            self.progress_bar.setValue(0)
            return

        all_new_posts = []

        try:
            # Progress milestones
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=True)

                for url in urls:
                    self.progress_bar.setValue(20)

                    # Open a new page
                    page = browser.new_page()
                    self.progress_bar.setValue(40)

                    # Navigate to the URL
                    page.goto(url)
                    self.progress_bar.setValue(60)

                    # Extract the post titles (adjust selector based on page structure)
                    posts = page.locator(".post-title").all_inner_texts()
                    self.progress_bar.setValue(80)

                    # Compare posts and update status
                    if os.path.exists(posts_file):
                        with open(posts_file, "r") as file:
                            previous_posts = json.load(file)

                        # Find new posts by comparing lists
                        new_posts = [post for post in posts if post not in previous_posts]

                        if new_posts:
                            all_new_posts.extend(new_posts)
                    else:
                        self.status_label.setText("First-time check; saving current posts.")

                    # Save the current posts to the file
                    with open(posts_file, "w") as file:
                        json.dump(posts, file)

                # Step 6: Complete the progress bar
                self.progress_bar.setValue(100)

                # Close the browser
                browser.close()

                if all_new_posts:
                    # Display icon and hyperlink for new posts
                    icon = QPixmap("icon.png")
                    self.status_label.setPixmap(icon)
                    self.status_label.setText(f"New posts detected: {', '.join(all_new_posts)}")
                    self.status_label.setOpenExternalLinks(True)
                else:
                    self.status_label.setText("No new posts detected.")

        except Exception as e:
            self.status_label.setText(f"An error occurred: {e}")
            self.progress_bar.setValue(0)

# Main application
if __name__ == "__main__":
    app = QApplication([])
    window = UpdateCheckerApp()
    window.show()
    app.exec_()