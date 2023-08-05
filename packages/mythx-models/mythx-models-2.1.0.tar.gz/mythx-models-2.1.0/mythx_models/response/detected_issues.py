"""This module contains the response models for the detected issues endpoint
and a report helper."""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from mythx_models.response.issue import Issue, SourceFormat, SourceType


class IssueReport(BaseModel):
    issues: List[Issue]
    source_type: Optional[SourceType] = Field(alias="sourceType")
    source_format: Optional[SourceFormat] = Field(alias="sourceFormat")
    source_list: Optional[List[str]] = Field(alias="sourceList")
    meta_data: Dict[str, Any] = Field(alias="meta")


class DetectedIssuesResponse(BaseModel):
    issue_reports: List[IssueReport]
