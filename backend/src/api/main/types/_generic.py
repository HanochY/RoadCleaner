class GenericOutput:
    pass

class GenericInput:
    class Config:
        extra = "forbid"

class GenericPublic(GenericOutput): # Visible to any user.
    pass

class GenericPrivate(GenericOutput): # Visible to specific user/s only.
    pass

class GenericFullInput(GenericInput): # Attributes not determined by server.
    class Config(GenericInput.Config):
        pass

class GenericPartialInput(GenericInput): # Attributes not determined by server - Nullable.
    class Config(GenericInput.Config):
        pass