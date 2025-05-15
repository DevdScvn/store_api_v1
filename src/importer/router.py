import codecs
import csv
from io import StringIO
from typing import Literal
from fastapi import APIRouter, UploadFile, HTTPException

from importer.utils import TABLE_MODEL_MAP, convert_csv_to_postgres_format
from fastapi.responses import StreamingResponse


router = APIRouter(
    prefix="/import",
    tags=["Импорт/Экспорт данных БД"],
)


@router.post(
    "/{table_name}",
    status_code=201,
    summary="Импорт csv файла в БД"
)
async def import_data_to_table(
        file: UploadFile,
        table_name: Literal["products", "orders"],
):
    """
    Принимает csv файл и записывает в базу данных
    """

    ModelDAO = TABLE_MODEL_MAP[table_name]
    # Внутри переменной file хранятся атрибуты:
    # file - сам файл, filename - название файла, size - размер файла.
    csvReader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'), delimiter=";")
    data = convert_csv_to_postgres_format(csvReader)
    file.file.close()
    if not data:
        raise "CannotProcessCSV"
    added_data = await ModelDAO.add_bulk(data)
    if not added_data:
        raise "CannotAddDataToDatabase"


@router.get("/{table_name}",
            summary="Экспорт данных их БД")
async def export_csv_orm(table_name: Literal["products", "orders"]):
    """
    Выгружает excel таблицу
    """
    ModelDAO = TABLE_MODEL_MAP[table_name]
    if not ModelDAO:
        raise HTTPException(status_code=404, detail="Table not found")

    try:
        # Получаем данные из базы
        data = await ModelDAO.get_excel_table()

        if not data:
            raise HTTPException(status_code=404, detail="No data found in table")

        # Создаем CSV в памяти
        stream = StringIO()

        # Определяем заголовки на основе первого элемента (если есть данные)
        fieldnames = list(data[0].keys()) if data else []

        writer = csv.DictWriter(stream, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(data)

        # Возвращаем файл как поток
        return StreamingResponse(
            iter([stream.getvalue()]),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename={table_name}_export.csv"
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error exporting data: {str(e)}"
        )
