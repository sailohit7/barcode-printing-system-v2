"""Persistent SQL Server connection settings with Windows DPAPI password protection."""
import json
import os
from pathlib import Path

APP_DIR = Path(os.environ.get("APPDATA", str(Path.home()))) / "BarcodePrintingSystem"
SETTINGS_FILE = APP_DIR / "sql_connection.json"


def _protect_password(password: str) -> str:
    if not password:
        return ""
    try:
        import win32crypt
        encrypted = win32crypt.CryptProtectData(password.encode("utf-8"), "Barcode Printing System", None, None, None, 0)
        return encrypted.hex()
    except Exception as exc:
        raise RuntimeError("Secure password storage requires the Windows pywin32 package. Install it with: pip install pywin32") from exc


def _unprotect_password(encrypted_hex: str) -> str:
    if not encrypted_hex:
        return ""
    try:
        import win32crypt
        decrypted = win32crypt.CryptUnprotectData(bytes.fromhex(encrypted_hex), None, None, None, 0)[1]
        return decrypted.decode("utf-8")
    except Exception as exc:
        raise RuntimeError("The saved SQL password could not be decrypted on this Windows account. Please enter it again.") from exc


def save_connection_settings(settings: dict) -> None:
    APP_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "driver": settings.get("driver", "SQL Server"),
        "server": settings.get("server", ".\\SQLEXPRESS").strip(),
        "database": settings.get("database", "barcode_system").strip(),
        "authentication": settings.get("authentication", "Windows"),
        "username": settings.get("username", "").strip(),
        "password_protected": _protect_password(settings.get("password", "")) if settings.get("authentication") == "SQL Server" else "",
        "trust_server_certificate": bool(settings.get("trust_server_certificate", True)),
    }
    temporary = SETTINGS_FILE.with_suffix(".tmp")
    temporary.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    temporary.replace(SETTINGS_FILE)


def load_connection_settings() -> dict:
    if not SETTINGS_FILE.exists():
        return {
            "driver": "SQL Server", "server": ".\\SQLEXPRESS", "database": "barcode_system",
            "authentication": "Windows", "username": "", "password": "",
            "trust_server_certificate": True,
        }
    payload = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
    payload["password"] = _unprotect_password(payload.pop("password_protected", ""))
    return payload
