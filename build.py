import json
import os

def build_site():
    print("Reading data.json...")
    try:
        with open('data.json', 'r') as f:
            plants = json.load(f)
    except FileNotFoundError:
        print("Error: data.json not found.")
        return

    print("Generating HTML components...")
    html_content = ""
    for plant in plants:
        
        # Build the image gallery HTML
        images_html = f'<img src="{plant["image"]}" alt="{plant["name"]}" class="primary-img" loading="lazy">'
        
        if "additional_images" in plant and isinstance(plant["additional_images"], list):
            for i, extra_img in enumerate(plant["additional_images"]):
                images_html += f'<img src="{extra_img}" alt="{plant["name"]} - Image {i+2}" class="additional-img" loading="lazy">'

        # Build individual cards
        card = f"""
        <article class="card" id="{plant['id']}">
            <div class="image-gallery">
                {images_html}
            </div>
            <div class="card-content">
                <h2>{plant['name']}</h2>
                <div class="meta">{plant.get('common_name', '')} | {plant.get('location', '')} | {plant.get('date', '')}</div>
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