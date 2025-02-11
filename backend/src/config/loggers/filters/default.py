import logging
import re

SENSITIVE_KEYS = (
        "credentials",
        "authorization",
        "token",
        "password",
        "access_token",
        "Bearer"
    )
GENERIC_TOKEN_PATTERN = rf"token=([^;]+)"
BEARER_TOKEN_PATTERN = rf"Bearer\s+([a-zA-Z0-9\-._~+/]+=*)"
    
class SensitiveDataFilter(logging.Filter):
    def filter(self, record):
        try:
            for sensitive_key in SENSITIVE_KEYS:
                for key, value in record.msg.items():
                    if isinstance(value, dict):
                        for ikey in value.keys():
                            if sensitive_key in ikey.lower():
                                record.msg[key][ikey] = "******"
                    else:
                        if sensitive_key in key.lower():
                            record.msg[key] = "******"
            return True
        except Exception as e:
            return True
