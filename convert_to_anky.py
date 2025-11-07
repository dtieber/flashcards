import pandas as pd

vocabulary_file = 'vocabulary.csv'
output_path = 'anki_vocab.csv'

vocab_df = pd.read_csv(vocabulary_file)
anki_df = pd.DataFrame({
    'Front': vocab_df['Chinese'],
    'Back': vocab_df['Pinyin'] + ' – ' + vocab_df['English']
})

anki_df.to_csv(output_path, index=False, header=False, encoding='utf-8')
print(f"Anki-compatible vocabulary file saved to {output_path} with {len(anki_df)} entries.")
