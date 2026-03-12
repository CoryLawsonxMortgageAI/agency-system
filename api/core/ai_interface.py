"""
AI Interface - Unified interface for multiple LLM providers
===========================================================
Supports OpenAI, Anthropic, and Groq with automatic fallback.
"""

import os
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class AIInterface:
    """
    Unified interface for AI model interactions.
    Handles multiple providers with automatic fallback.
    """
    
    def __init__(self):
        self.providers = {}
        self._init_providers()
    
    def _init_providers(self):
        """Initialize available AI providers."""
        # OpenAI
        if os.getenv("OPENAI_API_KEY"):
            try:
                from openai import AsyncOpenAI
                self.providers["openai"] = AsyncOpenAI()
                logger.info("✅ OpenAI provider initialized")
            except Exception as e:
                logger.warning(f"⚠️ Failed to initialize OpenAI: {e}")
        
        # Anthropic
        if os.getenv("ANTHROPIC_API_KEY"):
            try:
                from anthropic import AsyncAnthropic
                self.providers["anthropic"] = AsyncAnthropic()
                logger.info("✅ Anthropic provider initialized")
            except Exception as e:
                logger.warning(f"⚠️ Failed to initialize Anthropic: {e}")
        
        # Groq
        if os.getenv("GROQ_API_KEY"):
            try:
                from groq import AsyncGroq
                self.providers["groq"] = AsyncGroq()
                logger.info("✅ Groq provider initialized")
            except Exception as e:
                logger.warning(f"⚠️ Failed to initialize Groq: {e}")
        
        if not self.providers:
            logger.error("❌ No AI providers available. Set at least one API key.")
    
    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: int = 4000
    ) -> Dict[str, Any]:
        """
        Generate completion using the appropriate provider.
        Falls back to available providers if primary fails.
        """
        # Determine provider from model name
        provider = self._get_provider_for_model(model)
        
        if provider not in self.providers:
            # Try fallback providers
            for fallback in ["openai", "anthropic", "groq"]:
                if fallback in self.providers:
                    provider = fallback
                    model = self._get_default_model(fallback)
                    break
        
        if provider not in self.providers:
            raise RuntimeError("No AI providers available")
        
        # Generate based on provider
        if provider == "openai":
            return await self._generate_openai(
                system_prompt, user_prompt, model, temperature, max_tokens
            )
        elif provider == "anthropic":
            return await self._generate_anthropic(
                system_prompt, user_prompt, model, temperature, max_tokens
            )
        elif provider == "groq":
            return await self._generate_groq(
                system_prompt, user_prompt, model, temperature, max_tokens
            )
        
        raise RuntimeError(f"Unknown provider: {provider}")
    
    def _get_provider_for_model(self, model: str) -> str:
        """Determine provider from model name."""
        model_lower = model.lower()
        
        if "gpt" in model_lower or "davinci" in model_lower:
            return "openai"
        elif "claude" in model_lower:
            return "anthropic"
        elif "llama" in model_lower or "mixtral" in model_lower:
            return "groq"
        
        return "openai"  # Default
    
    def _get_default_model(self, provider: str) -> str:
        """Get default model for provider."""
        defaults = {
            "openai": "gpt-4",
            "anthropic": "claude-3-opus-20240229",
            "groq": "llama2-70b-4096"
        }
        return defaults.get(provider, "gpt-4")
    
    async def _generate_openai(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str,
        temperature: float,
        max_tokens: int
    ) -> Dict[str, Any]:
        """Generate using OpenAI API."""
        client = self.providers["openai"]
        
        response = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return {
            "content": response.choices[0].message.content,
            "tokens_used": response.usage.total_tokens if response.usage else None,
            "model": response.model,
            "provider": "openai",
            "cost": self._estimate_cost(response.usage.total_tokens, model) if response.usage else None
        }
    
    async def _generate_anthropic(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str,
        temperature: float,
        max_tokens: int
    ) -> Dict[str, Any]:
        """Generate using Anthropic API."""
        client = self.providers["anthropic"]
        
        response = await client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )
        
        return {
            "content": response.content[0].text,
            "tokens_used": response.usage.input_tokens + response.usage.output_tokens if response.usage else None,
            "model": response.model,
            "provider": "anthropic",
            "cost": None  # Calculate based on usage
        }
    
    async def _generate_groq(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str,
        temperature: float,
        max_tokens: int
    ) -> Dict[str, Any]:
        """Generate using Groq API."""
        client = self.providers["groq"]
        
        response = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return {
            "content": response.choices[0].message.content,
            "tokens_used": response.usage.total_tokens if response.usage else None,
            "model": response.model,
            "provider": "groq",
            "cost": None
        }
    
    def _estimate_cost(self, tokens: int, model: str) -> float:
        """Estimate API cost based on tokens used."""
        # Pricing per 1K tokens (approximate)
        pricing = {
            "gpt-4": 0.03,
            "gpt-4-turbo": 0.01,
            "gpt-3.5-turbo": 0.0015,
            "claude-3-opus": 0.015,
            "claude-3-sonnet": 0.003
        }
        
        rate = pricing.get(model, 0.01)
        return (tokens / 1000) * rate
