from .core.app import BookRecommendationsApp
from .routes import books, recommendations
from .lib.scalar import router as scalar_router

app = BookRecommendationsApp(
    title="Book Recommendations API",
    description="""
    A modern API for book recommendations using both traditional and AI-enhanced methods.
    
    ## Features
    
    * **Book Management**: Full CRUD operations for books
    * **User Management**: Create and manage user profiles
    * **Recommendations**:
        * Traditional recommendations based on similarity metrics
        * AI-enhanced recommendations using advanced language models
    * **Documentation**:
        * OpenAPI/Swagger UI at `/docs`
        * ReDoc at `/redoc`
        * Scalar docs at `/scalar`
    
    ## Models
    
    * **Book**: Represents a book with title, author, description, genres, etc.
    * **User**: Represents a user with username, email, etc.
    * **UserBook**: Tracks user-book interactions including ratings
    
    ## Authentication
    
    API key authentication is required for all endpoints.
    Include your API key in the `X-API-Key` header.
    
    ## Rate Limiting
    
    * Standard endpoints: 100 requests per minute
    * AI recommendation endpoints: 10 requests per minute
    
    ## Errors
    
    The API uses standard HTTP status codes and includes detailed error messages
    in the response body when something goes wrong.
    """,
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@bookrecommendations.example.com",
        "url": "https://bookrecommendations.example.com/support",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {
            "name": "books",
            "description": "Operations with books, including CRUD and search.",
        },
        {
            "name": "recommendations",
            "description": "Book recommendation endpoints using traditional and AI methods.",
        },
    ],
    # Use separate schemas for input/output for better OpenAPI documentation
    separate_input_output_schemas=True,
)

# Include routers
app.include_router(books.router)
app.include_router(recommendations.router)
app.include_router(scalar_router)