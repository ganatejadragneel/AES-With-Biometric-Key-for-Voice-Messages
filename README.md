# AES-With-Biometric-Key-for-Voice-Messages

A secure voice message encryption and decryption system using fingerprint biometrics as cryptographic keys.

## Overview

This project implements a secure voice message system that uses biometric data (fingerprints) as encryption keys. The system encrypts audio recordings using the Advanced Encryption Standard (AES) in Counter Mode (CTR), with the encryption key derived from fingerprint feature extraction. This approach combines the security of AES encryption with the uniqueness of biometric identification.

## System Architecture

The project is organized into the following components:

```
├── Decoder/
│   ├── fp1.jpeg        # Fingerprint image for decryption
│   ├── main.py         # Decryption script
├── Encoder/
│   ├── config.dictionary  # Stores encrypted data
│   ├── fp1.jpeg        # Primary fingerprint image
│   ├── fp2.jpeg        # Secondary fingerprint image
│   ├── fp3.jpeg        # Tertiary fingerprint image
│   ├── main.py         # Encryption script
│   ├── output.wav      # Recorded voice message
├── Fingerprint/
│   ├── fingerprint_detection.py  # Fingerprint processing library
│   ├── fp1.jpeg        # Fingerprint sample
│   ├── fp2.jpeg        # Fingerprint sample
│   ├── fp3.jpeg        # Fingerprint sample
├── Voice Encoder/
│   ├── aud.py          # Audio recording and processing utilities
│   ├── output.wav      # Sample output file
├── pycrypto/
│   ├── crypt.py        # AES encryption/decryption utilities
```

## Key Features

- **Biometric Key Generation**: Extracts unique features from fingerprint images to create cryptographic keys
- **Voice Recording**: Captures voice messages through microphone input
- **AES Encryption**: Secures voice data using AES-256 in Counter (CTR) mode
- **Secure Message Storage**: Stores encrypted messages with their initialization vectors (IVs)
- **Authorized Decryption**: Requires matching fingerprint to recover original voice messages

## How It Works

### Encryption Process

1. **Fingerprint Processing**:
   - Captures fingerprint image
   - Applies image enhancement and feature extraction
   - Generates a 32-byte (256-bit) key from fingerprint features

2. **Voice Recording**:
   - Records audio via microphone input
   - Processes the audio data for encryption

3. **Encryption**:
   - Uses the fingerprint-derived key with AES-CTR mode
   - Generates unique initialization vectors (IVs) for each audio segment
   - Stores encrypted data and IVs in a dictionary file

### Decryption Process

1. **Fingerprint Verification**:
   - Processes the provided fingerprint using the same algorithm
   - Generates the decryption key

2. **Message Recovery**:
   - Loads the encrypted data and IVs
   - Decrypts each segment using the fingerprint-derived key
   - Reconstructs the original voice message

## Requirements

- Python 3.6+
- OpenCV (`cv2`)
- NumPy
- scikit-image
- matplotlib
- PIL (Pillow)
- pyaudio
- audioread
- pycrypto or pycryptodome

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/AES-With-Biometric-Key-for-Voice-Messages.git
cd AES-With-Biometric-Key-for-Voice-Messages

# Install required packages
pip install -r requirements.txt
```

## Usage

### Recording and Encrypting a Voice Message

```bash
cd Encoder
python main.py
```

This will:
1. Prompt you to record a voice message
2. Process your fingerprint from fp1.jpeg
3. Encrypt the voice message using your fingerprint as the key
4. Store the encrypted data in config.dictionary

### Decrypting a Voice Message

```bash
cd Decoder
python main.py
```

This will:
1. Process your fingerprint from fp1.jpeg
2. Attempt to decrypt the message using your fingerprint
3. Play back the decrypted voice message if fingerprint verification succeeds

## Security Considerations

- The system's security depends on the uniqueness of fingerprint features
- The fingerprint images should be stored securely and never transmitted
- AES-CTR mode provides strong encryption with proper IV management
- Physical access to the fingerprint is required for decryption

## Applications

- Secure voice messaging for sensitive communications
- Multi-factor authentication systems
- Biometric-secured data storage
- Military/government classified communications

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- The fingerprint processing code is based on established computer vision techniques
- AES implementation leverages the PyCrypto/PyCryptodome library
