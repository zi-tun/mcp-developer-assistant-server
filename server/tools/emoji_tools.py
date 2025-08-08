import mcp.types as types
import logging
import re
import random
from fastmcp import Context

from server.server import mcp


logger = logging.getLogger(__name__)

# Comprehensive emoji mapping for story generation
EMOJI_MAPPING = {
    # Animals
    'cat': '🐱', 'dog': '🐶', 'bird': '🐦', 'fish': '🐟', 'bear': '🐻',
    'lion': '🦁', 'tiger': '🐯', 'elephant': '🐘', 'monkey': '🐵', 'pig': '🐷',
    'cow': '🐄', 'horse': '🐴', 'sheep': '🐑', 'rabbit': '🐰', 'mouse': '🐭',
    'panda': '🐼', 'koala': '🐨', 'fox': '🦊', 'wolf': '🐺', 'frog': '🐸',
    'chicken': '🐔', 'duck': '🦆', 'owl': '🦉', 'bat': '🦇', 'butterfly': '🦋',
    'bee': '🐝', 'spider': '🕷️', 'snake': '🐍', 'turtle': '🐢', 'whale': '🐋',
    'shark': '🦈', 'octopus': '🐙', 'crab': '🦀', 'lobster': '🦞',
    
    # Food & Drinks
    'pizza': '🍕', 'burger': '🍔', 'sandwich': '🥪', 'taco': '🌮', 'hotdog': '🌭',
    'bread': '🍞', 'cheese': '🧀', 'egg': '🥚', 'bacon': '🥓', 'meat': '🍖',
    'apple': '🍎', 'banana': '🍌', 'orange': '🍊', 'grape': '🍇', 'strawberry': '🍓',
    'cherry': '🍒', 'peach': '🍑', 'pineapple': '🍍', 'coconut': '🥥', 'avocado': '🥑',
    'carrot': '🥕', 'corn': '🌽', 'potato': '🥔', 'tomato': '🍅', 'broccoli': '🥦',
    'cake': '🎂', 'cookie': '🍪', 'ice cream': '🍦', 'candy': '🍬', 'chocolate': '🍫',
    'coffee': '☕', 'tea': '🍵', 'beer': '🍺', 'wine': '🍷', 'water': '💧',
    
    # Places & Transportation
    'home': '🏠', 'house': '🏠', 'school': '🏫', 'hospital': '🏥', 'store': '🏪',
    'restaurant': '🍽️', 'beach': '🏖️', 'mountain': '⛰️', 'forest': '🌲', 'city': '🏙️',
    'car': '🚗', 'bus': '🚌', 'train': '🚆', 'plane': '✈️', 'ship': '🚢',
    'bike': '🚲', 'motorcycle': '🏍️', 'rocket': '🚀', 'helicopter': '🚁',
    'space': '🌌', 'moon': '🌙', 'sun': '☀️', 'star': '⭐', 'earth': '🌍',
    
    # People & Emotions
    'man': '👨', 'woman': '👩', 'boy': '👦', 'girl': '👧', 'baby': '👶',
    'person': '👤', 'people': '👥', 'family': '👪', 'couple': '💑',
    'king': '👑', 'queen': '👸', 'prince': '🤴', 'princess': '👸',
    'happy': '😊', 'sad': '😢', 'angry': '😠', 'love': '❤️', 'heart': '💜',
    'laugh': '😂', 'cry': '😭', 'surprise': '😲', 'cool': '😎', 'wink': '😉',
    
    # Objects & Activities
    'book': '📚', 'phone': '📱', 'computer': '💻', 'tv': '📺', 'camera': '📷',
    'money': '💰', 'gift': '🎁', 'balloon': '🎈', 'party': '🎉', 'music': '🎵',
    'guitar': '🎸', 'piano': '🎹', 'microphone': '🎤', 'headphones': '🎧',
    'ball': '⚽', 'basketball': '🏀', 'football': '🏈', 'tennis': '🎾',
    'swimming': '🏊', 'running': '🏃', 'walking': '🚶', 'dancing': '💃',
    'sleeping': '😴', 'eating': '🍽️', 'drinking': '🥤', 'cooking': '👨‍🍳',
    'work': '💼', 'office': '🏢', 'meeting': '👥', 'presentation': '📊',
    
    # Weather & Nature
    'rain': '🌧️', 'snow': '❄️', 'thunder': '⛈️', 'rainbow': '🌈', 'cloud': '☁️',
    'wind': '💨', 'fire': '🔥', 'water': '💧', 'tree': '🌳', 'flower': '🌸',
    'grass': '🌱', 'leaf': '🍃', 'rock': '🗿', 'diamond': '💎',
    
    # Time & Direction
    'morning': '🌅', 'evening': '🌆', 'night': '🌃', 'midnight': '🕛',
    'today': '📅', 'tomorrow': '📆', 'yesterday': '📅',
    'up': '⬆️', 'down': '⬇️', 'left': '⬅️', 'right': '➡️',
    'fast': '💨', 'slow': '🐌', 'big': '📏', 'small': '🤏',
    
    # Actions
    'go': '➡️', 'come': '⬅️', 'stop': '🛑', 'start': '▶️', 'run': '🏃',
    'jump': '🤸', 'fly': '🕊️', 'swim': '🏊', 'climb': '🧗', 'fall': '🍂',
    'give': '🤲', 'take': '✋', 'hold': '🤝', 'throw': '🤾', 'catch': '🤾‍♂️',
    'open': '📂', 'close': '📁', 'break': '💥', 'fix': '🔧', 'build': '🔨',
}

# Fun story templates for variation
STORY_TEMPLATES = [
    "Once upon a time: {story}",
    "Breaking news: {story}",
    "Today's adventure: {story}",
    "Epic tale: {story}",
    "Quick story: {story}",
    "Meanwhile: {story}",
    "Plot twist: {story}",
    "The end: {story}"
]


def text_to_emoji_story(text: str, style: str = "simple") -> str:
    """Convert text to emoji story using different styles."""
    
    words = re.findall(r'\b\w+\b', text.lower())
    emoji_story = []
    
    for word in words:
        if word in EMOJI_MAPPING:
            emoji_story.append(EMOJI_MAPPING[word])
        else:
            # Try to find partial matches for compound words
            found = False
            for emoji_word in EMOJI_MAPPING:
                if emoji_word in word or word in emoji_word:
                    emoji_story.append(EMOJI_MAPPING[emoji_word])
                    found = True
                    break
            
            if not found and style == "creative":
                # Add random emojis for unknown words to keep it fun
                mystery_emojis = ['✨', '🌟', '💫', '🎭', '🎪', '🎨', '🔮', '🎯']
                emoji_story.append(random.choice(mystery_emojis))
    
    result = ''.join(emoji_story)
    
    # Add some storytelling flair based on style
    if style == "dramatic":
        result = f"🎭 {result} 🎬"
    elif style == "magical":
        result = f"✨ {result} ✨"
    elif style == "adventure":
        result = f"🗺️ {result} 🏆"
    elif style == "template":
        template = random.choice(STORY_TEMPLATES)
        result = template.format(story=result)
    
    return result if result else "❓🤷‍♂️❓"


@mcp.tool(
    name="emoji_story_generator",
    description="""
    Transform any text into a fun emoji story! Perfect for icebreakers, 
    making Slack/Teams conversations fun, or creative brainstorming.
    
    Args:
        text (str): The text to convert into emoji story
        style (str): Story style - "simple", "dramatic", "magical", "adventure", "creative", or "template"
    
    Example:
        emoji_story_generator(text="The cat went to space with a sandwich", style="adventure")
        Returns: 🗺️ 🐱🚀🥪 🏆
    """
)
async def emoji_story_generator(text: str, style: str = "simple", ctx: Context = None) -> list[types.TextContent]:
    """Generate emoji stories from text input."""
    try:
        await ctx.info(f"Converting '{text}' to emoji story with {style} style")
        
        emoji_story = text_to_emoji_story(text, style)
        
        result = f"**Original:** {text}\n**Emoji Story:** {emoji_story}"
        
        return [types.TextContent(type="text", text=result)]
    except Exception as e:
        await ctx.error(f"Error generating emoji story: {repr(e)}")
        return [types.TextContent(type="text", text=f"Error: {repr(e)}")]


@mcp.tool(
    name="emoji_conversation_starter",
    description="""
    Generate fun emoji conversation starters and icebreakers.
    Perfect for team meetings, social events, or just breaking the ice!
    
    Args:
        topic (str): Optional topic for the conversation starter (e.g., "work", "food", "travel")
    """
)
async def emoji_conversation_starter(topic: str = "", ctx: Context = None) -> list[types.TextContent]:
    """Generate emoji-based conversation starters."""
    try:
        conversation_starters = {
            "work": [
                "Describe your Monday morning in 3 emojis: 😴☕💻",
                "Your ideal workspace: 🏠🌱☕🎵",
                "Team meeting vibes: 👥💬📊☕",
                "Friday feeling: 🎉🍕🏠",
            ],
            "food": [
                "Perfect meal combo: 🍕🍔🍟🥤",
                "Cooking disaster story: 🔥🍳😱🚒",
                "Midnight snack choice: 🌙🍪🥛",
                "Dream restaurant: 🍝🍷🕯️🎵",
            ],
            "travel": [
                "Dream vacation: 🏖️✈️🏨🍹",
                "Travel nightmare: ✈️⏰😫🧳",
                "Perfect road trip: 🚗🗺️🎵🍿",
                "Weekend getaway: 🏔️🚶‍♂️📸",
            ],
            "general": [
                "Describe your day in emojis: ☀️☕💻🍕🏠",
                "Your spirit animal combo: 🦊🦋🐱",
                "Perfect weather: ☀️🌤️🌈",
                "Mood right now: 😊😴🤔💭",
                "Weekend plans: 🛋️📺🍿 or 🚴‍♂️🌳📸",
                "Coffee or tea story: ☕ vs 🍵",
                "Your superhero power: ⚡🦸‍♀️🌟",
            ]
        }
        
        if topic and topic.lower() in conversation_starters:
            starters = conversation_starters[topic.lower()]
        else:
            starters = conversation_starters["general"]
        
        selected_starter = random.choice(starters)
        
        result = f"**🎪 Conversation Starter 🎪**\n\n{selected_starter}\n\n*Share your emoji response!*"
        
        return [types.TextContent(type="text", text=result)]
    except Exception as e:
        await ctx.error(f"Error generating conversation starter: {repr(e)}")
        return [types.TextContent(type="text", text=f"Error: {repr(e)}")]


@mcp.tool(
    name="emoji_story_variations",
    description="""
    Generate multiple emoji story variations from the same text.
    Great for exploring different creative interpretations!
    
    Args:
        text (str): The text to convert into multiple emoji story variations
    """
)
async def emoji_story_variations(text: str, ctx: Context = None) -> list[types.TextContent]:
    """Generate multiple variations of emoji stories from the same text."""
    try:
        await ctx.info(f"Generating emoji story variations for '{text}'")
        
        styles = ["simple", "dramatic", "magical", "adventure", "creative", "template"]
        variations = []
        
        for style in styles:
            emoji_story = text_to_emoji_story(text, style)
            variations.append(f"**{style.capitalize()} Style:** {emoji_story}")
        
        result = f"**Original Text:** {text}\n\n" + "\n".join(variations)
        
        return [types.TextContent(type="text", text=result)]
    except Exception as e:
        await ctx.error(f"Error generating emoji story variations: {repr(e)}")
        return [types.TextContent(type="text", text=f"Error: {repr(e)}")]


@mcp.tool(
    name="emoji_word_finder",
    description="""
    Find the emoji representation for specific words or phrases.
    Helpful for learning the emoji vocabulary available in the story generator.
    
    Args:
        words (str): Comma-separated words to find emojis for
    """
)
async def emoji_word_finder(words: str, ctx: Context = None) -> list[types.TextContent]:
    """Find emoji representations for specific words."""
    try:
        word_list = [word.strip().lower() for word in words.split(',')]
        found_emojis = []
        not_found = []
        
        for word in word_list:
            if word in EMOJI_MAPPING:
                found_emojis.append(f"**{word}** → {EMOJI_MAPPING[word]}")
            else:
                not_found.append(word)
        
        result = "**🔍 Emoji Dictionary Lookup 🔍**\n\n"
        
        if found_emojis:
            result += "**Found:**\n" + "\n".join(found_emojis)
        
        if not_found:
            result += f"\n\n**Not found:** {', '.join(not_found)}"
            result += "\n\n*Try different words or use creative mode for mystery emojis!*"
        
        return [types.TextContent(type="text", text=result)]
    except Exception as e:
        await ctx.error(f"Error finding emoji words: {repr(e)}")
        return [types.TextContent(type="text", text=f"Error: {repr(e)}")]


@mcp.tool(
    name="random_emoji_challenge",
    description="""
    Generate a random emoji sequence and challenge users to create a story from it.
    Perfect for creative writing exercises and team building activities!
    
    Args:
        length (int): Number of emojis in the challenge (default: 5)
    """
)
async def random_emoji_challenge(length: int = 5, ctx: Context = None) -> list[types.TextContent]:
    """Generate random emoji challenges for creative storytelling."""
    try:
        # Select random emojis from different categories for variety
        all_emojis = list(EMOJI_MAPPING.values())
        challenge_emojis = random.sample(all_emojis, min(length, len(all_emojis)))
        
        emoji_sequence = ' '.join(challenge_emojis)
        
        result = f"**🎯 Emoji Story Challenge 🎯**\n\n"
        result += f"**Your Challenge:** {emoji_sequence}\n\n"
        result += "**Instructions:** Create a fun story using all these emojis!\n"
        result += "*Share your creative interpretation!*"
        
        return [types.TextContent(type="text", text=result)]
    except Exception as e:
        await ctx.error(f"Error generating emoji challenge: {repr(e)}")
        return [types.TextContent(type="text", text=f"Error: {repr(e)}")]