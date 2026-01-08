from pydantic import BaseModel
from typing import Literal


class JobReplacementPrediction(BaseModel):
    """Model for job replacement prediction.

    Attributes:
        job_title (str): The title of the job.
        genai_impact (bool): Whether the job is likely to be automated by AI. Automation means that machines take over a human task. Whether the job is likely to be augmented with AI. Augmentation means that Humans collaborate closely with machines to perform a task. Whether the job is likely to remain human-only.
        skills (list[str]): List of skills that the genai takes over completely.
        explanation (str): Explanation for the prediction. Maximum 100 words.
    """

    job_title: str
    genai_impact: Literal[
        "likely_automated_by_ai", "likely_augmented_with_ai", "likely_human_only"
    ]
    skills: list[str]
    explanation: str
