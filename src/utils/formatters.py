from src.service.user import User


def format_commission(commission: float) -> str:
    m = f'Текущая комиссия: {commission}'

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
