# GoogleLens

GoogleLens is a Python library that allows you to perform image searches using Google Lens. You can upload images via URLs, file paths, or binary data and retrieve visual match results.

## Installation

You can install the library via pip:

```bash
pip install GoogleLens
```

## Features

- Upload images from a URL, file path, or binary data.
- Extract raw text or structured visual match data from the Google Lens response.
- Retrieve the main and similar visual match results, including titles, thumbnails, and page URLs.

## Usage

### Uploading Images and Retrieving Results

#### Example 1: Upload image from URL

```python
from googlelens import GoogleLens

# Initialize GoogleLens instance
lens = GoogleLens()

# Upload image from URL
url = "https://example.com/sample-image.jpg"
result_url = lens.upload_image(url)

# Extract and print visual match results
print("Results from URL search:")
print(result_url.extract_visual_results())
```

#### Example 2: Upload image from file path

```python
from googlelens import GoogleLens

# Initialize GoogleLens instance
lens = GoogleLens()

# Upload image from a file path
file_path = "path/to/sample-image.jpg"
result_file = lens.upload_image(file_path)

# Extract and print visual match results
print("Results from file search:")
print(result_file.extract_visual_results())
```

#### Example 3: Upload image using bytes

```python
from googlelens import GoogleLens

# Initialize GoogleLens instance
lens = GoogleLens()

# Read image as bytes
with open("path/to/sample-image.jpg", "rb") as f:
    image_bytes = f.read()

# Upload image using bytes
result_bytes = lens.upload_image(image_bytes)

# Extract and print visual match results
print("Results from bytes search:")
print(result_bytes.extract_visual_results())
```

### Extracting Raw Text

You can also extract raw text from the Google Lens results, if available:

```python
# Extract raw text from the Google Lens response
raw_text = result_url.extract_raw_text()
print("Raw text extracted from the response:")
print(raw_text)
```

## API Reference

### `GoogleLens`

Main class to interact with Google Lens.

- `upload_image(image_input: Union[str, bytes]) -> GoogleLensResults`
  - Uploads an image to Google Lens and returns the search results.
  - `image_input`: Can be a URL (str), file path (str), or binary data (bytes).
  
### `GoogleLensResults`

Handles the parsing and extraction of useful data from the Google Lens response.

- `extract_visual_results() -> Dict[str, Union[None, Dict[str, str], List[Dict[str, str]]]]`
  - Extracts the visual match results including the main match and a list of similar matches.
  
- `extract_raw_text() -> List[str]`
  - Extracts raw text from the Google Lens response, if available.

## Contributing

Feel free to submit issues or pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License.
