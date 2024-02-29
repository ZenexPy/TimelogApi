from fastapi import Path, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from ..core.db_init import db_init
from . import crud
from ..core.models.project import Project as Project_model


async def get_project_by_id(project_id: Annotated[int, Path], session: AsyncSession = Depends(db_init.session_dependency)) -> Project_model:
    project = await crud.get_project_one(session=session, project_id=project_id)
    if project is not None:
        return project
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
    )
