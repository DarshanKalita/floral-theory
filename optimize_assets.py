import json
import os
from PIL import Image

# --- Configuration ---
JSON_FILE = 'data.json'
MAX_WIDTH = 600
QUALITY = 80  # 80 is the sweet spot for WebP (high quality, tiny file size)

def process_image(img_path):
    # 1. CONDITIONAL CHECK: Ignore external links
    if img_path.startswith(('http://', 'https://')):
        return img_path 

    # Clean up the path (removes leading './' if you accidentally typed it)
    clean_path = img_path.lstrip('./')

    if not os.path.exists(clean_path):
        print(f"⚠️ Warning: File not found - {clean_path}")
        return img_path

    # Generate the new .webp filename
    filename, _ = os.path.splitext(clean_path)
    webp_path = f"{filename}.webp"

    # Skip processing if the WebP file already exists
    if os.path.exists(webp_path):
        print(f"⏭️ Skipped (Already Optimized): {webp_path}")
        return webp_path

    try:
        with Image.open(clean_path) as img:
            # Convert to RGB to prevent errors with transparent PNGs
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')

            # Thumbnail scales the image down to MAX_WIDTH while perfectly preserving aspect ratio
            img.thumbnail((MAX_WIDTH, MAX_WIDTH))
            
            # Save the new optimized WebP file
            img.save(webp_path, 'WEBP', quality=QUALITY)
            
            # Calculate file size reduction for the console output
            old_size = os.path.getsize(clean_path) / 1024
            new_size = os.path.getsize(webp_path) / 1024
            print(f"✅ Optimized: {clean_path} ({old_size:.1f} KB) -> {webp_path} ({new_size:.1f} KB)")

            return webp_path

    except Exception as e:
        print(f"❌ Error processing {clean_path}: {e}")
        return img_path

# --- Main Execution ---
print("Scanning data.json for local images...")

# Load the JSON data
with open(JSON_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Loop through every plant in the archive
for item in data:
    # Check the main image
    if 'image' in item and item['image']:
        item['image'] = process_image(item['image'])
        
    # Check the additional_images array if you have one
    if 'additional_images' in item and isinstance(item['additional_images'], list):
        item['additional_images'] = [process_image(img) for img in item['additional_images']]

# Save the updated paths back to data.json
with open(JSON_FILE, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)

print("Finished. data.json has been updated.")