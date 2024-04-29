from mastodon import Mastodon
import os
import sys
import tempfile
from pdf2image import convert_from_path

def pdf_to_png(source, destino):
    print(f"Converting {source} to {destino}")
    images = convert_from_path(pdf_path=source, dpi=100, output_folder=destino, fmt="png", output_file="fax", single_file=True)

    # Diagnostic messages to confirm the conversion result
    if images:
        print(f"Conversion successful: {images}")
    else:
        print("Conversion failed. No images were created.")

def init_api():
    mastodon_client_id = os.getenv('MASTODON_CLIENT_KEY')
    mastodon_client_secret = os.getenv('MASTODON_CLIENT_SECRET')
    mastodon_access_token = os.getenv('MASTODON_ACCESS_TOKEN')
    mastodon_api_base_url = os.getenv('MASTODON_API_BASE_URL')

    if not all([mastodon_client_id, mastodon_client_secret, mastodon_access_token, mastodon_api_base_url]):
        print("Mastodon credentials are incorrect or missing, exiting.")
        print_usage()

    print("Initializing Mastodon API")
    mastodon = Mastodon(
        client_id=mastodon_client_id,
        client_secret=mastodon_client_secret,
        access_token=mastodon_access_token,
        api_base_url=mastodon_api_base_url
    )

    return mastodon


def send_toot(mastodon, txt, img_path):
    print(f"Uploading media from {img_path}")

    # Check if the file exists
    if not os.path.isfile(img_path):
        print(f"File not found: {img_path}")
        return

    try:
        with open(img_path, 'rb') as f:
            media = mastodon.media_post(f, mime_type='image/png')

        print(f"Setting Toot text to \"{txt}\" and marking media as sensitive")
        mastodon.status_post(status=txt, media_ids=[media], sensitive=True)
        print("Toot posted successfully with sensitive media.")

    except Exception as e:
        print(f"An error occurred: {e}")


def print_usage():
    print("Converts the first page of a PDF to an image and posts it to Mastodon.")
    print("")
    print("Mastodon API Credentials are supplied as environment variables:")
    print("MASTODON_CLIENT_KEY")
    print("MASTODON_CLIENT_SECRET")
    print("MASTODON_ACCESS_TOKEN")
    print("MASTODON_API_BASE_URL")
    print("")
    print("Usage:")
    print("'pdf_to_mastodon.py [PATH TO PDF] [TEXT TO TOOT]")

def main():
    if len(sys.argv) < 3:
        print("pdf_path and toot_text arguments are required")
        print_usage()

    pdf_path = sys.argv[1]
    toot_text = sys.argv[2]

    if not pdf_path or not toot_text:
        print("pdf_path or toot_text was None")
        print_usage()

    print(f"Starting pdf_to_mastodon")
    mastodon = init_api()

    with tempfile.TemporaryDirectory() as path:
        pdf_to_png(pdf_path, path)
        img_path = os.path.join(path, "fax.png")  # Correctly form the image path
        print(f"Generated image path: {img_path}")  # Diagnostic message for image path
        send_toot(mastodon, toot_text, img_path)

if __name__ == "__main__":
    main()

