from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


def load_keys():
    with open("./private_key.pem", "rb") as private_pem:
        private_key = serialization.load_pem_private_key(
            data=private_pem.read(), password=None
        )
    with open("./public_key.pem", "rb") as public_pem:
        public_key = serialization.load_pem_public_key(data=public_pem.read())

    return (
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        ),
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ),
    )


def generate_rsa_keys(key_size):
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),  # better to use encryption obviously
    )

    public_key = private_key.public_key()

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    # write keys to pem file
    with open("./private_key.pem", "wb") as file:
        file.write(private_pem)

    with open("./public_key.pem", "wb") as file:
        file.write(public_pem)


if __name__ == "__main__":
    generate_rsa_keys(key_size=4096)
