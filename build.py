import json
import os
import urllib.parse

# def optimize_url(raw_url, width=800):
#     """
#     Passes the raw GitHub image URL through a free CDN proxy to 
#     resize, compress, and convert it to WebP format instantly.
#     """
#     encoded_url = urllib.parse.quote(raw_url, safe='')
#     return f"https://wsrv.nl/?url={encoded_url}&w={width}&output=webp&we"

def optimize_url(url):
    # If it's a local file (doesn't start with http), return it exactly as is
    if not url.startswith('http'):
        return url
        
    # Otherwise, apply the proxy to external links
    return f"https://wsrv.nl/?url={url}&w=800&output=webp"



def build_site():
    print("Reading data.json...")
    try:
        with open('data.json', 'r') as f:
            plants = json.load(f)
    except FileNotFoundError:
        print("Error: data.json not found.")
        return

    print("Generating HTML components with optimized images and hi-res links...")
    html_content = ""
    for plant in plants:
        
        # Optimize the primary image and link it to the raw high-res version
        raw_primary_url = plant["image"]
        primary_opt_url = optimize_url(raw_primary_url)
        
        images_html = f"""
        <a href="{raw_primary_url}" target="_blank" title="Click to view full resolution">
            <img src="{primary_opt_url}" alt="{plant["name"]}" class="primary-img" loading="lazy">
        </a>
        """
        
        # Process additional images if they exist
        if "additional_images" in plant and isinstance(plant["additional_images"], list):
            for i, extra_img in enumerate(plant["additional_images"]):
                extra_opt_url = optimize_url(extra_img)
                images_html += f"""
                <a href="{extra_img}" target="_blank" title="Click to view full resolution">
                    <img src="{extra_opt_url}" alt="{plant["name"]} - Image {i+2}" class="additional-img" loading="lazy">
                </a>
                """

        # Build individual cards
        card = f"""
        <article class="card" id="{plant['id']}" data-location="{plant.get('location', '')}">
            <div class="image-gallery">
                {images_html}
            </div>
            <div class="card-content">
                <h2>{plant['common_name']}</h2>
                <div class="meta">{plant.get('name', '')} | <span class="loc-text">{plant.get('location', '')}</span> | {plant.get('date', '')}</div>
                <p class="desc">{plant.get('description', '')}</p>
            </div>
        </article>
        """
        html_content += card

    print("Injecting into template.html...")
    try:
        with open('template.html', 'r') as f:
            template = f.read()
    except FileNotFoundError:
        print("Error: template.html not found.")
        return

    final_html = template.replace('{{CONTENT}}', html_content)

    with open('index.html', 'w') as f:
        f.write(final_html)

    print("Success! index.html generated.")

if __name__ == "__main__":
    build_site()