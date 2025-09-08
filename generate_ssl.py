import os
from pathlib import Path
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from datetime import datetime, timedelta

# Create ssl directory if it doesn't exist
ssl_dir = Path("ssl")
ssl_dir.mkdir(exist_ok=True)

# Generate private key
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

# Create a self-signed certificate
subject = issuer = x509.Name(
    [
        x509.NameAttribute(NameOID.COUNTRY_NAME, "SL"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Western Area"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Freetown"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Fourah Bay College"),
        x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, "Library"),
        x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
    ]
)

cert = (
    x509.CertificateBuilder()
    .subject_name(subject)
    .issuer_name(issuer)
    .public_key(private_key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.utcnow())
    .not_valid_after(datetime.utcnow() + timedelta(days=365))
    .add_extension(
        x509.SubjectAlternativeName([x509.DNSName("localhost")]),
        critical=False,
    )
    .sign(private_key, hashes.SHA256())
)

# Write private key
with open(ssl_dir / "private.key", "wb") as f:
    f.write(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )

# Write certificate
with open(ssl_dir / "certificate.crt", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

print("SSL certificate and private key have been generated in the ssl directory")
