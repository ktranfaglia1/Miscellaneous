#  Author: Kyle Tranfaglia
#  Title: DataAnnotations coding problem
#  Last updated: 03/04/25
#  Description: This program uses Pandas and requests packages to read in a table of data from a Google Document
#  and decrypt the secret message using coordinate and character data mapping
import pandas as pd
import requests


def decrypt_google_doc(doc_url):
    # Fetch the HTML content of the Google Doc
    response = requests.get(doc_url)

    # Read all tables from the HTML content
    table = pd.read_html(response.text)

    # Check that tables were found
    if not table:
        print("Debugging: No tables found in the document")
        return

    # Get the required data
    df = table[0]
    print(df)

    # Set the first row as column names and remove it from data
    df.columns = df.iloc[0]
    df = df[1:].reset_index(drop=True)
    df.columns = df.columns.astype(str).str.lower().str.replace("-", "").str.replace(" ", "")

    # Print processed column names
    print("Updated Column Names:", df.columns.tolist())

    # Find the correct column names (This can probably be avoided, but it fixed an extraction issue)
    x_col = next((col for col in df.columns if "xcoordinate" in col), None)
    y_col = next((col for col in df.columns if "ycoordinate" in col), None)
    char_col = next((col for col in df.columns if "character" in col), None)

    # Check if all columns exist (another debugging step)
    if not all([x_col, y_col, char_col]):
        print(f"Missing columns ... Found: {df.columns.tolist()}")
        return

    # Convert coordinate values to numeric type
    df[x_col] = pd.to_numeric(df[x_col], errors='coerce')
    df[y_col] = pd.to_numeric(df[y_col], errors='coerce')

    # Drop rows with invalid coordinates (Should be unnecessary)
    df = df.dropna(subset=[x_col, y_col])

    # Convert coordinates to integers
    df[x_col] = df[x_col].astype(int)
    df[y_col] = df[y_col].astype(int)

    # Extract tuples
    coordinates = list(df[[x_col, char_col, y_col]].itertuples(index=False, name=None))

    # Check if coordinates could be extracted
    if not coordinates:
        print("No valid data found in the table")
        return

    # Determine grid size
    max_x = max(x for x, _, _ in coordinates) + 1
    max_y = max(y for _, _, y in coordinates) + 1

    # Create an empty grid filled with spaces
    grid = [[" " for _ in range(max_x)] for _ in range(max_y)]

    # Fill the grid with characters
    for x, char, y in coordinates:
        grid[y][x] = char

    # Print the grid row by row
    print("\n---------- The Decoded Secret Message: ---------- \n")
    for row in grid:
        print("".join(row))


if __name__ == '__main__':
    # Call the function with the url
    decrypt_google_doc("https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub")
