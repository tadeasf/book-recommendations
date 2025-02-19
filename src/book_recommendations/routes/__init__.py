from .books import router as books_router
from .recommendations import router as recommendations_router

__all__ = [
    "books_router",
    "recommendations_router",
    "docs_router",
]
