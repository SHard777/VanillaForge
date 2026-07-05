import glob
from pypdf import PdfReader
total_chars = 0
files = glob.glob('*.pdf')
for f in files:
    try:
        reader = PdfReader(f)
        text = ''.join([p.extract_text() for p in reader.pages])
        total_chars += len(text)
        print(f'{f}: {len(text)} chars (~{len(text)//4} tokens)')
    except Exception as e:
        print(f'Error reading {f}: {e}')
print(f'\nTotal Chars: {total_chars}')
print(f'Total Est. Tokens: {total_chars // 4}')
