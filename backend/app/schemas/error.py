from pydantic import BaseModel, Field

class ErrorResponse(BaseModel):
    detail: str = Field(description="Human-readable reason the request failed")

class HealthStatus(BaseModel):
    status: str = Field(description="Service status, 'healthy' when the API is up")
