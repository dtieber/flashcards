from fpdf import FPDF
import pandas as pd
import math

CSV_FILE_PATH = 'vocabulary.csv'
OUTPUT_PDF_PATH = 'flashcards_printable.pdf'
FONT_PATH = 'NotoSansCJKsc-Regular.otf'
FONT_NAME = 'NotoSans'

PAGE_WIDTH = 210
PAGE_HEIGHT = 297

CARD_COLUMNS = 4
CARD_ROWS = 6

FONT_SIZE_FRONT = 32
FONT_SIZE_BACK = 14

MARK_LENGTH = 0.5  # mm
LINE_WIDTH = 0.01  # mm
LINE_COLOR = (200, 200, 200)


def load_vocabulary(csv_path):
    data = []
    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # skip header
        for row in reader:
            if len(row) == 3:
                data.append([row[0], row[1], row[2]])
    return pd.DataFrame(data, columns=["Chinese", "Pinyin", "English"])


def draw_crop_marks(pdf, x, y, card_width, card_height, col, row):
    pdf.set_line_width(LINE_WIDTH)
    pdf.set_draw_color(*LINE_COLOR)

    # Top-left corner
    if row != 0:
        pdf.line(x, y, x + MARK_LENGTH, y)
    if col != 0:
        pdf.line(x, y, x, y + MARK_LENGTH)

    # Top-right corner
    if row != 0:
        pdf.line(x + card_width - MARK_LENGTH, y, x + card_width, y)
    if col != CARD_COLUMNS - 1:
        pdf.line(x + card_width, y, x + card_width, y + MARK_LENGTH)

    # Bottom-left corner
    if row != CARD_ROWS - 1:
        pdf.line(x, y + card_height, x + MARK_LENGTH, y + card_height)
    if col != 0:
        pdf.line(x, y + card_height - MARK_LENGTH, x, y + card_height)

    # Bottom-right corner
    if row != CARD_ROWS - 1:
        pdf.line(x + card_width - MARK_LENGTH, y + card_height, x + card_width, y + card_height)
    if col != CARD_COLUMNS - 1:
        pdf.line(x + card_width, y + card_height - MARK_LENGTH, x + card_width, y + card_height)


def draw_card_content(pdf, x, y, card_width, card_height, text, side):
    if side == 'front':
        pdf.set_xy(x, y + (card_height / 2) - (FONT_SIZE_FRONT / 2))
        pdf.cell(card_width, FONT_SIZE_FRONT, text=text, align='C')
    else:
        num_lines = text.count('\n') + 1
        line_height = FONT_SIZE_BACK + 2
        total_text_height = num_lines * line_height
        pdf.set_xy(x, y + (card_height / 2) - (total_text_height / 2))
        pdf.multi_cell(card_width, line_height, text=text, align='C')


def generate_flashcards_pdf(df):
    pdf = FPDF('P', 'mm', 'A4')
    pdf.set_margins(0, 0, 0)
    pdf.set_auto_page_break(False)
    pdf.add_font(FONT_NAME, '', FONT_PATH)

    cards_per_page = CARD_COLUMNS * CARD_ROWS
    card_width = PAGE_WIDTH / CARD_COLUMNS
    card_height = PAGE_HEIGHT / CARD_ROWS
    num_pages = math.ceil(len(df) / cards_per_page)

    for page in range(num_pages):
        for side in ['front', 'back']:
            pdf.add_page()
            pdf.set_font(FONT_NAME, size=FONT_SIZE_FRONT if side == 'front' else FONT_SIZE_BACK)

            for i in range(cards_per_page):
                idx = page * cards_per_page + i
                if idx >= len(df):
                    break

                col = i % CARD_COLUMNS
                row = i // CARD_COLUMNS

                x = col * card_width
                y = row * card_height

                draw_crop_marks(pdf, x, y, card_width, card_height, col, row)

                if side == 'front':
                    text = df.iloc[idx]["Chinese"]
                else:
                    text = f"{df.iloc[idx]['Pinyin']}\n{df.iloc[idx]['English']}"

                draw_card_content(pdf, x, y, card_width, card_height, text, side)

    pdf.output(OUTPUT_PDF_PATH)


if __name__ == "__main__":
    vocabulary_df = load_vocabulary(CSV_FILE_PATH)
    generate_flashcards_pdf(vocabulary_df)
