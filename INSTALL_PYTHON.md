# Python Installation Guide for Windows

## Step 1: Download Python

1. Go to: https://www.python.org/downloads/
2. Click **"Download Python 3.12.x"** (latest version)
3. Save the installer to your computer

## Step 2: Install Python

1. **Run the installer** (python-3.12.x-amd64.exe)

2. ⚠️ **IMPORTANT**: Check these boxes:
   - ✅ **"Add python.exe to PATH"** (MUST check this!)
   - ✅ "Install pip"
   - ✅ "Install for all users" (optional)

3. Click **"Install Now"**

4. Wait for installation to complete

5. Click **"Close"**

## Step 3: Verify Installation

Open a **NEW PowerShell window** and run:

```powershell
python --version
```

You should see: `Python 3.12.x`

Also check pip:

```powershell
pip --version
```

## Step 4: Install Project Dependencies

Navigate to your project and install required packages:

```powershell
cd C:\Users\D\Desktop\Lottery\lottery-scraper-api
pip install -r requirements.txt
```

This will install:
- FastAPI (web framework)
- BeautifulSoup4 (HTML parsing)
- Requests (HTTP library)
- SQLAlchemy (database)
- APScheduler (task scheduling)
- And other dependencies

## Step 5: Test Your Installation

```powershell
python test_scraper.py
```

## Troubleshooting

### "python is not recognized"

**Problem**: PATH wasn't added during installation

**Solution 1** - Reinstall Python:
1. Uninstall Python from Windows Settings
2. Download installer again
3. This time, CHECK "Add python.exe to PATH"
4. Install

**Solution 2** - Add to PATH manually:
1. Search Windows for "Environment Variables"
2. Click "Environment Variables"
3. Under "System Variables", find "Path"
4. Click "Edit"
5. Click "New"
6. Add: `C:\Users\D\AppData\Local\Programs\Python\Python312\`
7. Add: `C:\Users\D\AppData\Local\Programs\Python\Python312\Scripts\`
8. Click OK
9. **Restart PowerShell**

### "pip is not recognized"

Try:
```powershell
python -m pip --version
```

If that works, use `python -m pip install` instead of `pip install`

### Permission denied during pip install

Run PowerShell as Administrator:
1. Right-click PowerShell
2. Choose "Run as Administrator"
3. Try `pip install -r requirements.txt` again

## Quick Reference

After installation, use these commands:

```powershell
# Check Python version
python --version

# Check pip version
pip --version

# Install packages from requirements.txt
pip install -r requirements.txt

# Install a single package
pip install requests

# List installed packages
pip list

# Run Python script
python script_name.py

# Run Python script with arguments
python script_name.py --debug
```

## Next Steps After Installing Python

1. **Install dependencies**:
   ```powershell
   cd C:\Users\D\Desktop\Lottery\lottery-scraper-api
   pip install -r requirements.txt
   ```

2. **Test the scraper**:
   ```powershell
   python test_scraper.py
   ```

3. **Start the API server**:
   ```powershell
   python main.py
   ```

4. **Access API documentation**:
   - Open browser: http://localhost:8000/docs

## Alternative: Use Python from Microsoft Store

If the installer doesn't work:

1. Open **Microsoft Store**
2. Search for "Python 3.12"
3. Click **Install**
4. Automatically adds to PATH
5. Access via `python` or `python3` command

Then continue with Step 4 above.
