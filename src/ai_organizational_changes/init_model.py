"""Utils for initialization of Gemini."""

from dotenv import load_dotenv
from pydantic_ai import Agent
import os
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from pydantic_ai.models.cohere import CohereModel, CohereModelSettings
from pydantic_ai.providers.cohere import CohereProvider
from pydantic_ai.models.google import GoogleModelSettings
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from ai_organizational_changes.model import JobReplacementPrediction
from pydantic_ai.models.openai import OpenAIResponsesModelSettings

load_dotenv(override=True)


def init_openrouter_agent(
    system_prompt: str = "",
    model_name: str = "gpt5-chat",
    temperature=0.3,
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
            temperature=temperature
        ),
    )
    return Agent(
        model=model,
        system_prompt=system_prompt,
        output_type=JobReplacementPrediction,
        retries=10,
    )


def init_gemini_agent(
    system_prompt: str = "",
    thinking_budget: int = 200,
    temperature: float = 0.3,  # 0..7
    model_name: str = "gemini-2.5-flash",
) -> Agent[None, JobReplacementPrediction]:
    provider = GoogleProvider(api_key=os.getenv(key="GEMINI_API_KEY"))  # pyright: ignore[reportArgumentType]

    settings = GoogleModelSettings(
        temperature=temperature,
        google_thinking_config={"thinking_budget": thinking_budget},
    )
    model = GoogleModel(model_name=model_name, provider=provider, settings=settings)
    agent = Agent(
        model=model, system_prompt=system_prompt, output_type=JobReplacementPrediction
    )

    return agent


def init_cohere_agent(
    system_prompt: str = "",
    thinking_budget: int = 200,
    temperature: float = 0.3,  # 0..7
    model_name: str = "gemini-2.5-flash",
) -> Agent[None, JobReplacementPrediction]:
    """Initialize a Cohere agent."""

    model = CohereModel(
        model_name=model_name,
        provider=CohereProvider(api_key=os.getenv("COHERE_API_KEY")),
        settings=CohereModelSettings(temperature=temperature),
    )
    agent = Agent(
        model=model, system_prompt=system_prompt, output_type=JobReplacementPrediction
    )  # Add other parameters as needed
    return agent
