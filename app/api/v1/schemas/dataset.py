from typing import Optional, List, Any, Dict
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class ColumnMetaSchema(BaseModel):
    name: str
    data_type: str
    null_count: int
    null_percentage: float
    unique_count: int
    sample_values: Optional[List[Any]] = None


class QualityReportSchema(BaseModel):
    overall_score: float
    completeness: float
    uniqueness: float
    validity: float
    total_anomalies: int
    missing_cells: int
    duplicate_rows: int
    columns: List[ColumnMetaSchema] = []
    recommendations: Optional[List[str]] = None


class CleaningRuleSchema(BaseModel):
    column: str
    action: str
    parameters: Optional[Dict[str, Any]] = None


class DatasetCreate(BaseModel):
    name: str
    description: Optional[str] = None


class DatasetResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    file_format: str
    file_size_bytes: int
    row_count: int
    col_count: int
    status: str
    quality_score: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    quality_report: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)


class DatasetListResponse(BaseModel):
    items: List[DatasetResponse]
    total: int
    page: int
    limit: int
