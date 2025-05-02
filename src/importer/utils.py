import datetime
import json
import logging
from typing import Iterable

from products.product_dao import ProductDAO

TABLE_MODEL_MAP = {
    "products": ProductDAO,
    # "rooms": RoomDAO,
    # "bookings": BookingDAO,
}

log = logging.getLogger(__name__)


def convert_csv_to_postgres_format(csv_iterable: Iterable):
    try:
        data = []
        for row in csv_iterable:
            for k, v in row.items():
                if v.isdigit():
                    row[k] = int(v)
                elif k == "services":
                    row[k] = json.loads(v.replace("'", '"'))
                elif "date" in k:
                    row[k] = datetime.strptime(v, "%Y-%m-%d")
            data.append(row)
        return data
    except Exception:
        log.error("Cannot convert CSV into DB format", exc_info=True)
