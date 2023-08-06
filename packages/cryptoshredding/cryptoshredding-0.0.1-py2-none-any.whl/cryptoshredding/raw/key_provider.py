from aws_encryption_sdk.identifiers import EncryptionKeyType, WrappingAlgorithm
from aws_encryption_sdk.internal.crypto.wrapping_keys import WrappingKey
from aws_encryption_sdk.key_providers.raw import RawMasterKeyProvider

from ..key_store import KeyStore


class KeyStoreKeyProvider(RawMasterKeyProvider):
    provider_id = "key_store"

    def __init__(self, key_store: KeyStore):
        self._key_store = key_store

    def _get_raw_key(self, key_id):
        key = self._key_store.get_key(key_id=key_id)
        
        return WrappingKey(
            wrapping_algorithm=WrappingAlgorithm.AES_256_GCM_IV12_TAG16_NO_PADDING,
            wrapping_key=key,
            wrapping_key_type=EncryptionKeyType.SYMMETRIC,
        )
