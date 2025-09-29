from pydantic import BaseModel


class JobReplacementPrediction(BaseModel):
    """Model for job replacement prediction.

    Attributes:
        job_title (str): The title of the job.
        likely_replaced_by_ai (bool): Whether the job is likely to be replaced by AI.
        skills_replaced (list[str]): List of skills that will be replaced by AI.
        explanation (str): Explanation for the prediction. Maximum 100 words.
    """

    job_title: str
    likely_replaced_by_ai: bool
    skills_replaced: list[str]
    explanation: str
