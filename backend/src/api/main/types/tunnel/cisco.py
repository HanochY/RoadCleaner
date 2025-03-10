from api.main.types.tunnel._generic import TunnelPublic, TunnelPrivate, TunnelFullInput, TunnelPartialInput


class CiscoTunnelPublic(TunnelPublic):
    keychain_core: str
    keychain_edge: str
    
class CiscoTunnelPrivate(TunnelPrivate):
    keychain_core: str
    keychain_edge: str
    
class CiscoTunnelFullInput(TunnelFullInput):
    keychain_core: str
    keychain_edge: str
    class Config(TunnelFullInput.Config):
        pass
class CiscoTunnelPartialInput(TunnelPartialInput):
    keychain_core: str
    keychain_edge: str
    class Config(TunnelPartialInput.Config):
        pass