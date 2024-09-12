from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, extract

from .base import BaseCRUD
from app.models import CharityProject


class CharityProjectCRUD(BaseCRUD):
    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession
    ):
        projects = await session.execute(
            select(self.model).where(
                self.model.fully_invested.is_(True)).order_by(
                    (
                        extract('year', self.model.close_date) -
                        extract('year', self.model.create_date)
                    ),
                    (
                        extract('month', self.model.close_date) -
                        extract('month', self.model.create_date)
                    ),
                    (
                        extract('day', self.model.close_date) -
                        extract('day', self.model.create_date)
                    )))
        return projects.scalars().all()


charity_project_crud = CharityProjectCRUD(CharityProject)