"""

Privacy1 AB CONFIDENTIAL
________________________

 [2017] - [2018] Privacy1 AB
 All Rights Reserved.

 NOTICE:  All information contained herein is, and remains the property
 of Privacy1 AB.  The intellectual and technical concepts contained herein
 are proprietary to Privacy1 AB and may be covered by European, U.S. and Foreign
 Patents, patents in process, and are protected by trade secret or copyright law.

 Dissemination of this information or reproduction of this material
 is strictly forbidden.
 """

import os
import base64
import struct
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from keychainClient.exception import KeychainEncryptionException
from keychainClient.model import KeySpec

class KeychainEncryptor:

    TAG_SIZE_IN_BYTES = 16
    IV_SIZE_IN_BYTES = 12

    VERSION_SIZE_IN_BYTES = 1
    KEY_VERSION_SIZE_IN_BYTES = 1

    STREAM_BLOCK_SIZE = 32 * 1024 * 1024

    def __init__(self):
        self.VERSION = 0x01

    def encrypt(self, keySpec, plainTextBytes):
        iv = self.__generateIv()
        return self.encryptWithIv(keySpec, plainTextBytes, iv)

    def encryptWithIv(self, keySpec, plainTextBytes, iv):
        aesgcm = AESGCM(keySpec.getKey())
        cipherTextBytes = aesgcm.encrypt(nonce=iv, data=plainTextBytes,
                                         associated_data=keySpec.getCategory().encode("utf-8"))
        versionByte = struct.pack(">B", self.VERSION)
        keyVersionByte = struct.pack(">B", keySpec.getKeyVersion())
        return versionByte + keyVersionByte + iv + cipherTextBytes

    def encryptStream(self, keySpec, inFileName, outFileName):
        iv = self.__generateIv()
        versionByte = struct.pack(">B", self.VERSION)
        keyVersionByte = struct.pack(">B", keySpec.getKeyVersion())

        outFile = open(outFileName, 'wb')
        outFile.write(versionByte)
        outFile.write(keyVersionByte)
        outFile.write(iv)

        asegcm = AESGCM(keySpec.getKey())
        def read_in_trunk(fileObject, chunkSize = self.STREAM_BLOCK_SIZE):
            while True:
                data = fileObject.read(chunkSize)
                if not data:
                    break
                yield data

        with open(inFileName, 'rb') as inFile:
            for chunk in read_in_trunk(inFile):
                cipherStream = asegcm.encrypt(nonce=iv, data=chunk, associated_data=keySpec.getCategory().encode("utf-8"))
                outFile.write(cipherStream)
        
        inFile.close()
        outFile.close()

    def encryptAndEncode(self, keySpec, plainTextBytes):
        cipherText = self.encrypt(keySpec, plainTextBytes)
        return base64.b64encode(cipherText).decode('utf-8')

    def decrypt(self, keySpec, cipherTextBytes):
        if len(cipherTextBytes) <= self.TAG_SIZE_IN_BYTES + self.IV_SIZE_IN_BYTES + self.VERSION_SIZE_IN_BYTES \
                + self.KEY_VERSION_SIZE_IN_BYTES:
            raise KeychainEncryptionException("Invalid encrypt bytes size " + str(len(cipherTextBytes)))

        versionByte = cipherTextBytes[0:self.VERSION_SIZE_IN_BYTES]
        version = struct.unpack(">B", versionByte)[0]
        if version != self.VERSION:
            raise KeychainEncryptionException("Version mismatch. Expected " + str(self.VERSION) +
                                              ", Using in data " + str(version))

        keyVersionByte = \
            cipherTextBytes[self.VERSION_SIZE_IN_BYTES:self.VERSION_SIZE_IN_BYTES + self.KEY_VERSION_SIZE_IN_BYTES]
        keyVersion = struct.unpack(">B", keyVersionByte)[0]
        if keyVersion != keySpec.getKeyVersion():
            raise KeychainEncryptionException("Key version mismatch. Expected " + str(keySpec.getKeyVersion()) +
                                              ", Using in data " + str(keyVersion))

        iv = cipherTextBytes[self.VERSION_SIZE_IN_BYTES + self.KEY_VERSION_SIZE_IN_BYTES:
                             self.VERSION_SIZE_IN_BYTES + self.KEY_VERSION_SIZE_IN_BYTES + self.IV_SIZE_IN_BYTES]

        encryptBytes = cipherTextBytes[self.VERSION_SIZE_IN_BYTES + self.KEY_VERSION_SIZE_IN_BYTES + self.IV_SIZE_IN_BYTES:]

        aesgcm = AESGCM(keySpec.getKey())
        return aesgcm.decrypt(nonce=iv, data=encryptBytes, associated_data=keySpec.getCategory().encode("utf-8"))

    def decryptStream(self, keySpec, inEncryptFileName, outPlainFileName):
        inFile = open(inEncryptFileName, "rb")
        versionByte = inFile.read(self.VERSION_SIZE_IN_BYTES)
        version = struct.unpack(">B", versionByte)[0]
        if version != self.VERSION:
            raise KeychainEncryptionException("Version mismatch. Expected " + str(self.VERSION) +
                                              ", Using in data " + str(version))

        keyVersionByte = inFile.read(self.KEY_VERSION_SIZE_IN_BYTES)
        keyVersion = struct.unpack(">B", keyVersionByte)[0]
        if keyVersion != keySpec.getKeyVersion():
            raise KeychainEncryptionException("Key version mismatch. Expected " + str(keySpec.getKeyVersion()) +
                                              ", Using in data " + str(keyVersion))

        iv = inFile.read(self.IV_SIZE_IN_BYTES)
        aesgcm = AESGCM(keySpec.getKey())

        outFile = open(outPlainFileName, "wb")
        def read_in_trunk(fileObject, chunkSize = self.STREAM_BLOCK_SIZE):
            while True:
                data = fileObject.read(chunkSize)
                if not data:
                    break
                yield data
        for chunk in read_in_trunk(inFile):
            plainStream = aesgcm.decrypt(nonce=iv, data=chunk, associated_data=keySpec.getCategory().encode("utf-8"))
            outFile.write(plainStream)

        inFile.close()
        outFile.close()

    def decodeAndDecrypt(self, keySpec, cipherText):
        cipherTextBytes = base64.b64decode(cipherText)
        return self.decrypt(keySpec, cipherTextBytes)

    def __generateIv(self):
        return os.urandom(self.IV_SIZE_IN_BYTES)
