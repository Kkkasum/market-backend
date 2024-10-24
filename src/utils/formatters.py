from src.service.user import User


def format_fee(fee: float, extra: str) -> str:
    m = f'Текущая комиссия: <b>{fee}</b>{extra}'

    return m


def format_user(user: User) -> str:
    m = (
        f'Баланс\n'
        f'TON: {user.ton_balance}\n'
        f'USDT: {user.usdt_balance}\n\n'
        f'Номера:'
        f'{[
            f'{i}. {n.number}\n'
            for i, n in enumerate(user.numbers)
        ]}\n'
        f'Юзернеймы:'
        f'{[
            f'{i}. {un.username}\n'
            for i, un in enumerate(user.usernames)
        ]}'
    )

    return m


def format_wallet(address: str) -> str:
    m = f'Адрес кошелька: {address}'

    return m


def format_stats(period: str, withdrawals: int, deposits: int, swaps: int) -> str:
    m = (
        f'Статистика за {period}\n\n'
        f'Количество выводов: {withdrawals}\n'
        f'Количество вводов: {deposits}\n'
        f'Количество свапов: {swaps}'
    )

    return m
