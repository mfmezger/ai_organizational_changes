from ai_organizational_changes.init_model import init_gemini_agent

import pandas as pd
import json
import asyncio
from datetime import datetime
from loguru import logger
from tenacity import retry, wait_exponential, retry_if_exception_type
from tqdm import tqdm

system_prompt = """Based on what you know, can you please read the following role and predict which roles are likely to be replaced by generative AI and which skills specifically for the role will be replaced by generative AI"""


@retry(
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type((Exception,)),
    reraise=True,
)
async def process_job(
    google_agent, job: str, semaphore: asyncio.Semaphore
) -> dict | None:
    """Process a single job with retry logic."""
    job = job.strip()
    if not job:
        return None

    async with semaphore:
        try:
            # Convert run_sync to async call - assuming the agent has an async method
            # If not, we'll need to run it in a thread executor
            try:
                google_response = await google_agent.run(f"Job:\n{job}")
            except AttributeError:
                # Fallback to sync method in thread executor if async method doesn't exist
                loop = asyncio.get_event_loop()
                google_response = await loop.run_in_executor(
                    None, google_agent.run_sync, f"Job:\n{job}"
                )

            # Add job name to the response data
            response_data = google_response.output.model_dump()
            response_data["job"] = job
            return response_data

        except Exception:
            raise


async def main() -> None:
    google_agent = init_gemini_agent(system_prompt=system_prompt)
    # openrouter_agent = init_openrouter_agent(system_prompt=system_prompt)
    # Use the agents for your tasks

    # Load the data from jobs.txt and every new line is a new job
    with open("jobs.txt") as f:
        jobs = f.readlines()

    # Filter out empty jobs
    jobs = [job.strip() for job in jobs if job.strip()]

    logger.info(
        f"Starting to process {len(jobs)} jobs concurrently (max 10 concurrent)"
    )

    # Create a semaphore to limit concurrent processing to 10 jobs
    semaphore = asyncio.Semaphore(10)

    # Process all jobs concurrently using asyncio.gather with progress bar
    try:
        tasks = [process_job(google_agent, job, semaphore) for job in jobs]

        # Use tqdm to wrap asyncio.gather for progress tracking
        results = []
        with tqdm(total=len(jobs), desc="Processing jobs") as pbar:
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
            f"Successfully processed {len(all_results)} out of {len(jobs)} jobs"
        )

        if all_results:
            # Generate timestamp for filenames
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            # Save all results as a single JSON file with timestamp
            json_filename = f"ai_organizational_changes_results_{timestamp}.json"
            with open(json_filename, "w") as f:
                json.dump(all_results, f, indent=2)

            # Save all results as a single Excel file with each job as one row
            excel_filename = f"ai_organizational_changes_results_{timestamp}.xlsx"
            df = pd.json_normalize(all_results)
            df.to_excel(excel_filename, index=False)

            logger.info(f"Results saved to {json_filename} and {excel_filename}")
        else:
            logger.error("No successful results to save")

    except Exception as e:
        logger.error(f"Critical error in main processing: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
