from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import ProjectCreate, Project, ProjectUpdate, ProjectUpdatePartial, ProjectGet

from ..core.models.project import Project as Project_model


async def create_project(session: AsyncSession, create_model: ProjectCreate) -> Project_model:
    project = Project_model(**create_model.model_dump())
    session.add(project)
    await session.commit()

    return project


async def get_project_one(project_id: int , session: AsyncSession) -> Project_model | None:
    return await session.get(Project_model, project_id)


async def get_project_all(session: AsyncSession) -> list[Project_model]:
    stmt = select(Project_model).order_by(Project_model.id)
    result: Result = await session.execute(stmt)
    projects = result.scalars().all()
    return list(projects)


async def delete_project(project: Project, session: AsyncSession) -> None:
    await session.delete(project)
    await session.commit()


async def update_project(session: AsyncSession, project: ProjectGet, project_update: ProjectUpdate | ProjectUpdatePartial, partial: bool = False) -> Project_model:
    for name, value in project_update.model_dump(exclude_unset=partial).items():
        setattr(project, name, value)
    await session.commit()
    return project