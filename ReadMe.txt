#Step 1: Install Required Python Packages

pip install pycryptodome

pip install pyinstaller

#Step 2: Create Your Own Certificate
Generate a Self-Signed Certificate:

You can create a self-signed certificate using OpenSSL. First, install OpenSSL (if not already installed). Then run the following commands:

openssl req -newkey rsa:2048 -nodes -keyout mycert.key -x509 -days 365 -out mycert.crt

Convert the Certificate to PFX Format:

Convert the certificate to a PFX file:

openssl pkcs12 -export -out mycert.pfx -inkey mycert.key -in mycert.crt

#Step 3: Install SignTool
*Install Windows 10 SDK:

*SignTool is part of the Windows 10 SDK. Download and install it from the Microsoft website.

*Locate SignTool:

After installing the Windows 10 SDK, locate the SignTool executable. It is typically found in: C:\\Program Files (x86)\\Windows Kits\\10\\App Certification Kit\\signtool.exe"

#Step 4: Prepare Your Script and Input File
Save Your Script:

*Prepare the Input File:

*Ensure you have an input.exe file in the same directory as your script. This is the file you want to encrypt and later decrypt/extract.

#Step 5: Run the Script
Execute the Script:

python encryptor.py (or use the batch file run_script.bat)

*Verify the Output:

*If everything is set up correctly, the script will generate a loader.exe file. This file is the encrypted loader executable.

Step 6: Test the Loader Executable
Run the Loader Executable:

Test the loader.exe to ensure it decrypts and runs the input.exe correctly.

!!!!After all requierments are installed. Create you cert. Put "mycert.pfx" into the same folder as encryptor.py.
Also, add in your file to be encrypted. rename that file "input.exe". (make sure in encryptor.py you added your correct
path to your signtool location.)
Run the script.


Troubleshooting Tips
*Ensure all paths in the script (such as signtool_path) are correct.
*Verify the input file (input.exe) exists and is accessible.
*Check that Python and required libraries are correctly installed.
*Make sure OpenSSL is installed and in your system's PATH for certificate creation.

Disclaimer: Educational Use Only

This tool, PyCrypt, is provided for educational purposes only. By using this tool, you agree that:

*Non-Commercial Use: PyCrypt is intended solely for educational and informational purposes. It should not be used for any commercial, illegal, or unethical activities.

*No Warranty: This tool is provided "as is," without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement.

*Limitation of Liability: The authors, contributors, and distributors of PyCrypt shall not be liable for any direct, indirect, incidental, special, exemplary, or consequential damages (including, but not limited to, procurement of substitute goods or services; loss of use, data, or profits; or business interruption) however caused and on any theory of liability, whether in contract, strict liability, or tort (including negligence or otherwise) arising in any way out of the use of this tool, even if advised of the possibility of such damage.

*User Responsibility: Users are solely responsible for their use of PyCrypt. It is the user's responsibility to ensure compliance with all applicable laws and regulations.

*Legal Advice: This disclaimer does not constitute legal advice. Users should consult with a qualified legal professional for advice on their specific circumstances.

##### By using PyCrypt, you acknowledge and agree to abide by the terms of this disclaimer. If you do not agree with these terms, you should not use PyCrypt. #####

