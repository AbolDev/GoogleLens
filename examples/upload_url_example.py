from googlelens import GoogleLens

def main():
    # Initialize the GoogleLens object
    lens = GoogleLens()

    # URL of the image
    image_url = 'https://example.com/path_to_your_image.png'

    # Upload the image from URL and get results
    try:
        results = lens.upload_image(image_url)
        print("Image uploaded from URL successfully!")

        # Extract and print raw text
        raw_text = results.extract_raw_text()
        print("Raw extracted text:", raw_text)

        # Extract and print visual results
        visual_results = results.extract_visual_results()
        print("Extracted visual results:", visual_results)

    except Exception as e:
        print(f"Error during image upload: {e}")

if __name__ == '__main__':
    main()
