from dataclasses import dataclass
from typing import Any, Optional


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
