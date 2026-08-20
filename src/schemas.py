"""
Pydantic data models and schemas for structured ATS verification outputs.
"""

from typing import List, Set

from pydantic import BaseModel, Field, model_validator


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

    @model_validator(mode="after")
    def sanitize_and_deduplicate_keywords(self) -> "ATSMatchResult":
        """
        Enforces strict mutual exclusivity and case-insensitive deduplication between
        matched_keywords and missing_critical_keywords.
        """
        # 1. Deduplicate matched_keywords preserving original casing and order
        seen_matched: Set[str] = set()
        clean_matched: List[str] = []
        for kw in self.matched_keywords or []:
            trimmed = kw.strip() if isinstance(kw, str) else str(kw).strip()
            if trimmed and trimmed.lower() not in seen_matched:
                seen_matched.add(trimmed.lower())
                clean_matched.append(trimmed)
        self.matched_keywords = clean_matched

        # 2. Deduplicate missing_critical_keywords and remove any present in matched_keywords
        seen_missing: Set[str] = set()
        clean_missing: List[str] = []
        for kw in self.missing_critical_keywords or []:
            trimmed = kw.strip() if isinstance(kw, str) else str(kw).strip()
            if (
                trimmed
                and trimmed.lower() not in seen_matched
                and trimmed.lower() not in seen_missing
            ):
                seen_missing.add(trimmed.lower())
                clean_missing.append(trimmed)
        self.missing_critical_keywords = clean_missing

        # 3. Ensure match_score is clamped between 0 and 100
        self.match_score = max(0, min(100, int(self.match_score)))

        return self
