from pydantic import BaseModel, HttpUrl, Field, conint
from typing import List, Optional

class QRCodeRequest(BaseModel):
    url: str
    fill_color: str = "red"
    back_color: str = "white"
    size: int = 10

    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://example.com",
                "fill_color": "black",
                "back_color": "yellow",
                "size": 20
            }
        }

class Link(BaseModel):
    rel: str = Field(..., description="Relation type of the link.")
    href: HttpUrl = Field(..., description="The URL of the link.")
    action: str = Field(..., description="HTTP method for the action this link represents.")
    type: str = Field(default="application/json", description="Content type of the response for this link.")

    class Config:
        json_schema_extra = {
            "example": {
                "rel": "self",
                "href": "https://api.example.com/qr/123",
                "action": "GET",
                "type": "application/json"
            }
        }

class QRCodeResponse(BaseModel):
    message: str = Field(..., description="A message related to the QR code request.")
    qr_code_url: HttpUrl = Field(..., description="The URL to the generated QR code.")
    links: List[Link] = Field(default=[], description="HATEOAS links related to the QR code.")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "QR code created successfully.",
                "qr_code_url": "https://api.example.com/qr/123",
                "links": [
                    {
                        "rel": "self",
                        "href": "https://api.example.com/qr/123",
                        "action": "GET",
                        "type": "application/json"
                    }
                ]
            }
        }

class Token(BaseModel):
    access_token: str = Field(..., description="The access token for authentication.")
    token_type: str = Field(default="bearer", description="The type of the token.")

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "jhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }

class TokenData(BaseModel):
    username: Optional[str] = Field(None, description="The username that the token represents.")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "user@example.com"
            }
        }
