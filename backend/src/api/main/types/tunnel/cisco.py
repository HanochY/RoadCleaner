from api.main.types.tunnel._generic import TunnelPublic, TunnelPrivate, TunnelFullInput, TunnelPartialInput


class CiscoTunnelPublic(TunnelPublic):
    keychain_inner: str | None = None
    keychain_outer: str | None = None
    
class CiscoTunnelPrivate(TunnelPrivate):
    keychain_inner: str | None = None
    keychain_outer: str | None = None
    
class CiscoTunnelFullInput(TunnelFullInput):
    class Config(TunnelFullInput.Config):
        pass
class CiscoTunnelPartialInput(TunnelPartialInput):
    class Config(TunnelPartialInput.Config):
        pass