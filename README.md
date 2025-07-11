🖱️ Mouse Jiggler for macOS
A simple Python-based desktop app to simulate mouse movement and prevent your Mac from sleeping or starting the screensaver.

📦 Setup Instructions
✅ Step 1: Download the Files
Download main.py from this repository.
Download requirements.txt if available.

🧰 Step 2: Set Up Python Environment
Open Terminal on your Mac.

Navigate to the folder where you saved the files:
cd /path/to/your/downloaded/files

📦 Step 3: Install Dependencies
Install the required Python packages:

With pip:
pip3 install pyautogui
Or using requirements.txt:
pip3 install -r requirements.txt

🔐 Step 4: Grant Accessibility Permissions
To allow Python to control your mouse:

Go to System Settings → Privacy & Security → Accessibility
Click the lock icon and enter your password to make changes.
Add Terminal (or the app you're using to run Python) to the list of allowed apps.
Ensure the box is checked ✅.

▶️ Step 5: Run the Application
In Terminal, run the app:
python3 main.py
The GUI will open with Start and Stop buttons to control the real mouse jiggling.



