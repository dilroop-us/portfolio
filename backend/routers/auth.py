from fastapi import APIRouter, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
import uuid
import secrets
import base64
import hashlib

from backend.schemas import (
    AuthDemoRequest, TokenResponse, TokenPairResponse, RefreshTokenRequest,
    RevokeTokenRequest, ValidateTokenRequest, ValidateTokenResponse,
    OAuth2AuthRequest, OAuth2TokenRequest, OAuth2TokenResponse,
    RBACPermissionCheck, RBACResponse
)
from backend.config import settings
from backend.redis_client import redis_client

router = APIRouter(prefix="/api", tags=["auth"])

oauth2_codes = {}
user_roles = {
    "user_1": {"role": "admin", "permissions": ["read", "write", "delete", "admin"]},
    "user_2": {"role": "editor", "permissions": ["read", "write"]},
    "user_3": {"role": "viewer", "permissions": ["read"]},
}

@router.post("/auth/demo", response_model=TokenResponse)
async def auth_demo(request: AuthDemoRequest):
    algorithm = request.algorithm or "HS256"
    
    if not algorithm.startswith('HS'):
        raise HTTPException(
            status_code=400,
            detail=f"{algorithm} requires PEM-formatted cryptographic keys. This demo only supports HMAC algorithms (HS256, HS384, HS512). For RSA/ECDSA/RSA-PSS demos, use the frontend client-side implementation."
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    to_encode = {
        "sub": request.username,
        "exp": datetime.utcnow() + access_token_expires,
        "iat": datetime.utcnow(),
        "role": "backend_engineer"
    }
    
    try:
        access_token = jwt.encode(to_encode, settings.secret_key, algorithm=algorithm)
        decoded = jwt.decode(access_token, settings.secret_key, algorithms=[algorithm])
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            decoded=decoded
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"JWT encoding failed: {str(e)}"
        )

@router.post("/auth/token-pair", response_model=TokenPairResponse)
async def generate_token_pair(request: AuthDemoRequest):
    access_expires = timedelta(minutes=15)
    refresh_expires = timedelta(days=7)
    
    jti_access = str(uuid.uuid4())
    jti_refresh = str(uuid.uuid4())
    
    access_payload = {
        "sub": request.username,
        "exp": datetime.utcnow() + access_expires,
        "iat": datetime.utcnow(),
        "jti": jti_access,
        "type": "access",
        "role": "fullstack_engineer"
    }
    
    refresh_payload = {
        "sub": request.username,
        "exp": datetime.utcnow() + refresh_expires,
        "iat": datetime.utcnow(),
        "jti": jti_refresh,
        "type": "refresh"
    }
    
    algorithm = request.algorithm or "HS256"
    access_token = jwt.encode(access_payload, settings.secret_key, algorithm=algorithm)
    refresh_token = jwt.encode(refresh_payload, settings.secret_key, algorithm=algorithm)
    
    return TokenPairResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=900,
        decoded_access=access_payload,
        decoded_refresh=refresh_payload
    )

@router.post("/auth/refresh", response_model=TokenResponse)
async def refresh_access_token(request: RefreshTokenRequest):
    try:
        decoded = jwt.decode(request.refresh_token, settings.secret_key, algorithms=["HS256"])
        
        if decoded.get("type") != "refresh":
            raise HTTPException(status_code=400, detail="Invalid token type")
        
        if redis_client.exists(f"blacklist:{decoded['jti']}"):
            raise HTTPException(status_code=401, detail="Token has been revoked")
        
        new_jti = str(uuid.uuid4())
        access_payload = {
            "sub": decoded["sub"],
            "exp": datetime.utcnow() + timedelta(minutes=15),
            "iat": datetime.utcnow(),
            "jti": new_jti,
            "type": "access",
            "role": decoded.get("role", "fullstack_engineer")
        }
        
        access_token = jwt.encode(access_payload, settings.secret_key, algorithm="HS256")
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            decoded=access_payload
        )
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid refresh token: {str(e)}")

@router.post("/auth/revoke")
async def revoke_token(request: RevokeTokenRequest):
    try:
        decoded = jwt.decode(request.token, settings.secret_key, algorithms=["HS256"])
        jti = decoded.get("jti")
        
        if jti and redis_client.is_connected():
            exp = decoded.get("exp")
            if exp:
                ttl = int(exp - datetime.utcnow().timestamp())
                redis_client.set(f"blacklist:{jti}", "revoked", ttl)
        
        return {"message": "Token revoked successfully", "jti": jti}
    except JWTError as e:
        raise HTTPException(status_code=400, detail=f"Invalid token: {str(e)}")

@router.post("/auth/validate", response_model=ValidateTokenResponse)
async def validate_token(request: ValidateTokenRequest):
    try:
        decoded = jwt.decode(request.token, settings.secret_key, algorithms=[request.algorithm])
        
        jti = decoded.get("jti")
        if jti and redis_client.exists(f"blacklist:{jti}"):
            return ValidateTokenResponse(
                valid=False,
                error="Token has been revoked"
            )
        
        return ValidateTokenResponse(
            valid=True,
            decoded=decoded
        )
    except JWTError as e:
        return ValidateTokenResponse(
            valid=False,
            error=str(e)
        )

@router.post("/oauth2/authorize", response_model=dict)
async def oauth2_authorize(request: OAuth2AuthRequest):
    code = secrets.token_urlsafe(32)
    code_verifier = secrets.token_urlsafe(32)
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest()).decode().rstrip('=')
    
    oauth2_codes[code] = {
        "client_id": request.client_id,
        "redirect_uri": request.redirect_uri,
        "scope": request.scope,
        "code_verifier": code_verifier
    }
    
    return {
        "authorization_url": f"{request.redirect_uri}?code={code}&state={request.state or ''}",
        "code": code,
        "code_verifier": code_verifier,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256"
    }

@router.post("/oauth2/token", response_model=OAuth2TokenResponse)
async def oauth2_token(request: OAuth2TokenRequest):
    if request.code not in oauth2_codes:
        raise HTTPException(status_code=400, detail="Invalid authorization code")
    
    code_data = oauth2_codes[request.code]
    
    if code_data["client_id"] != request.client_id:
        raise HTTPException(status_code=400, detail="Client ID mismatch")
    
    expected_verifier = code_data["code_verifier"]
    if request.code_verifier != expected_verifier:
        raise HTTPException(status_code=400, detail="Code verifier validation failed")
    
    access_token = jwt.encode(
        {"sub": request.client_id, "exp": datetime.utcnow() + timedelta(hours=1), "scope": code_data["scope"]},
        settings.secret_key,
        algorithm="HS256"
    )
    
    refresh_token = jwt.encode(
        {"sub": request.client_id, "exp": datetime.utcnow() + timedelta(days=7)},
        settings.secret_key,
        algorithm="HS256"
    )
    
    del oauth2_codes[request.code]
    
    return OAuth2TokenResponse(
        access_token=access_token,
        token_type="Bearer",
        expires_in=3600,
        refresh_token=refresh_token,
        scope=code_data["scope"]
    )

@router.post("/rbac/check", response_model=RBACResponse)
async def check_permission(request: RBACPermissionCheck):
    user = user_roles.get(request.user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    resource_permissions = {
        "projects": ["read"],
        "users": ["read", "write", "admin"],
        "settings": ["admin"]
    }
    
    required = resource_permissions.get(request.resource, [])
    if request.action in required and request.action in user["permissions"]:
        allowed = True
    else:
        allowed = request.action in user["permissions"]
    
    return RBACResponse(
        allowed=allowed,
        user_role=user["role"],
        required_permissions=required,
        user_permissions=user["permissions"]
    )
