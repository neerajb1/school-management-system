from app.extensions import db
from app.models.finance import FeeType


def create_fee_type_service(admin_user_id: int, data: dict) -> FeeType:
    name = data.get("name")
    frequency = data.get("frequency")  # MONTHLY / QUARTERLY / YEARLY

    if not name:
        raise ValueError("name is required")

    if not frequency:
        raise ValueError("frequency is required")

    fee_type = FeeType(
        name=name.strip(),
        frequency=frequency,
        created_by_id=admin_user_id,
        updated_by_id=admin_user_id,
    )

    db.session.add(fee_type)
    return fee_type
