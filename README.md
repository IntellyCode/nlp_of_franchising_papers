
# LDA on PDF Files

**Version:** Alpha 1.0.0

## Overview

This project allows you to run Latent Dirichlet Allocation (LDA) on PDF files, utilizing Gensim for modeling and PyLDAvis for visualization. It supports multithreading capabilities to enhance performance and efficiency.

## Installation

To get started, follow these steps:

1. **Clone the Repository**: Download or clone the repository to your local machine.
   
   ```bash
   git clone <repository_url>
   ```
2. **Python Version**: Ensure you have python version 3.12 or later installed on your device. 


3. **Install Dependencies**: Navigate to the project directory and install the required packages using pip:

   ```bash
   pip install -r requirements.txt
   ```
4. **Install NLP Library**: Download the spacy language model

   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Run the Main File**: Locate the main file in the project and execute it in the Python interpreter or run it directly:

   ```bash
   python main.py
   ```

## User Manual

1. **Select PDF Files**: In the left window, choose the PDF files you wish to include from your directories. You can do this by double-clicking or pressing Enter.

2. **Adjust Parameters**: In the top right section, adjust the LDA parameters. Only modify these settings if you are knowledgeable about them, as proper error handling for incorrect configurations is not yet implemented.

3. **Set Output Directory**: Specify the directory where you want to save the output files (e.g., for macOS: `/Users/<user>/Desktop`).

4. **View Selected PDFs**: The bottom panel displays the selected PDF files. 

5. **Start Processing**: Click the "Start" button to create one LDA model for all the selected files.

6. **Clear Selection**: Click "Clear" to remove all files and create a new LDA model. 

7. **Multithreading**: The application supports parallel processing. After clicking "Start," you can immediately click "Clear," select a new batch of files, and click "Start" again. The number of output files will correspond to the number of batches processed.

## Known Issues

- The progress bar currently has some bugs; it only reflects the progress of reading the files. 
- The visualization process may take some time. If you click "Start" and the console or GUI does not display any errors (Warnings, Critical errors, or General Errors), the process is likely running smoothly.
