class GenericOutput:
    pass

class GenericInput:
    pass

class GenericPublic(GenericOutput): # Visible to any user.
    pass

class GenericPrivate(GenericOutput): # Visible to specific user/s only.
    pass

class GenericFullInput(GenericInput): # Attributes not determined by server.
    pass

class GenericPartialInput(GenericInput): # Attributes not determined by server - Nullable.
    pass