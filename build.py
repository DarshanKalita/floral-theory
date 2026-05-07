import json
import os

def build_site():
    print("Generating HTML components from external links...")
    
    if not os.path.exists("data.json") or not os.path.exists("template.html"):
        print("Error: Ensure both data.json and template.html exist in this directory.")
        return

    with open("data.json", "r", encoding="utf-8") as f:
        plants = json.load(f)

    html_content = ""
    for plant in plants:
        # Pull the raw GitHub attachment link
        raw_url = plant.get("image", "")
        
        # Apply the proxy strictly for the grid thumbnail to prevent CORS blocks
        proxy_url = f"https://wsrv.nl/?url={raw_url}&w=800&output=webp" if raw_url else ""

        # Click opens the raw link; grid displays the fast proxy
        images_html = f"""
            <a href="{raw_url}" target="_blank" title="Click to view full resolution">
                <img src="{proxy_url}" alt="{plant.get('name', '')}" class="primary-img">
            </a>
        """

        # Handle additional images the exact same way
        if "additional_images" in plant and isinstance(plant["additional_images"], list):
            for extra_img in plant["additional_images"]:
                extra_proxy = f"https://wsrv.nl/?url={extra_img}&w=800&output=webp"
                images_html += f"""
                    <a href="{extra_img}" target="_blank" title="Click to view full resolution">
                        <img src="{extra_proxy}" alt="Additional image for {plant.get('name', '')}">
                    </a>
                """

        html_content += f"""
        <div class="card" id="{plant.get('id', '')}" data-location="{plant.get('location', '')}">
            <div class="image-gallery">
                {images_html}
            </div>
            <div class="card-content">
                <h2>{plant.get('common_name', '')}</h2>
<div class="meta">
                    <span class="meta-name">{plant.get('name', '')}</span>
                    <span class="meta-detail">{plant.get('location', '')}</span>
                    <span class="meta-detail">{plant.get('date', '')}</span>
                </div>                <p class="desc">{plant.get('description', '')}</p>
            </div>
        </div>
        """

    with open("template.html", "r", encoding="utf-8") as f:
        template = f.read()

    final_html = template.replace("{{CONTENT}}", html_content)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(final_html)

    print("✅ Successfully built index.html.")

if __name__ == "__main__":
    build_site()