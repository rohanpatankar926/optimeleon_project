from typing import List, Dict, Any
import openai
import os
import re

def generate_headline_subheadline(image_description: str, marketing_insights: List[str], original_headline: Dict[str, str]) -> Dict[str, str]:
    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        headline_tag = re.search(r'<(\w+)', original_headline.get("headline", "<h1>"))
        subheadline_tag = re.search(r'<(\w+)', original_headline.get("subheadline", "<p>"))
        headline_tag = headline_tag.group(1) if headline_tag else "h1"
        subheadline_tag = subheadline_tag.group(1) if subheadline_tag else "p"
        prompt = f"""
        You are an expert copywriter for an e-commerce landing page. Based on the following information, generate a personalized headline and subheadline:
        IMAGE DESCRIPTION: {image_description}
        MARKETING INSIGHTS: {', '.join(marketing_insights)}
        ORIGINAL STRUCTURE:
        - Headline: {original_headline.get("headline", "<h1>Headline</h1>")}
        - Subheadline: {original_headline.get("subheadline", "<p>Subheadline</p>")}
        Requirements:
        1. Match the HTML structure (use <{headline_tag}> and <{subheadline_tag}> tags)
        2. Keep similar length and style as the original
        3. Incorporate themes from the image description
        4. Address pain points and benefits from marketing insights
        5. Make it engaging and conversion-focused
        Return ONLY the JSON with "headline" and "subheadline" keys containing the HTML:
        """
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert copywriter specializing in e-commerce headlines and subheadlines."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        generated_text = response.choices[0].message.content.strip()
        try:
            import json
            result = json.loads(generated_text)
            return {
                "headline": result.get("headline", f"<{headline_tag}>AI Generated Headline</{headline_tag}>"),
                "subheadline": result.get("subheadline", f"<{subheadline_tag}>AI Generated Subheadline</{subheadline_tag}>")
            }
        except json.JSONDecodeError:
            lines = generated_text.split('\n')
            headline = f"<{headline_tag}>AI Generated Headline</{headline_tag}>"
            subheadline = f"<{subheadline_tag}>AI Generated Subheadline</{subheadline_tag}>"
            
            for line in lines:
                if "headline" in line.lower() or "title" in line.lower():
                    headline = f"<{headline_tag}>{line.strip()}</{headline_tag}>"
                elif "subheadline" in line.lower() or "subtitle" in line.lower():
                    subheadline = f"<{subheadline_tag}>{line.strip()}</{subheadline_tag}>"
            
            return {"headline": headline, "subheadline": subheadline}
            
    except Exception as e:
        print(f"Text generation failed: {e}")
        headline_html = original_headline.get("headline", "<h1>Headline</h1>")
        subheadline_html = original_headline.get("subheadline", "<p>Subheadline</p>")
        return {
            "headline": headline_html.replace("First Marathon Journey Begins.", "Your Personalized Marathon Adventure Starts Now!"),
            "subheadline": subheadline_html.replace("", "Join thousands of runners embracing their first marathon with comfort and confidence.")
        }