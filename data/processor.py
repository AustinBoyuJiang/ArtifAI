import os

RAW_DATA_DIR = "./raw_data"
PROCESSED_DATA_DIR = "./processed_data"


def process_image(filename, category):
    # Placeholder for your processing logic
    # You'll likely want to use libraries like Pillow for image processing in Python
    # For this example, we're just copying the image from raw_data to processed_data
    raw_path = os.path.join(RAW_DATA_DIR, category, filename)
    processed_path = os.path.join(PROCESSED_DATA_DIR, category, filename)

    # Placeholder processing logic (just a copy for now)
    with open(raw_path, 'rb') as source:
        with open(processed_path, 'wb') as dest:
            dest.write(source.read())


def process_all_in_category(category):
    for filename in os.listdir(os.path.join(RAW_DATA_DIR, category)):
        process_image(filename, category)
