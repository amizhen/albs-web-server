import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from alws.crud.products import create_product
from alws.models import Product
from alws.schemas.product_schema import ProductCreate

from tests.constants import ADMIN_USER_ID


@pytest.fixture(
    params=[
        ADMIN_USER_ID,
    ]
)
def product_create_payload(request) -> dict:
    return {
        "name": "AlmaLinux",
        "owner_id": request.param,
        "title": "AlmaLinux",
        "description": "",
        "platforms": [
            {
                "id": 1,
                "name": "AlmaLinux-8",
                "distr_type": "rhel",
                "distr_version": "8",
                "arch_list": [
                    "i686",
                    "x86_64",
                    "ppc64le",
                    "aarch64",
                    "s390x",
                ],
                "modularity": {},
            },
        ],
        "is_community": True,
    }


@pytest.mark.anyio
@pytest.fixture
async def create_base_product(session: AsyncSession, product_create_payload: dict):
    product = (
        (
            await session.execute(
                select(Product).where(
                    Product.name == product_create_payload["name"],
                ),
            )
        )
        .scalars()
        .first()
    )
    if not product:
        await create_product(
            session,
            ProductCreate(**product_create_payload),
        )