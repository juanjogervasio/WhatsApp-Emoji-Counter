# WhatsApp Peach Emoji Counter 🍑

In this personal project, I developed a Python script to count the number of peach emojis sent by each user in a WhatsApp group chat. It provides some statistics regarding how this count evolves in time.

### NOTE
Months are counted as 30 days from the first record. For example, if the first peach emoji was sent on July 4th, the program will group counts by 30 days since July 4th and so on.

---
## Installation

Before running the script, install the required Python packages listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

## HOW TO USE

1. Download the chat's `.txt` file from WhatsApp for analysis. The `Dummy_chat.txt` file included in this project can be used for testing.  
2. Save the `txt` file in the same directory as the `peaches.py` file.  
3. Run the `peaches.py` script in terminal.  
4. When asked for the file name, provide the full name of the chat file, including extension.  
5. Press Enter when finished. The program will create the following files:  
   - **mensaje.txt**: a text file with a summary of the previous month's results, formatted for easy copying and pasting into a WhatsApp chat.  
   - **ultimo.png**: a plot showing how each user's count evolved over the previous month.  
   - **historico.png**: a plot showing total counts for each month since the first record. 
