
# Project Summary

This project scrapes LinkedIn profiles and generates profile insights, e.g. years of work experience, whether they went to an international school etc.

# How to run

1. Install Poetry package manager: https://python-poetry.org/docs/#installation

1. OPTIONAL: Change Poetry settings so Python virtual environment is created WITHIN the project directory.

    ```
    poetry config virtualenvs.in-project true
    ```

   - I do this because Selenium webdriver might need to be configured if your computer runs Apple's new ARM-based chips.
     - HOW: I edit the 'webdriver_manager' package source code directly within my local '.venv'.


1. Install all dependencies:

   ```
   poetry install
   ```

1. Configure '.env' file with:
   - Your LinkedIn login details
   - LinkedIn search link
     - HOW TO FIND: Go to LinkedIn's search bar, enter your search terms, press enter and copy the resultant URL.
   - Number of profiles you want to scrape.
1. Finally, run the program:
   ```
   cd src 

   poetry run python M0100_Search.py 

   (then)

   poetry run python M0200_Profile_Scraping.py 
   
   poetry run python M0300_Generate_Insights.py

   poetry run python M0400_File_Generation.py
   ```
   - The program is split into four stages because at every stage, you might want to manually check the data for scraping errors.

# Future goals:
  - Deal with 'suspicious login attempt' popup.
  - Handle sections that have have too much information and requires you to click 'see all' to show all data.

