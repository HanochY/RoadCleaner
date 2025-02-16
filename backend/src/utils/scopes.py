from fastapi.security import SecurityScopes

async def authorize_scopes(security_scopes: SecurityScopes, scopes: list[str]):
    for scope in security_scopes.scopes:
        if scope not in scopes:
            return False
    return True

async def generate_authenticate_value(security_scopes: SecurityScopes):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    return authenticate_value
