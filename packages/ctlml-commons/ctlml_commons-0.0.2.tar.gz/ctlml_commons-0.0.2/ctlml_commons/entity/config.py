from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    base_dir: str
    email: str
    users_key: str
    default_delimiter: str
    testing: bool
    debug: bool
    f_it_mode: bool
    profile_info: bool
    buy_one_sell_one_mode: bool
    window_secs: int
    random_investors: int
    error_sleep_time_sec: int
    output_dir: str
    log_dir: str
    tmp_dir: str
