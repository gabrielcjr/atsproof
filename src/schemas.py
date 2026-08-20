"""
Pydantic data models and schemas for structured ATS verification outputs.
"""

from typing import List

from pydantic import BaseModel, Field


class TailoringSuggestion(BaseModel):
    """Represents a before-and-after work experience bullet point enhancement."""

    original_bullet: str = Field(
        description="An actual work experience or project achievement bullet point from the candidate's employment history (NEVER a skills list or category header)."
    )
    suggested_optimized_bullet: str = Field(
        description="A rewritten high-impact accomplishment bullet using strong action verbs, relevant tech stack context, and measurable outcomes (Google XYZ format: Accomplished [X], measured by [Y], by doing [Z])."
    )


class ATSMatchResult(BaseModel):
    """Complete ATS benchmark and match evaluation response."""

    match_score: int = Field(
        description="Overall match percentage from 0 to 100 based on required skills, tools, and experience level."
    )
    matched_keywords: List[str] = Field(
        description="List of matching skills, technologies, and certifications found in both resume and job description."
    )
    missing_critical_keywords: List[str] = Field(
        description="List of high-priority requirements or keywords from the job description missing from the resume."
    )
    experience_gap_feedback: str = Field(
        description="Analysis comparing the required years/seniority/domain vs candidate's demonstrated background."
    )
    tailoring_suggestions: List[TailoringSuggestion] = Field(
        description="List of 2 to 4 actionable work experience bullet point enhancements."
    )
    summary_verdict: str = Field(
        description="A 2-3 sentence strategic verdict on the candidate's interview odds and top action items."
    )
