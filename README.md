# Sudoku-Desktop-App

This is a simple desktop application done in Python that allows users to play games of Sudoku with various difficulty levels.

Sudoku games are generated using Python module py-sudoku: pip install py-sudoku
User interface uses tkinter: pip install tk

Once puzzles are generated, their difficulty are configured with a microservice architechture using csv and txt files.

To run the app and generate new games, run both sudoku_app.py and sudokuMS.py as separate processes.
