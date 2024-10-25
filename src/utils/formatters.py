from src.service.user import User


def format_const(const: float, extra: str) -> str:
    m = f'Текущая значение: <b>{const}</b>{extra}'

    return m


def format_number(number: str) -> str:
    m = f'+{number[0:3]} {number[3:7]} {number[7:11]}'

    return m


def format_user(user_id: int, user: User) -> str:
    m = (
        f'<b>User ID</b>: {user_id}\n'
        f'<b>TON</b>: {user.ton_balance}\n'
        f'<b>USDT</b>: {user.usdt_balance}\n\n'
        f'<b>Numbers</b>:\n'
        f'{'\n'.join([
            f'{i + 1}. {format_number(n.number)}'
            for i, n in enumerate(user.numbers)
        ])}\n\n'
        f'<b>Usernames</b>:\n'
        f'{'\n'.join([
            f'{i + 1}. @{un.username}'
            for i, un in enumerate(user.usernames)
        ])}'
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
