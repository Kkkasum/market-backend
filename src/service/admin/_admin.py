from ._models import Commission
from src.repo.admin import AdminRepo, CommissionType

from src.common import r


class AdminService:
    @staticmethod
    async def get_commissions() -> list[Commission]:
        withdraw = r.get(CommissionType.WITHDRAWAL)
        if withdraw:
            swap, buy, sell = (
                r.get(CommissionType.SWAP),
                r.get(CommissionType.BUY),
                r.get(CommissionType.SELL)
            )

            return [
                Commission(
                    type=t,
                    value=v
                )
                for t, v in zip(
                    (
                        CommissionType.WITHDRAWAL,
                        CommissionType.SWAP,
                        CommissionType.BUY,
                        CommissionType.SELL
                    ),
                    (
                        withdraw, swap, buy, sell
                    )
                )
            ]

        commissions = await AdminRepo.get_commissions()

        async with r.pipeline(transaction=True) as pipe:
            await (
                pipe.set(commissions[0].type, commissions[0].value)
                .set(commissions[1].type, commissions[1].value)
                .set(commissions[2].type, commissions[2].value)
                .set(commissions[3].type, commissions[3].value)
                .set(commissions[4].type, commissions[4].value)
                .execute()
            )

        return [
            Commission.model_validate(c, from_attributes=True)
            for c in commissions
        ]

    @staticmethod
    async def get_commission(c: CommissionType) -> float:
        res = await r.get(c)
        if res:
            return float(res)

        return (await AdminRepo.get_commission(c)).value

    @staticmethod
    async def set_commission(commission_type: CommissionType, value: float) -> None:
        await r.set(commission_type, value)

        await AdminRepo.set_commission(commission_type, value)

    @staticmethod
    async def activate_user(user_id: int) -> None:
        await AdminRepo.activate_user(user_id)

    @staticmethod
    async def block_user(user_id: int) -> None:
        await AdminRepo.block_user(user_id)

    @staticmethod
    async def delete_user(user_id: int) -> None:
        await AdminRepo.delete_user(user_id)
