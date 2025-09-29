from ai_organizational_changes.init_model import init_gemini_agent

import pandas as pd
import json
from loguru import logger

system_prompt = """Based on what you know, can you please read the following role and predict which roles are likely to be replaced by generative AI and which skills specifically for the role will be replaced by generative AI"""


def main() -> None:
    google_agent = init_gemini_agent(system_prompt=system_prompt)
    # openrouter_agent = init_openrouter_agent(system_prompt=system_prompt)
    # Use the agents for your tasks

    # now lets load the data in jobs.txt and every new line is a new job
    with open("jobs.txt") as f:
        jobs = f.readlines()

    # Collect all results
    all_results = []

    for job in jobs:
        job = job.strip()
        if not job:
            continue
        logger.info(f"Job: {job}")
        google_response = google_agent.run_sync(f"Job:\n{job}")
        logger.info(
            f"Google Agent Response: {google_response.output.model_dump_json(indent=2)}"
        )

        # openrouter_response = openrouter_agent.run(f"Provide a summary for the following job description:\n{job}")
        # print(f"OpenRouter Agent Response: {openrouter_response}")

        # Add job name to the response data
        response_data = google_response.output.model_dump()
        response_data["job"] = job
        all_results.append(response_data)

    # Save all results as a single JSON file
    with open("ai_organizational_changes_results.json", "w") as f:
        json.dump(all_results, f, indent=2)

    # Save all results as a single Excel file with each job as one row
    df = pd.json_normalize(all_results)
    df.to_excel("ai_organizational_changes_results.xlsx", index=False)

    logger.info(f"Processed {len(all_results)} jobs")


if __name__ == "__main__":
    main()
