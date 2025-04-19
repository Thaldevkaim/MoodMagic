import os
from typing import List, Dict, Optional
from dotenv import load_dotenv
from openai import OpenAI
import json
from config import settings

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)

class AIGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate_moodboard_content(self, theme: str, style: str, color_palette: list, mood: str, additional_notes: str = ""):
        prompt = f"""
        Create a moodboard for a {theme} project with {style} style.
        Color palette: {', '.join(color_palette)}
        Mood: {mood}
        Additional notes: {additional_notes}
        
        Please provide:
        1. A creative title
        2. A detailed description
        3. 3-5 key visual elements
        4. 2-3 font pairings
        5. 3-5 texture suggestions
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a creative design assistant specializing in moodboards."},
                {"role": "user", "content": prompt}
            ]
        )
        
        content = response.choices[0].message.content
        return {
            "title": content.split("\n")[0].strip(),
            "description": content.split("\n")[1].strip(),
            "visual_elements": content.split("\n")[2:5],
            "fonts": content.split("\n")[5:7],
            "textures": content.split("\n")[7:]
        }

    def generate_mood_content(self, vibe_text: str, tags: List[str]) -> Dict:
        """
        Generate moodboard content using OpenAI's GPT-4.
        
        Args:
            vibe_text: Description of the desired vibe/mood
            tags: List of style tags
            
        Returns:
            Dictionary containing:
            - color_palette: List of 3 HEX color codes
            - fonts: List with one font pair (heading and body)
            - headline: One-line headline
            - tagline: Short, poetic tagline
        """
        try:
            # Construct the prompt
            prompt = f"""You are a creative design assistant.

Given this mood description and tags, generate a brand design moodboard summary.

Mood: {vibe_text}
Tags: {', '.join(tags)}

Respond with:
1. Three HEX color codes that match the mood.
2. A Google Fonts heading and body font pair.
3. A one-line headline.
4. A short, poetic tagline.

Respond in JSON format:
{{
  "color_palette": [...],
  "fonts": [{{ "heading": "...", "body": "..." }}],
  "headline": "...",
  "tagline": "..."
}}"""
            
            # Call OpenAI API with new format
            completion = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a creative design assistant specializing in brand design and moodboards."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            # Parse the response
            content = completion.choices[0].message.content
            try:
                # Try to parse the JSON response
                return json.loads(content)
            except json.JSONDecodeError:
                # If JSON parsing fails, return default content
                return {
                    "color_palette": ["#EAE0D5", "#DAD2BC", "#A99985"],
                    "fonts": [{"heading": "Playfair Display", "body": "Poppins"}],
                    "headline": "Simplicity Shaped by the Future",
                    "tagline": "A dance between silence and structure."
                }
            
        except Exception as e:
            print(f"Error generating content: {e}")
            return {
                "color_palette": ["#EAE0D5", "#DAD2BC", "#A99985"],
                "fonts": [{"heading": "Playfair Display", "body": "Poppins"}],
                "headline": "Simplicity Shaped by the Future",
                "tagline": "A dance between silence and structure."
            }

    def _generate_text(self, prompt: str, max_tokens: int = 150) -> str:
        """
        Generate text using OpenAI's GPT model
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a creative design assistant specializing in moodboards and visual aesthetics."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating text: {e}")
            return ""

    def _parse_font_pairs(self, response: str) -> List[Dict]:
        """
        Parse font pairs from the AI response
        """
        pairs = []
        lines = response.split('\n')
        for line in lines:
            if ':' in line:
                parts = line.split(':')
                if len(parts) == 2:
                    heading, body = parts
                    pairs.append({
                        "heading": heading.strip(),
                        "body": body.strip()
                    })
        return pairs[:2]  # Return only the first two pairs

    def _parse_copy(self, response: str) -> tuple:
        """
        Parse headline and tagline from the AI response
        """
        headline = "Where Design Meets Inspiration"
        tagline = "Design that speaks to the soul"
        
        lines = response.split('\n')
        for line in lines:
            if line.startswith('Headline:'):
                headline = line.replace('Headline:', '').strip()
            elif line.startswith('Tagline:'):
                tagline = line.replace('Tagline:', '').strip()
        
        return headline, tagline

    def _get_fallback_content(self) -> Dict:
        """
        Return fallback content in case of errors
        """
        return {
            "color_palette": ["#EAE0D5", "#DAD2BC", "#A99985"],
            "fonts": [{"heading": "Playfair Display", "body": "Poppins"}],
            "headline": "Simplicity Shaped by the Future",
            "tagline": "A dance between silence and structure."
        }

    async def generate_color_palette(self, vibe: str) -> List[str]:
        """
        Generate a color palette based on the vibe description
        """
        try:
            prompt = f"""Generate a color palette for a {vibe} design.
            Return exactly 3 hex color codes separated by commas.
            Example format: #FFFFFF, #000000, #FF0000
            Colors should be harmonious and match the described aesthetic."""
            
            response = await self._generate_text(prompt)
            if response:
                return [color.strip() for color in response.split(',')]
            return []
        except Exception as e:
            print(f"Error generating color palette: {e}")
            return []

    async def generate_font_pair(self, vibe: str) -> dict:
        """
        Generate a font pair (heading and body) based on the vibe
        """
        try:
            prompt = f"""Suggest a font pair for a {vibe} design.
            Return in format 'heading:body'.
            Use only Google Fonts.
            Example: Playfair Display:Inter"""
            
            response = await self._generate_text(prompt)
            if response:
                heading, body = response.split(':')
                return {
                    "heading": heading.strip(),
                    "body": body.strip()
                }
            return {"heading": "Playfair Display", "body": "Inter"}
        except Exception as e:
            print(f"Error generating font pair: {e}")
            return {"heading": "Playfair Display", "body": "Inter"}

    async def generate_headline(self, vibe: str) -> str:
        """
        Generate a catchy headline based on the vibe
        """
        try:
            prompt = f"""Generate a catchy headline for a {vibe} brand.
            Keep it under 10 words.
            Make it memorable and impactful."""
            
            response = await self._generate_text(prompt, max_tokens=50)
            return response or "Where Design Meets Inspiration"
        except Exception as e:
            print(f"Error generating headline: {e}")
            return "Where Design Meets Inspiration"

    async def generate_tagline(self, vibe: str) -> str:
        """
        Generate a tagline based on the vibe
        """
        try:
            prompt = f"""Generate a short tagline for a {vibe} brand.
            Keep it under 15 words.
            Make it poetic and evocative."""
            
            response = await self._generate_text(prompt, max_tokens=50)
            return response or "Design that speaks to the soul"
        except Exception as e:
            print(f"Error generating tagline: {e}")
            return "Design that speaks to the soul"

    async def generate_image_prompt(self, keywords: List[str]) -> Optional[str]:
        """
        Generate a detailed image generation prompt from keywords
        """
        try:
            prompt = f"Create a detailed image generation prompt for a moodboard with these keywords: {', '.join(keywords)}"
            response = await self._generate_text(prompt)
            return response
        except Exception as e:
            print(f"Error generating image prompt: {e}")
            return None

    async def generate_image(self, prompt: str) -> Optional[str]:
        """
        Generate an image using Stable Diffusion
        """
        try:
            # TODO: Implement Stable Diffusion API call
            # This is a placeholder for the actual implementation
            return f"Generated image URL for prompt: {prompt}"
        except Exception as e:
            print(f"Error generating image: {e}")
            return None

    async def generate_moodboard_suggestions(self, keywords: List[str]) -> List[str]:
        """
        Generate additional keyword suggestions for a moodboard
        """
        try:
            prompt = f"Suggest 5 related keywords or themes for a moodboard with these keywords: {', '.join(keywords)}"
            response = await self._generate_text(prompt)
            if response:
                return [s.strip() for s in response.split('\n') if s.strip()]
            return []
        except Exception as e:
            print(f"Error generating suggestions: {e}")
            return []

# Example usage
if __name__ == "__main__":
    generator = AIGenerator()
    vibe = "minimalist scandinavian"
    tags = ["modern", "cozy", "neutral"]
    
    content = generator.generate_mood_content(vibe, tags)
    print("Generated Content:")
    print(f"Colors: {content['color_palette']}")
    print("Fonts:")
    for font in content['fonts']:
        print(f"- {font['heading']} / {font['body']}")
    print(f"Headline: {content['headline']}")
    print(f"Tagline: {content['tagline']}") 