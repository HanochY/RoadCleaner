from api.main.types.tunnel._generic import TunnelPublic, TunnelPrivate, TunnelFullInput, TunnelPartialInput


class JuniperTunnelPublic(TunnelPublic):
    associaton_name_inner: str | None = None
    associaton_name_outer: str | None = None
    
class JuniperTunnelPrivate(TunnelPrivate):
    associaton_name_inner: str | None = None
    associaton_name_outer: str | None = None
    
class JuniperTunnelFullInput(TunnelFullInput):
    class Config(TunnelFullInput.Config):
        pass
class JuniperTunnelPartialInput(TunnelPartialInput):
    class Config(TunnelPartialInput.Config):
        pass