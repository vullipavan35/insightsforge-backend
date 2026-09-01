from typing import List, Optional
import os
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.database.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.dataset import Dataset
from app.api.v1.schemas.dataset import DatasetResponse, DatasetListResponse, QualityReportSchema
from app.config import settings

router = APIRouter(prefix="/datasets", tags=["Datasets"])


@router.get("", response_model=DatasetListResponse, summary="List user datasets")
def list_datasets(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieves a paginated list of datasets belonging to the current user."""
    offset = (page - 1) * limit

    # Count total
    count_stmt = select(func.count(Dataset.id)).where(Dataset.user_id == current_user.id)
    total = db.scalar(count_stmt) or 0

    # Query items
    stmt = (
        select(Dataset)
        .where(Dataset.user_id == current_user.id)
        .order_by(Dataset.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    items = db.scalars(stmt).all()

    return DatasetListResponse(
        items=[DatasetResponse.model_validate(item) for item in items],
        total=total,
        page=page,
        limit=limit,
    )


@router.post("/upload", response_model=DatasetResponse, status_code=status.HTTP_201_CREATED, summary="Upload a new dataset")
async def upload_dataset(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Accepts CSV, XLSX, or JSON file uploads and registers a dataset record."""
    filename = file.filename or "dataset.csv"
    ext = filename.split(".")[-1].lower() if "." in filename else "csv"
    if ext not in ["csv", "xlsx", "json", "parquet"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file format. Supported formats: CSV, XLSX, JSON, Parquet.",
        )

    # Save to upload dir
    os.makedirs(settings.FILE_UPLOAD_DIR, exist_ok=True)
    target_path = os.path.join(settings.FILE_UPLOAD_DIR, f"{current_user.id}_{filename}")

    content = await file.read()
    file_size = len(content)

    with open(target_path, "wb") as f:
        f.write(content)

    new_dataset = Dataset(
        user_id=current_user.id,
        name=filename,
        description=description,
        file_path=target_path,
        file_format=ext,
        file_size_bytes=file_size,
        row_count=0,
        col_count=0,
        status="READY",
        quality_score=95.0,
    )
    db.add(new_dataset)
    db.commit()
    db.refresh(new_dataset)

    return DatasetResponse.model_validate(new_dataset)


@router.get("/{dataset_id}", response_model=DatasetResponse, summary="Get dataset details")
def get_dataset(
    dataset_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieves metadata and processing status for a specific dataset."""
    stmt = select(Dataset).where(Dataset.id == dataset_id, Dataset.user_id == current_user.id)
    dataset = db.scalars(stmt).first()
    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found or access denied.",
        )
    return DatasetResponse.model_validate(dataset)
