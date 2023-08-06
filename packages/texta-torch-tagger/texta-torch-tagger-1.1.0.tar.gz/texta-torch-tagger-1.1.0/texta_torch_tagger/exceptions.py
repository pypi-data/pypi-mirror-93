class NoEmbeddingError(Exception):
    """Raised when Embedding not included when needed."""
    pass

    
class PosLabelNotSpecifiedError(Exception):
    """Raised when positive label is not specified with binary label set."""
    pass
