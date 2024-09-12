from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"


async def spreadsheets_create(aiogoogle: Aiogoogle) -> str:
    date = datetime.now().strftime(FORMAT)
    sercice = await aiogoogle.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {
            'title': f'Отчёт на {date}',
            'locale': 'ru_RU'
        },
        'sheets': [{
            'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': 'Лист1',
                'gridProperties': {'rowCount': 100,
                                   'columnCount': 3}
            }
        }]
    }
    response = await aiogoogle.as_service_account(
        sercice.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
    spreadsheetId: str,
    aiogoogle: Aiogoogle
) -> None:
    permission_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email
    }
    service = await aiogoogle.discover('drive', 'v3')
    await aiogoogle.as_service_account(
        service.permissions.create(
            fileId=spreadsheetId,
            json=permission_body,
            fields='id'
        )
    )


async def spreadsheets_update_value(
        spreadsheetId: str,
        projects: list,
        aiogoogle: Aiogoogle
) -> None:
    now_date = datetime.now().strftime(FORMAT)
    service = await aiogoogle.discover('sheets', 'v4')
    table_body = [
        ['Отчёт от', now_date],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    for project in projects:
        new_row = [
            project.name,
            str(project.close_date - project.create_date),
            project.description]
        table_body.append(new_row)
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_body
    }
    await aiogoogle.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetId,
            range='A1:C100',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )