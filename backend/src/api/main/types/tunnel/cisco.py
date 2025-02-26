from api.main.types.tunnel._generic import TunnelPublic, TunnelPrivate, TunnelFullInput, TunnelPartialInput


class CiscoTunnelPublic(TunnelPublic):
    keychain_core: str
    keychain_edge: str
    key_name_core: str
    key_name_edge: str
    
class CiscoTunnelPrivate(TunnelPrivate):
    keychain_core: str
    keychain_edge: str
    key_name_core: str
    key_name_edge: str
    
class CiscoTunnelFullInput(TunnelFullInput):
    keychain_core: str
    keychain_edge: str
    key_name_core: str
    key_name_edge: str
    
class CiscoTunnelPartialInput(TunnelPartialInput):
    keychain_core: str
    keychain_edge: str
    key_name_core: str
    key_name_edge: str