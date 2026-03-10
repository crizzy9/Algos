# https://github.com/EricZheng0404/LibreSignal/blob/main/Questions/bank_system/simulation_solution.py#L117
class Account:
    def __init__(self, timestamp: int, account_id: str) -> None:
        self.account_id: str = account_id
        self.history: list[dict[str, str|int]] = [{
            "event": "CREATE",
            "timestamp": timestamp
        }]
        self.balance: int = 0
        self.payments: dict[str, str] = {}
    
    def get_balance(self, timestamp: int):
        cashback = 2
        day_timestamp = 24*60*60*1000 
        final_balance = self.balance
        for e in self.history:
            if e["event"] == "CASHBACK" and int(e["timestamp"]) + day_timestamp >= timestamp:
                final_balance += round((int(e["amount"]) + cashback)*100)

        return final_balance

class Simulation:

    def __init__(self):
        self.accounts: dict[str, Account] = {}

    def create_account(self, timestamp: int, account_id: str) -> bool | None:
        if not self.accounts.get(account_id):
            self.accounts[account_id] = Account(timestamp, account_id)
            return True

        return False

    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        account = self.accounts.get(account_id)
        if account is not None:
            account.balance += amount
            account.history.append({
                "event": "DEPOSIT",
                "timestamp": timestamp,
                "amount": amount
            })
            return account.balance
        return None


    def transfer(self, timestamp: int, source_account_id: str, target_account_id: str, amount: int) -> int | None:
        source_account =  self.accounts.get(source_account_id)
        target_account =  self.accounts.get(target_account_id)
        if source_account_id != target_account_id and source_account is not None and target_account is not None and source_account.balance >= amount:
            source_account.balance -= amount
            _ = self.deposit(timestamp, target_account_id, amount)
            # target_account.balance += amount
            source_account.history.append({
                "event": "TRANSFER",
                "timestamp": timestamp,
                "target": target_account_id,
                "amount": amount
            })
            return source_account.balance
        return None

    def top_spenders(self, timestamp: int, n: int) -> list[str] | None:
        outgoing: list[tuple[str, int]] = []
        for id, account in self.accounts.items():
            out = 0
            for a in account.history:
                if a["event"] == "TRANSFER":
                    out += int(a["amount"])

            outgoing.append((id, out))

        spenders = [f"{id}({t})" for id, t in sorted(outgoing, key=lambda item: (-item[1], item[0]))]
        return spenders[:n]


    def pay(self, timestamp: int, account_id: str, amount: int) -> str | None:
        cashback = 2
        account = self.accounts.get(account_id)
        if account is not None and account.balance >= amount:
            account.history.append({
                "event": "CASHBACK",
                "timestamp": timestamp,
                "amount": amount
            })
            pass
        return None

    def get_payment_status(self, timestamp: int, account_id: str, payment: str) -> str | None:
        account = self.accounts.get(account_id)
        if account is not None and account.get_balance(timestamp)
        pass

    def merge_accounts(self, timestamp: int, account_id_1: str, account_id_2: str) -> bool | None:
        pass

    def get_balance(self, timestamp: int, account_id: str, time_at: int) -> int | None:
        pass
