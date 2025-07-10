from fpdf import FPDF
import pandas as pd
import math

CSV_FILE_PATH = 'vocabulary.csv'
FRONT_COLUMNS = ["Chinese"]
BACK_COLUMNS = ["Pinyin", "English"]

OUTPUT_PDF_PATH = 'flashcards_printable.pdf'
FONT_PATH = 'NotoSansCJKsc-Regular.otf'
FONT_NAME = 'NotoSans'

PAGE_WIDTH = 210
PAGE_HEIGHT = 297

CARD_COLUMNS = 4
CARD_ROWS = 6

FONT_SIZE_BASE = 32

MARK_LENGTH = 0.5  # mm
LINE_WIDTH = 0.01  # mm
LINE_COLOR = (200, 200, 200)


def load_vocabulary(csv_path):
    expected_cols = FRONT_COLUMNS + BACK_COLUMNS
    data = []
    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # skip header
        for row in reader:
            data.append(row)
    return pd.DataFrame(data, columns=expected_cols)


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


def draw_card_content(pdf, x, y, card_width, card_height, texts):
    num_lines = len(texts)

    font_size = max(4, FONT_SIZE_BASE/num_lines)
    pdf.set_font(FONT_NAME, size=font_size)

    total_text_height = num_lines * font_size
    start_y = y + (card_height / 2) - (total_text_height / 2)

    for i, line in enumerate(texts):
        pdf.set_xy(x, start_y + i * font_size)
        pdf.cell(card_width, font_size, text=line, align='C')


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
                    texts = [df.iloc[idx][col_name] for col_name in FRONT_COLUMNS]
                else:
                    texts = [df.iloc[idx][col_name] for col_name in BACK_COLUMNS]

                draw_card_content(pdf, x, y, card_width, card_height, texts)

    pdf.output(OUTPUT_PDF_PATH)


if __name__ == "__main__":
    vocabulary_df = load_vocabulary(CSV_FILE_PATH)
    generate_flashcards_pdf(vocabulary_df)
