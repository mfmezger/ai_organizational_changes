"""Utils for initialization of LLM agents."""

from dotenv import load_dotenv
from pydantic_ai import Agent
import os
from pydantic_ai.models.cohere import CohereModel, CohereModelSettings
from pydantic_ai.providers.cohere import CohereProvider
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from ai_organizational_changes.model import JobReplacementPrediction
from pydantic_ai.models.openai import OpenAIResponsesModelSettings

load_dotenv(override=True)

# Providers that require their own SDK (not OpenRouter)
COHERE_PREFIXES = ("cohere/", "command-")


def init_openrouter_agent(
    system_prompt: str = "",
    model_name: str = "gpt5-chat",
    temperature=0.0,
) -> Agent[None, JobReplacementPrediction]:
    """Initialize an OpenRouter agent.

    Args:
        system_prompt (str, optional): The system prompt for the LLM. Defaults to "".
        model_name (str, optional): Name of the model that is used. Defaults to "gpt5-chat".
        temperature (float, optional): Controls the randomness of the output. Defaults to 0.3.

    Returns:
        Agent[None, JobReplacementPrediction]: _description_
    """
    model = OpenAIChatModel(
        model_name=model_name,
        provider=OpenAIProvider(
            api_key=os.getenv(key="OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
        ),
        settings=OpenAIResponsesModelSettings(
            # openai_reasoning_effort="low",
            temperature=temperature,
            top_p=0,
            seed=121,
            max_tokens=4096,  # Limit tokens to avoid credit issues with expensive models
        ),
    )
    return Agent(
        model=model,
        system_prompt=system_prompt,
        output_type=JobReplacementPrediction,
        retries=10,
    )


def init_cohere_agent(
    system_prompt: str = "",
    temperature: float = 0.0,
    model_name: str = "command-r-plus",
) -> Agent[None, JobReplacementPrediction]:
    """Initialize a Cohere agent."""
    # Strip cohere/ prefix if present
    if model_name.startswith("cohere/"):
        model_name = model_name.replace("cohere/", "")

    model = CohereModel(
        model_name=model_name,
        provider=CohereProvider(api_key=os.getenv("COHERE_API_KEY")),
        settings=CohereModelSettings(temperature=temperature, p=0, seed=121),
    )
    return Agent(
        model=model,
        system_prompt=system_prompt,
        output_type=JobReplacementPrediction,
        retries=10,
    )


def init_agent(
    system_prompt: str = "",
    model_name: str = "openai/gpt-4o",
    temperature: float = 0.0,
) -> Agent[None, JobReplacementPrediction]:
    """Unified agent factory that routes to the appropriate provider.

    Args:
        system_prompt: The system prompt for the LLM.
        model_name: Name of the model. Use 'cohere/' prefix for Cohere models.
        temperature: Controls the randomness of the output.

    Returns:
        Agent configured for the specified model.
    """
    # Check if this is a Cohere model
    if model_name.startswith(COHERE_PREFIXES):
        return init_cohere_agent(
            system_prompt=system_prompt,
            model_name=model_name,
            temperature=temperature,
        )

    # Default to OpenRouter for all other models
    return init_openrouter_agent(
        system_prompt=system_prompt,
        model_name=model_name,
        temperature=temperature,
    )
