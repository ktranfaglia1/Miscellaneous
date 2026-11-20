# Miscellaneous

Small, self-contained programming experiments and coding challenges that don't belong to a larger project.

## Contents

| File | Description |
|---|---|
| `Google_Doc_Decrypter.py` | **Grid message decoder.** Downloads a published Google Doc and parses its HTML table with pandas. Each row is a character with x and y coordinates. The script places every character on a grid and prints the grid row by row to reveal a hidden message drawn in block characters. It looks up column names robustly and checks for missing or invalid data. |

## Running

```bash
pip install pandas requests lxml
python Google_Doc_Decrypter.py
```

To decode a different document, pass its published URL to `decrypt_google_doc()`.

**[Kyle Tranfaglia](https://github.com/ktranfaglia1)**
