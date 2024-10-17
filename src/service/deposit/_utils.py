from pytoniq_core import Transaction


def filter_ton_deposit(tx: Transaction) -> bool:
    if tx.out_msgs:
        return False

    if tx.in_msg:
        return False

    return True
