"""
Groq AI API integration for stress relief assistance.

This module provides age-appropriate AI-generated content for stress relief,
including calming stories, personalized messages, and journal prompts.

Usage Examples:
    # Initialize the helper
    ai = AIHelper()
    
    # Generate a calming story for a child
    story = ai.generate_calming_story(age_group='child')
    print(story)
    
    # Get a calming message for a stressed teen
    message = ai.get_calming_message(age_group='teen', stress_level='stressed')
    print(message)
    
    # Generate journal prompts
    prompts = ai.generate_journal_prompt(
        age_group='adult',
        feelings=['anxious', 'overwhelmed'],
        triggers=['work deadline', 'family conflict']
    )
    print(prompts)
"""

import os
import logging
from typing import List, Optional, Literal
from functools import lru_cache
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


# System prompts for different age groups and use cases
SYSTEM_PROMPTS = {
    'story': {
        'child': """You are a gentle storyteller who creates calming stories for children (ages 0-10).
Use very simple words that a child can understand. Write in a warm, gentle, and reassuring tone.
Keep stories 3-4 paragraphs long. Use themes like:
- Friendly animals in peaceful places
- Gentle adventures with happy endings
- Magical places that feel safe and calm
- Nature scenes that are soothing
Avoid scary elements, conflict, or complex emotions. Focus on peace, safety, and comfort.""",
        
        'teen': """You are a supportive storyteller who creates calming stories for teenagers (ages 10-18).
Use relatable language that teens can connect with. Write in an understanding, non-judgmental tone.
Keep stories 4-5 paragraphs long. Use themes like:
- Overcoming challenges and finding inner strength
- Finding peace in difficult moments
- Connection with nature or meaningful places
- Moments of clarity and self-discovery
- Gentle metaphors for emotional processing
Make it relatable but not preachy. Focus on validation and calm reflection.""",
        
        'adult': """You are a mindfulness-focused storyteller who creates reflective, calming narratives for adults.
Use clear, thoughtful language that encourages reflection. Write in a contemplative, peaceful tone.
Keep stories 4-5 paragraphs long. Use themes like:
- Mindfulness and present-moment awareness
- Finding peace amidst life's challenges
- Nature as a source of calm and perspective
- Gentle reflections on resilience and inner strength
- Metaphors for emotional balance and tranquility
Focus on mindfulness, self-compassion, and finding inner calm."""
    },
    
    'message': {
        'child': """You are a caring, gentle helper speaking to a child (ages 0-10).
Use very simple, warm words. Be reassuring and kind. Keep responses to 2-3 short sentences.
Speak like a caring friend or family member. Use encouraging, supportive language.
Never be judgmental. Focus on comfort and safety.""",
        
        'teen': """You are a supportive, understanding helper speaking to a teenager (ages 10-18).
Use relatable, authentic language. Be non-judgmental and validating. Keep responses to 2-3 sentences.
Acknowledge their feelings without minimizing them. Offer gentle, practical support.
Speak as a trusted friend or mentor. Be real but hopeful.""",
        
        'adult': """You are a mindful, supportive helper speaking to an adult.
Use clear, thoughtful language. Be empathetic and non-judgmental. Keep responses to 2-3 sentences.
Acknowledge the difficulty while offering perspective. Focus on mindfulness and self-compassion.
Speak with wisdom and understanding. Be supportive without being preachy."""
    },
    
    'journal': {
        'child': """You are a gentle guide helping a child (ages 0-10) process their feelings through journaling.
Create 2-3 simple, open-ended questions that help them explore their emotions.
Use very simple words. Make questions feel safe and non-threatening.
Focus on helping them name feelings and understand them better.
Be empathetic and gentle. Avoid complex or overwhelming questions.""",
        
        'teen': """You are a supportive guide helping a teenager (ages 10-18) process their emotions through journaling.
Create 2-3 reflective, open-ended questions that help them explore their feelings and experiences.
Use relatable language. Make questions feel validating and non-judgmental.
Help them process emotions, understand triggers, and find their own insights.
Be empathetic and understanding. Encourage self-reflection without being preachy.""",
        
        'adult': """You are a mindful guide helping an adult process their emotions through journaling.
Create 2-3 reflective, open-ended questions that encourage deep self-reflection.
Use thoughtful, clear language. Make questions feel supportive and non-judgmental.
Help them explore feelings, understand patterns, and find clarity.
Be empathetic and wise. Encourage mindfulness and self-compassion."""
    }
}

# Fallback responses if API fails
FALLBACK_RESPONSES = {
    'story': {
        'child': """Once upon a time, there was a little bunny who loved to sit by a peaceful stream. 
The water made gentle sounds as it flowed over smooth stones. The bunny felt safe and calm there, 
watching the sunlight dance on the water. Everything felt peaceful and good.""",
        
        'teen': """Imagine a quiet moment when everything feels okay. Maybe you're sitting somewhere 
that feels safe, where you can just be yourself. In this moment, you can breathe and know that 
you're doing your best. Sometimes life feels hard, but you have strength inside you. Take a deep 
breath and remember that this feeling will pass.""",
        
        'adult': """In this moment, allow yourself to simply be. Notice your breath, the gentle 
rhythm of your body. You are here, present, and that is enough. Life brings challenges, but you 
also bring resilience. Take a moment to acknowledge your strength, your capacity to find calm 
amidst the storm. You are more capable than you know."""
    },
    
    'message': {
        'child': "It's okay to feel this way. You're safe, and I'm here with you. Take a deep breath.",
        'teen': "I see you're going through a lot right now. Your feelings are valid, and you're not alone in this.",
        'adult': "This is a difficult moment, but you have the strength to navigate it. Be gentle with yourself."
    },
    
    'journal': {
        'child': "How are you feeling right now? What made you feel this way? What helps you feel better?",
        'teen': "What emotions are you experiencing right now? What situations or thoughts triggered these feelings? How can you be kind to yourself in this moment?",
        'adult': "What are you feeling in this moment, and where do you notice it in your body? What patterns or triggers do you notice? How can you practice self-compassion right now?"
    }
}


class AIHelper:
    """
    Handles Groq AI API calls for age-appropriate stress relief content.
    
    Provides calming stories, personalized messages, and journal prompts
    tailored to different age groups (child, teen, adult).
    """
    
    def __init__(self, model: str = "llama-3.1-8b-instant"):
        """
        Initialize the Groq AI client.
        
        Args:
            model: Groq model to use (default: "llama-3.1-8b-instant")
            
        Raises:
            ValueError: If GROQ_API_KEY is not found in environment variables
        """
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            logger.warning("GROQ_API_KEY not found - AI features will use fallback responses")
            self.client = None
        else:
            try:
                self.client = Groq(api_key=api_key)
                logger.info(f"Groq AI client initialized with model: {model}")
            except Exception as e:
                logger.error(f"Failed to initialize Groq client: {str(e)}")
                self.client = None
        
        self.model = model
        self.temperature = 0.75  # Balanced creativity
        self._response_cache = {}  # Simple cache for repeated prompts
    
    def generate_calming_story(self, age_group: Literal['child', 'teen', 'adult'] = 'adult') -> str:
        """
        Generate an age-appropriate calming story using AI.
        
        Creates personalized calming stories with themes and language appropriate
        for the specified age group. Stories are designed to promote relaxation
        and emotional regulation.
        
        Args:
            age_group: Target age group ('child', 'teen', or 'adult')
            
        Returns:
            Generated calming story text (3-5 paragraphs depending on age group)
            
        Example:
            story = ai.generate_calming_story(age_group='child')
            print(story)
        """
        if age_group not in ['child', 'teen', 'adult']:
            logger.warning(f"Invalid age_group: {age_group}, defaulting to 'adult'")
            age_group = 'adult'
        
        # Check cache
        cache_key = f"story_{age_group}"
        if cache_key in self._response_cache:
            logger.debug("Returning cached story")
            return self._response_cache[cache_key]
        
        # User prompt with calming themes
        user_prompt = """Create a calming, peaceful story that helps the reader feel safe and relaxed.
Focus on themes of peace, comfort, and tranquility. Make it engaging but soothing."""
        
        system_prompt = SYSTEM_PROMPTS['story'][age_group]
        
        try:
            if not self.client:
                raise ValueError("Groq client not initialized")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=300,
                temperature=self.temperature
            )
            
            story = response.choices[0].message.content.strip()
            
            # Cache the response
            self._response_cache[cache_key] = story
            
            logger.info(f"Generated calming story for {age_group}")
            return story
            
        except Exception as e:
            logger.error(f"Error generating calming story: {str(e)}")
            fallback = FALLBACK_RESPONSES['story'][age_group]
            logger.info("Using fallback story")
            return fallback
    
    def get_calming_message(
        self, 
        age_group: Literal['child', 'teen', 'adult'] = 'adult',
        stress_level: Literal['calm', 'stressed', 'extreme'] = 'stressed'
    ) -> str:
        """
        Get an immediate, personalized calming message.
        
        Provides brief, supportive messages tailored to the user's age group
        and current stress level. Messages are designed to be immediately
        helpful and non-judgmental.
        
        Args:
            age_group: Target age group ('child', 'teen', or 'adult')
            stress_level: Current stress level ('calm', 'stressed', or 'extreme')
            
        Returns:
            Brief calming message (2-3 sentences)
            
        Example:
            message = ai.get_calming_message(age_group='teen', stress_level='stressed')
            print(message)
        """
        if age_group not in ['child', 'teen', 'adult']:
            logger.warning(f"Invalid age_group: {age_group}, defaulting to 'adult'")
            age_group = 'adult'
        
        if stress_level not in ['calm', 'stressed', 'extreme']:
            logger.warning(f"Invalid stress_level: {stress_level}, defaulting to 'stressed'")
            stress_level = 'stressed'
        
        # Check cache
        cache_key = f"message_{age_group}_{stress_level}"
        if cache_key in self._response_cache:
            logger.debug("Returning cached message")
            return self._response_cache[cache_key]
        
        # Create context-aware user prompt
        stress_context = {
            'calm': "The person is feeling calm and relaxed.",
            'stressed': "The person is experiencing elevated stress and needs support.",
            'extreme': "The person is experiencing extreme stress and needs immediate, gentle support."
        }
        
        user_prompt = f"""Provide a brief, supportive calming message. 
{stress_context[stress_level]}
Keep it to 2-3 sentences. Be immediate, helpful, and non-judgmental."""
        
        system_prompt = SYSTEM_PROMPTS['message'][age_group]
        
        try:
            if not self.client:
                raise ValueError("Groq client not initialized")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=150,
                temperature=self.temperature
            )
            
            message = response.choices[0].message.content.strip()
            
            # Cache the response
            self._response_cache[cache_key] = message
            
            logger.info(f"Generated calming message for {age_group} with {stress_level} stress")
            return message
            
        except Exception as e:
            logger.error(f"Error generating calming message: {str(e)}")
            fallback = FALLBACK_RESPONSES['message'][age_group]
            logger.info("Using fallback message")
            return fallback
    
    def generate_journal_prompt(
        self,
        age_group: Literal['child', 'teen', 'adult'] = 'adult',
        feelings: Optional[List[str]] = None,
        triggers: Optional[List[str]] = None
    ) -> str:
        """
        Generate reflective journal prompts based on user's feelings and triggers.
        
        Creates 2-3 open-ended questions that help the user process their emotions
        and understand their stress patterns. Questions are age-appropriate and
        designed to encourage self-reflection.
        
        Args:
            age_group: Target age group ('child', 'teen', or 'adult')
            feelings: List of feelings/emotions the user is experiencing
            triggers: List of situations or events that triggered stress
            
        Returns:
            Journal prompts as a string (2-3 questions)
            
        Example:
            prompts = ai.generate_journal_prompt(
                age_group='teen',
                feelings=['anxious', 'overwhelmed'],
                triggers=['school exam', 'social pressure']
            )
            print(prompts)
        """
        if age_group not in ['child', 'teen', 'adult']:
            logger.warning(f"Invalid age_group: {age_group}, defaulting to 'adult'")
            age_group = 'adult'
        
        # Build context for the prompt
        context_parts = []
        if feelings:
            context_parts.append(f"Current feelings: {', '.join(feelings)}")
        if triggers:
            context_parts.append(f"Triggers: {', '.join(triggers)}")
        
        context = " ".join(context_parts) if context_parts else "The person is processing their emotions."
        
        # Check cache (with context hash for similar situations)
        cache_key = f"journal_{age_group}_{hash(context)}"
        if cache_key in self._response_cache:
            logger.debug("Returning cached journal prompts")
            return self._response_cache[cache_key]
        
        user_prompt = f"""Create 2-3 reflective journal questions that help process emotions.
{context}
Make the questions open-ended, empathetic, and helpful for self-reflection."""
        
        system_prompt = SYSTEM_PROMPTS['journal'][age_group]
        
        try:
            if not self.client:
                raise ValueError("Groq client not initialized")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=200,
                temperature=self.temperature
            )
            
            prompts = response.choices[0].message.content.strip()
            
            # Cache the response
            self._response_cache[cache_key] = prompts
            
            logger.info(f"Generated journal prompts for {age_group}")
            return prompts
            
        except Exception as e:
            logger.error(f"Error generating journal prompts: {str(e)}")
            fallback = FALLBACK_RESPONSES['journal'][age_group]
            logger.info("Using fallback journal prompts")
            return fallback
    
    def clear_cache(self) -> None:
        """Clear the response cache."""
        self._response_cache.clear()
        logger.info("Response cache cleared")
    
    def get_cache_size(self) -> int:
        """Get the number of cached responses."""
        return len(self._response_cache)


# Example usage

if __name__ == "__main__":
    # Initialize AI helper
    ai = AIHelper()
    
    # Test calming story generation
    print("=== Calming Story (Child) ===")
    story = ai.generate_calming_story(age_group='child')
    print(story)
    print()
    
    # Test calming message
    print("=== Calming Message (Teen, Stressed) ===")
    message = ai.get_calming_message(age_group='teen', stress_level='stressed')
    print(message)
    print()
    
    # Test journal prompts
    print("=== Journal Prompts (Adult) ===")
    prompts = ai.generate_journal_prompt(
        age_group='adult',
        feelings=['anxious', 'overwhelmed'],
        triggers=['work deadline', 'family conflict']
    )
    print(prompts)
    print()
    
    print(f"Cache size: {ai.get_cache_size()}")
