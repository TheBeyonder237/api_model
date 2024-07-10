import os
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from typing import List, Union


class Settings(BaseSettings):
    PROJECT_NAME: str = "Orizonne API"
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[Union[str, AnyHttpUrl]] = []
    SECRET_KEY: str = os.getenv("SECRET_KEY", "mysecretkey")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    API_KEY: str = os.getenv("NOTCHPAY_API_KEY","pk.cnnnT35K5qDVFZJtqcqc0Ic9UMTDr8TRtsrw91nbGca7rUUqoTLH4mWMsF72EruG37zoEa9mNvvqIceO2b1Cvwea0zgcPIFnLuhs5ftum5WKGNVDefKdgMixgOH38")
    NOTCHPAY_API_URL: str = os.getenv("NOTCHPAY_API_URL", "https://api.notchpay.co/payments")
    MEDIA_FOLDER: str = os.getenv("MEDIA_FOLDER", "./media")


settings = Settings()
