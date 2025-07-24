from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/generate', methods=['POST'])
def generate_preview():
    data = request.json
    niche = data.get("niche", "your niche")
    product = data.get("product", "a product or offer")
    vibe = data.get("vibe", None)
    
    prompt = f"""Act as a branding expert.
    Target Audience: {niche}
    Product or Offer: {product}"""
    
    if vibe:
        prompt += f"\nBrand Vibe: {vibe}"
    
    prompt += """
    Give one short brand insight (2-3 sentences) and list 3 emotion tags this audience is likely feeling.
    Format the response as:
    Insight: ...
    Tags: [Tag1, Tag2, Tag3]
    """
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7,
        )

        content = response['choices'][0]['message']['content']

        # Split result into insight and tags
        if "Tags:" in content:
            insight_part, tag_part = content.split("Tags:")
            insight = insight_part.replace("Insight:", "").strip()
            tags = [tag.strip() for tag in tag_part.strip(" []\n").split(",")]
        else:
            insight = content.strip()
            tags = []

        return jsonify({"insight": insight, "tags": tags})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
