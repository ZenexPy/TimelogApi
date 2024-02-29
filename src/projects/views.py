from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .schemas import ProjectGet, ProjectCreate, Project, ProjectUpdate, ProjectUpdatePartial
from ..core.db_init import db_init
from .dependencies import get_project_by_id


router = APIRouter(tags=["Projects"], prefix="/projects")


@router.get("/", response_model=list[ProjectGet])
async def get_projects(session: AsyncSession = Depends(db_init.session_dependency)):

    return await crud.get_project_all(session=session)


@router.post("/", response_model=ProjectGet, status_code=status.HTTP_201_CREATED)
async def create_project(
    create_model: ProjectCreate, 
    session: AsyncSession = Depends(db_init.session_dependency)
    ):

    return await crud.create_project(session=session, create_model=create_model)


@router.get("/{project_id}/", response_model=ProjectGet)
async def get_project(project=Depends(get_project_by_id)):

    return project


@router.put("/{project_id}/")
async def update_product(
    project_update: ProjectUpdate,
    project = Depends(get_project_by_id),
    session: AsyncSession = Depends(db_init.session_dependency)
    ):
    return await crud.update_project(
        session=session,
        project=project,
        project_update=project_update
    )


@router.patch("/{project_id}", response_model=ProjectGet)
async def update_product(
    project_update: ProjectUpdatePartial,
    project = Depends(get_project_by_id),
    session: AsyncSession = Depends(db_init.session_dependency)
    ):
    return await crud.update_project(
        session=session,
        project=project,
        project_update=project_update,
        partial=True
    )

@router.delete("/{project_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project = Depends(get_project_by_id), 
    session: AsyncSession = Depends(db_init.session_dependency)
    ):
    return await crud.delete_project(project=project, session=session)