# apps/api/crypto_service.py
from typing import Tuple

def encrypt_at_rest(plaintext: bytes) -> Tuple[bytes, bytes]:
    # Placeholder: brancher une lib (p.ex. Fernet / AES-GCM)
    # return (ciphertext, iv)
    return plaintext, b"iv"

def encrypt_in_transit():
    # Config côté infra: TLS 1.3 via reverse proxy (Nginx/Traefik)
    return True

def segment_route(resource_path: str) -> str:
    # Ex: "/certification/*" => "sensitive", "/reports/*" => "public"
    return "sensitive" if resource_path.startswith("/certification") else "public"
