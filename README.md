Super Proof of concept for checking to see if a website has any new content on the page specified.

# Patch Notes

## Version 1.1.0 - March 14, 2025

### Changes:
1. **Error Handling**:
   - Added a `try-except` block in the `check_for_new_posts` method to handle potential exceptions during the web scraping process.
   - Updated the status label to provide feedback in case of errors.

2. **User Feedback**:
   - Ensured the progress bar and button states are reset in case of an error.

### Detailed Changes:
- **main.py**:
  - Wrapped the web scraping logic inside a `try-except` block to catch and handle exceptions.
  - Updated the `status_label` to display error messages if an exception occurs.
  - Reset the progress bar and re-enabled the check button in case of an error.