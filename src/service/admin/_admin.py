from ._models import Fee
from src.repo.admin import AdminRepo, FeeType

from src.common import r


class AdminService:
    @staticmethod
    async def get_fees() -> list[Fee]:
        withdrawal_tron = r.get(FeeType.WITHDRAWAL_TRON)
        if withdrawal_tron:
            withdrawal_ton, swap, buy, sell = (
                r.get(FeeType.WITHDRAWAL_TON),
                r.get(FeeType.SWAP),
                r.get(FeeType.BUY),
                r.get(FeeType.SELL)
            )

            return [
                Fee(
                    type=t,
                    value=v
                )
                for t, v in zip(
                    (
                        FeeType.WITHDRAWAL_TRON,
                        FeeType.WITHDRAWAL_TON,
                        FeeType.SWAP,
                        FeeType.BUY,
                        FeeType.SELL
                    ),
                    (
                        withdrawal_tron, withdrawal_ton, swap, buy, sell
                    )
                )
            ]

        fees = await AdminRepo.get_fees()

        async with r.pipeline(transaction=True) as pipe:
            await (
                pipe.set(fees[0].type, fees[0].value)
                .set(fees[1].type, fees[1].value)
                .set(fees[2].type, fees[2].value)
                .set(fees[3].type, fees[3].value)
                .set(fees[4].type, fees[4].value)
                .execute()
            )

        return [
            Fee.model_validate(c, from_attributes=True)
            for c in fees
        ]

    @staticmethod
    async def get_fee(c: FeeType) -> float | None:
        res = await r.get(c)
        if res:
            return float(res)

        fee = await AdminRepo.get_fee(c)
        if not fee:
            return

        return fee.value

    @staticmethod
    async def set_fee(fee_type: FeeType, value: int) -> None:
        await r.set(fee_type, value)

        await AdminRepo.set_fee(fee_type, value)

    @staticmethod
    async def activate_user(user_id: int) -> None:
        await AdminRepo.activate_user(user_id)

    @staticmethod
    async def block_user(user_id: int) -> None:
        await AdminRepo.block_user(user_id)

    @staticmethod
    async def delete_user(user_id: int) -> None:
        await AdminRepo.delete_user(user_id)
