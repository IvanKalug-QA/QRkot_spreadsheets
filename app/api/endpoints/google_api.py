from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser

from app.crud.charityproject import charity_project_crud
from app.services.google_api import (
    set_user_permissions,
    spreadsheets_update_value,
    spreadsheets_create
)


router = APIRouter()


@router.post(
    '/',
    response_model=str,
    dependencies=[Depends(current_superuser)]
)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    aiogoogle: Aiogoogle = Depends(get_service)
):
    projects = await charity_project_crud.get_projects_by_completion_rate(
        session
    )
    spreadsheets_id = await spreadsheets_create(aiogoogle)
    await spreadsheets_update_value(spreadsheets_id, projects, aiogoogle)
    await set_user_permissions(spreadsheets_id, aiogoogle)
    return 'OK'