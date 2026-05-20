# Simulasi Keamanan Cloud Storage

Prototype simulasi keamanan cloud storage berbasis **Multilayer Security** untuk mengamankan data pada penyimpanan lokal sebelum diunggah ke cloud. Sistem ini mengintegrasikan kriptografi simetris, asimetris, hashing, steganografi, hingga pencatatan integritas berbasis blockchain.

---
## Multilayer Security Features
- **AES-256 Encryption**
- **RSA-2048 Key Protection**
- **SHA-256 Hashing**
- **Simple Blockchain Verification**
- **LSB Steganography**
- **Streamlit Interface**
---

## Install Dependency

```python
pip install -r requirements.txt
```
---

## Menjalankan Pengujian 
1. AES Encryption Test

- generate AES key
- encrypt file
- decrypt file
- chunk encryption

 ```python
python tests/test_aes.py
 ```

2. RSA Encryption Test

- generate RSA keypair
- encrypt AES key
- decrypt AES key

```python
python tests/test_rsa.py
```

3. SHA-256 Hash Test

- generate file hash
- verify integrity

```python
python tests/test_hash.py
```

4. Blockchain Test

- genesis block
- add block
- blockchain integrity verification
```python
python tests/test_blockchain.py
```

5. LSB Steganography Test
- embed metadata ke gambar
- extract metadata dari gambar
```python
python tests/test_stego.py
```

6. Backend Security Simulation Test

Menguji seluruh backend security module secara detail:
- AES Encryption
- RSA Protection
- SHA-256 Hashing
- Metadata Steganography
- Recovery Process

```python
python tests/test_backend.py
```

7. Full Workflow Integration Test

Menguji workflow utama sistem:

- Secure File
- encrypt file
- encrypt AES key
- generate hash
- save hash to blockchain
- embed metadata
- Recover File
- extract metadata
- verify blockchain
- verify file integrity
- decrypt AES key
- decrypt file

```python
python tests/test_workflow.py
```