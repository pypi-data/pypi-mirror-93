from dataclasses import dataclass
from typing import Any, Dict, Optional, Union

URL: str = "https://a.r.com/ach/relationships/53082140-7c28-624e-4130-573462cff1bd/"
UNLINK: str = "https://a.r.com/ach/relationships/53082140-7c28-624e-4130-573462cff1bd/unlink/"
EXAMPLE: Dict[str, Optional[Union[str, bool]]] = {
    "id": "53082140-7c28-624e-4130-573462cff1bd",
    "verification_method": "micro_deposits",
    "bank_account_number": "1374",
    "bank_account_nickname": "YoungOld Locality Debit Union",
    "verified": True,
    "state": "approved",
    "first_created_at": "2010-03-10T17:22:53.979434-05:00",
    "document_request": None,
    "url": URL,
    "withdrawal_limit": "1.63",
    "initial_deposit": "0.00",
    "account": "https://a.r.com/accounts/8ZX73609/",
    "unlink": UNLINK,
    "verify_micro_deposits": None,
    "unlinked_at": None,
    "created_at": "2010-03-10T17:22:53.979434-05:00",
    "bank_account_type": "checking",
    "bank_routing_number": "459201000",
    "bank_account_holder_name": "Doe Johnny",
}


@dataclass(frozen=True)
class BankAccount:
    id: str
    verification_method: str
    bank_account_holder_name: str
    bank_account_type: str
    bank_account_number: str
    bank_routing_number: str
    bank_account_nickname: str
    verified: bool
    state: str  # TODO: enum
    first_created_at: str  # TODO: datetime
    url: str
    withdrawal_limit: str
    initial_deposit: str
    account: str
    unlink: str
    created_at: str  # TODO: datetime
    document_request: Optional[Any] = None
    verify_micro_deposits: Optional[Any] = None
    unlinked_at: Optional[Any] = None


def main() -> None:
    print(BankAccount(**EXAMPLE))


if __name__ == "__main__":
    main()
