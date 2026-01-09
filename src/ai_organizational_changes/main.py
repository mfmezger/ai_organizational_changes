from ai_organizational_changes.init_model import init_agent

import pandas as pd
import json
import asyncio
from datetime import datetime
from loguru import logger
from tqdm import tqdm
from pathlib import Path
import os
import logfire

# configure logfire
logfire.configure(token=os.getenv(key="LOGFIRE_TOKEN"))
logfire.instrument_pydantic_ai()


# List of models to process
MODELS: list[str] = [
    "openai/gpt-5",
    "anthropic/claude-4.5-sonnet",
    "google/gemini-3-flash-preview",
    "x-ai/grok-4",
    "command-a-reasoning-08-2025",
]


system_prompt = """Based on what you know, can you please read the following role and predict which roles are likely to be impacted by generative AI and which skills specifically for the role will be impacted by generative AI"""


async def process_job(
    agent, job: str, semaphore: asyncio.Semaphore, max_retries: int = 5
) -> dict | None:
    """Process a single job with retry logic for rate limits."""
    job = job.strip()
    if not job:
        return None

    async with semaphore:
        retry_delay = 10  # Start with 10 seconds
        for attempt in range(max_retries):
            try:
                response = await agent.run(f"Job:\n{job}")

                # Add job name to the response data
                response_data = response.output.model_dump()
                response_data["job"] = job
                return response_data

            except Exception as e:
                error_str = str(e)
                # Check for rate limit error (429)
                if "429" in error_str or "rate" in error_str.lower():
                    if attempt < max_retries - 1:
                        logger.warning(
                            f"Rate limit hit for '{job}', retrying in {retry_delay}s (attempt {attempt + 1}/{max_retries})"
                        )
                        await asyncio.sleep(retry_delay)
                        retry_delay *= 2  # Exponential backoff
                        continue
                # Re-raise if not a rate limit error or max retries reached
                raise


async def process_model(model_name: str, jobs: list[str]) -> None:
    """Process all jobs for a single model."""
    logger.info(f"Processing model: {model_name}")

    agent = init_agent(
        system_prompt=system_prompt,
        model_name=model_name,
        temperature=0,
    )

    # Use lower concurrency for Cohere due to stricter rate limits
    is_cohere = model_name.startswith(("cohere/", "command-"))
    max_concurrent = 2 if is_cohere else 10

    logger.info(
        f"Starting to process {len(jobs)} jobs (max {max_concurrent} concurrent) for {model_name}"
    )

    # Create a semaphore to limit concurrent processing
    semaphore = asyncio.Semaphore(max_concurrent)

    # Process all jobs concurrently using asyncio.gather with progress bar
    try:
        tasks = [process_job(agent=agent, job=job, semaphore=semaphore) for job in jobs]

        # Use tqdm to wrap asyncio.gather for progress tracking
        results = []
        with tqdm(total=len(jobs), desc=f"Processing jobs ({model_name})") as pbar:
            # Process tasks in chunks or use a custom approach with tqdm
            results = await asyncio.gather(*tasks, return_exceptions=True)
            pbar.update(len(jobs))  # Update progress bar when all tasks complete

        # Filter out None results and exceptions
        all_results = []
        failed_jobs = []

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Failed to process job '{jobs[i]}': {result}")
                failed_jobs.append(jobs[i])
            elif result is not None:
                all_results.append(result)

        if failed_jobs:
            logger.warning(f"Failed to process {len(failed_jobs)} jobs: {failed_jobs}")

        logger.info(
            f"Successfully processed {len(all_results)} out of {len(jobs)} jobs for {model_name}"
        )

        if all_results:
            # Generate timestamp for filenames
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            # save the results in a folder named results
            Path("results").mkdir(exist_ok=True)

            # Save all results as a single JSON file with timestamp
            json_filename = f"results/{model_name.replace('/', '_')}_{timestamp}.json"
            with Path(json_filename).open(mode="w") as f:
                json.dump(obj=all_results, fp=f, indent=2)

            # Save all results as a single Excel file with each job as one row
            excel_filename = f"results/{model_name.replace('/', '_')}_{timestamp}.xlsx"
            df = pd.json_normalize(data=all_results)
            df.to_excel(excel_writer=excel_filename, index=False)

            logger.info(f"Results saved to {json_filename} and {excel_filename}")
        else:
            logger.error(f"No successful results to save for {model_name}")

    except Exception as e:
        logger.error(f"Critical error processing model {model_name}: {e}")
        raise


async def main() -> None:
    # Load the data from jobs.txt and every new line is a new job
    with Path("jobs.txt").open() as f:
        jobs = f.readlines()

    # Filter out empty jobs
    jobs = [job.strip() for job in jobs if job.strip()]

    logger.info(f"Loaded {len(jobs)} jobs to process")
    logger.info(f"Will process {len(MODELS)} models: {MODELS}")

    # Process each model sequentially
    for model_name in MODELS:
        try:
            await process_model(model_name=model_name, jobs=jobs)
        except Exception as e:
            logger.error(f"Failed to process model {model_name}: {e}")
            # Continue with next model even if one fails
            continue

    logger.info("Finished processing all models")


if __name__ == "__main__":
    asyncio.run(main=main())
