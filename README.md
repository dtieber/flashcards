# Generate Flashcards 📇
A simple script to generate flashcards.

### Configuration
Customize your flashcards by selecting which columns appear on the front and back. For example:
```
FRONT_COLUMNS = ["Chinese"]
BACK_COLUMNS = ["Pinyin", "English"]
```
📌 Important: The column names in your vocabulary CSV must exactly match those specified in FRONT_COLUMNS and BACK_COLUMNS. 

### Vocabulary
Your vocabulary.csv could look something like this:
```
Chinese,Pinyin,English
一,yī,one
二,èr,two
三,sān,three
```

### Run script
First, you have to install the dependencies with `pip install -r requirements.txt`.
You'll also have to download the font `NotoSansCJKsc-Regular.otf` and copy it to this folder.
Now you can execute the script with `python3 generate_flashcards.py`.
