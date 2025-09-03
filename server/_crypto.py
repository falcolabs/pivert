import os

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
from cryptography.hazmat.primitives import serialization as crypto_serialization

def init_keystore() -> tuple[str, str]:
    if not os.path.exists("privatekey.pem"):
        key = rsa.generate_private_key(
            backend=crypto_default_backend(), public_exponent=65537, key_size=2048
        )
        with open("privatekey.pem", "w", encoding="utf-8") as f:
            f.write(
                private := key.private_bytes(
                    crypto_serialization.Encoding.PEM,
                    crypto_serialization.PrivateFormat.TraditionalOpenSSL,
                    crypto_serialization.NoEncryption(),
                ).decode("utf-8")
            )

        with open("publickey.pem", "w", encoding="utf-8") as f:
            f.write(
                public := key.public_key()
                .public_bytes(
                    crypto_serialization.Encoding.PEM,
                    crypto_serialization.PublicFormat.PKCS1,
                )
                .decode("utf-8")
            )
        return public, private
    else:
        with open("publickey.pem", "r", encoding="utf-8") as public:
            with open("privatekey.pem", "r", encoding="utf-8") as private:
                return public.read().strip(), private.read().strip()
            