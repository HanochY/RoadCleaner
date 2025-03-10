from api.main.types.tunnel._generic import TunnelPublic, TunnelPrivate, TunnelFullInput, TunnelPartialInput


class JuniperTunnelPublic(TunnelPublic):
    associaton_name_core: str
    associaton_name_edge: str
    
class JuniperTunnelPrivate(TunnelPrivate):
    associaton_name_core: str
    associaton_name_edge: str
    
class JuniperTunnelFullInput(TunnelFullInput):
    associaton_name_core: str
    associaton_name_edge: str
    class Config(TunnelFullInput.Config):
        pass
class JuniperTunnelPartialInput(TunnelPartialInput):
    associaton_name_core: str
    associaton_name_edge: str
    class Config(TunnelPartialInput.Config):
        pass