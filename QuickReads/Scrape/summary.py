import nltk
import csv
import os
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

# Download NLTK resources
nltk.download('stopwords')
nltk.download('popular')

# Function to read text from CSV file
def read_text_from_csv(filename):
    texts = []
    with open(filename, 'r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            text = row['Content']  # Assuming the text is in 'Content' column
            texts.append(text)
    return texts

# Function to tokenize and generate summary for each text
def generate_summary(texts):
    stopWords = set(stopwords.words("english"))
    summaries = []

    for text in texts:
        paragraphs = text.split('\n')  # Splitting text into paragraphs
        concatenated_text = ' '.join(paragraphs)  # Concatenating paragraphs
        words = word_tokenize(concatenated_text)  # Tokenizing concatenated text

        freqTable = dict()
        for word in words:
            word = word.lower()
            if word in stopWords:
                continue
            if word in freqTable:
                freqTable[word] += 1
            else:
                freqTable[word] = 1

        sentences = sent_tokenize(concatenated_text)
        sentenceValue = dict()

        for sentence in sentences:
            for word, freq in freqTable.items():
                if word in sentence.lower():
                    if sentence in sentenceValue:
                        sentenceValue[sentence] += freq
                    else:
                        sentenceValue[sentence] = freq

        if sentenceValue:
            sumValues = 0
            for sentence in sentenceValue:
                sumValues += sentenceValue[sentence]

            average = int(sumValues / len(sentenceValue))

            summary = ''
            word_count = 0
            for sentence in sentences:
                if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
                    words_in_sentence = word_tokenize(sentence)
                    word_count += len(words_in_sentence)
                    if word_count <= 160:  # Adjusted word count for summary length
                        summary += " " + sentence
                    else:
                        break
            summaries.append(summary)
        else:
            summaries.append("No text found in 'Content' column.")

    return summaries

# Function to process a CSV file and update it with summaries
def process_csv(input_csv_filename):
    # Read text from CSV file
    texts = read_text_from_csv(input_csv_filename)

    # Generate summaries
    summaries = generate_summary(texts)

    # Check if 'Field1' already exists
    with open(input_csv_filename, 'r', encoding='utf-8-sig') as check_file:
        reader = csv.DictReader(check_file)
        fieldnames = reader.fieldnames
        if 'Field1' not in fieldnames:
            fieldnames.append('Field1')  # Add 'Field1' if it doesn't exist

    # Update 'Content' column with summaries
    with open(input_csv_filename, 'r', encoding='utf-8-sig') as input_file, \
         open('temp.csv', 'w', newline='', encoding='utf-8-sig') as output_file:
        csv_reader = csv.DictReader(input_file)
        csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        csv_writer.writeheader()

        for row, summary in zip(csv_reader, summaries):
            row['Field1'] = summary
            csv_writer.writerow(row)

    # Replace original file with updated one
    os.replace('temp.csv', input_csv_filename)

# Input CSV file names
input_csv_filenames = ['healthline_articles.csv', 'Technology_articles.csv','Education_articles.csv',
                       'Politics_articles.csv','Business_articles.csv','Movies_articles.csv','Nature_articles.csv',
                       'Sports_articles.csv','Travel_articles.csv']

# Process each CSV file
for filename in input_csv_filenames:
    process_csv(filename)
