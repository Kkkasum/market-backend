from src.service.user import User


def format_fee(fee: float, extra: str) -> str:
    m = f'Текущая комиссия: <b>{fee}</b>{extra}'

    return m


def format_user(user: User) -> str:
    m = (
        f'TON: {user.ton_balance}\n'
        f'USDT: {user.usdt_balance}\n\n'
        f'Numbers:'
        f'{[
            f'{i}. {n.number}\n'
            for i, n in enumerate(user.numbers)
        ]}\n'
        f'Usernames:'
        f'{[
            f'{i}. {un.username}\n'
            for i, un in enumerate(user.usernames)
        ]}'
    )

    return m


def format_wallet(address: str) -> str:
    m = f'Адрес кошелька: <code>{address}</code>'

    return m


def format_stats(period: str, withdrawals: int, deposits: int, swaps: int) -> str:
    m = (
        f'Статистика за <b>{period}</b>\n\n'
        f'<b>Количество выводов</b>: {withdrawals}\n'
        f'<b>Количество вводов</b>: {deposits}\n'
        f'<b>Количество свапов</b>: {swaps}'
    )

    return m
