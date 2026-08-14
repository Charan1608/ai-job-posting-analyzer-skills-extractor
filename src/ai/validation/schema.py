"""
=========================================================
PYDANTIC SCHEMA
AI-Powered Job Posting Analyzer
=========================================================
"""

from typing import List, Optional, Any

from pydantic import BaseModel, Field, field_validator


class SkillExtraction(BaseModel):

    technical_skills: List[str] = Field(default_factory=list)

    soft_skills: List[str] = Field(default_factory=list)

    tools: List[str] = Field(default_factory=list)

    certifications: List[str] = Field(default_factory=list)

    experience: Optional[str] = None

    education: Optional[str] = None

    @field_validator("experience", "education", mode="before")
    @classmethod
    def convert_list_to_string(cls, value: Any):

        if value is None:
            return None

        if isinstance(value, list):
            return ", ".join(str(v) for v in value)

        return str(value)