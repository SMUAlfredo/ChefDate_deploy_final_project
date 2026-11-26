from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class AddOn:
    name: str
    price_cad: Decimal


ADD_ONS = {
    'cleaning': AddOn('Cleaning', Decimal('50.00')),
    'waitstaff': AddOn('Waitstaff', Decimal('80.00')),
}
