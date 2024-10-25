from ._models import GetConst
from src.common import r
from src.repo.admin import AdminRepo, Const


class AdminService:
    @staticmethod
    async def get_constants() -> list[GetConst]:
        withdrawal_tron = r.get(Const.FEE_WITHDRAWAL_TRON)
        if withdrawal_tron:
            instant_sell_perc, max_instant_sell, withdrawal_ton, swap, buy, sell = (
                r.get(Const.INSTANT_SELL_PERC),
                r.get(Const.MAX_INSTANT_SELL),
                r.get(Const.FEE_WITHDRAWAL_TON),
                r.get(Const.FEE_SWAP),
                r.get(Const.FEE_BUY),
                r.get(Const.FEE_SELL)
            )

            return [
                GetConst(
                    const=t,
                    value=v
                )
                for t, v in zip(
                    (
                        Const.INSTANT_SELL_PERC,
                        Const.MAX_INSTANT_SELL,
                        Const.FEE_WITHDRAWAL_TRON,
                        Const.FEE_WITHDRAWAL_TON,
                        Const.FEE_SWAP,
                        Const.FEE_BUY,
                        Const.FEE_SELL,
                    ),
                    (
                        instant_sell_perc, max_instant_sell, withdrawal_ton, swap, buy, sell
                    )
                )
            ]

        constants = await AdminRepo.get_constants()

        async with r.pipeline(transaction=True) as pipe:
            await (
                pipe
                .set(constants[0].const, constants[0].value)
                .set(constants[1].const, constants[1].value)
                .set(constants[2].const, constants[2].value)
                .set(constants[3].const, constants[3].value)
                .set(constants[4].const, constants[4].value)
                .set(constants[5].const, constants[5].value)
                .set(constants[6].const, constants[6].value)
                .execute()
            )

        return [
            GetConst.model_validate(c, from_attributes=True)
            for c in constants
        ]

    @staticmethod
    async def get_constant(c: Const) -> float | None:
        res = await r.get(c)
        if res:
            return float(res)

        constant = await AdminRepo.get_constant(c)
        if not constant:
            return

        return constant.value

    @staticmethod
    async def set_constant(const: Const, value: int | float) -> None:
        await r.set(const, value)

        await AdminRepo.set_constant(const, value)

    @staticmethod
    async def activate_user(user_id: int) -> None:
        await AdminRepo.activate_user(user_id)

    @staticmethod
    async def block_user(user_id: int) -> None:
        await AdminRepo.block_user(user_id)

    @staticmethod
    async def delete_user(user_id: int) -> None:
        await AdminRepo.delete_user(user_id)
