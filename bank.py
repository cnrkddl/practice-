import json
from datetime import datetime


class BankError(Exception):
    pass


class Account:
    def __init__(self, number, owner):
        self.number = number
        self.owner = owner
        self.balance = 0
        self.history = []

    def _record(self, kind, amount, memo):
        self.history.append({
            "at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "kind": kind,
            "amount": amount,
            "balance": self.balance,
            "memo": memo,
        })

    def deposit(self, amount, memo=""):
        if amount <= 0:
            raise BankError("금액은 0보다 커야 합니다")
        self.balance += amount
        self._record("입금", amount, memo)

    def withdraw(self, amount, memo=""):
        if amount <= 0:
            raise BankError("금액은 0보다 커야 합니다")
        if amount > self.balance:
            raise BankError(f"잔액 부족 (잔액 {self.balance:,}원)")
        self.balance -= amount
        self._record("출금", amount, memo)

    def print_history(self):
        print(f"[{self.number}] {self.owner} - 잔액 {self.balance:,}원")
        for h in self.history:
            print(f"  {h['at']}  {h['kind']}  {h['amount']:>8,}원  "
                  f"잔액 {h['balance']:>8,}원  {h['memo']}")


class Bank:
    def __init__(self):
        self.accounts = {}
        self.next_number = 1001

    def open_account(self, owner):
        acc = Account(str(self.next_number), owner)
        self.accounts[acc.number] = acc
        self.next_number += 1
        return acc

    def get(self, number):
        if number not in self.accounts:
            raise BankError(f"없는 계좌번호: {number}")
        return self.accounts[number]

    def transfer(self, src, dst, amount):
        if src == dst:
            raise BankError("같은 계좌로는 이체할 수 없습니다")
        sender = self.get(src)
        receiver = self.get(dst)
        sender.withdraw(amount, f"{receiver.owner}님에게 이체")
        receiver.deposit(amount, f"{sender.owner}님 이체")

    def save(self, path="bank.json"):
        data = {
            "next_number": self.next_number,
            "accounts": [
                {"number": a.number, "owner": a.owner,
                 "balance": a.balance, "history": a.history}
                for a in self.accounts.values()
            ],
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, path="bank.json"):
        bank = cls()
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            return bank
        bank.next_number = data["next_number"]
        for d in data["accounts"]:
            acc = Account(d["number"], d["owner"])
            acc.balance = d["balance"]
            acc.history = d["history"]
            bank.accounts[acc.number] = acc
        return bank


if __name__ == "__main__":
    bank = Bank.load()
    if not bank.accounts:
        a = bank.open_account("홍길동")
        bank.open_account("김철수")
        a.deposit(10000, "월급")

    bank.transfer("1001", "1002", 1000)

    for acc in bank.accounts.values():
        acc.print_history()
    bank.save()
