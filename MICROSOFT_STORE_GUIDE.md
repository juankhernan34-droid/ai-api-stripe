# Microsoft Store Publishing Guide

Get your AI API Stripe Deployment app on the Microsoft Store! 🚀

## Prerequisites

- ✅ Windows 10/11 PC
- ✅ Microsoft account (free)
- ✅ Developer account ($19 one-time fee)
- ✅ Built `.exe` file (see BUILD_DESKTOP_APP.md)

---

## Step 1: Build Your .exe File

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="AI_API_Stripe" desktop_app.py
```

Your app: `dist/AI_API_Stripe.exe`

---

## Step 2: Create Developer Account

1. Go to https://partner.microsoft.com/dashboard/home
2. Click **"Enroll"** or sign in with Microsoft account
3. Pay **$19** (one-time developer fee)
4. Verify your identity (takes 24-48 hours)

---

## Step 3: Prepare App Files

### 3.1 Create App Manifest

Save as `AppxManifest.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<Package xmlns="http://schemas.microsoft.com/appx/manifest/foundation/windows10" 
         xmlns:mp="http://schemas.microsoft.com/appx/2014/relationships/manifests" 
         xmlns:uap="http://schemas.microsoft.com/appx/manifest/uap/windows10">
  
  <Identity
    Name="juankhernan34.AIAPIStripe"
    Publisher="CN=Juan Hernan"
    Version="1.0.0.0" />
  
  <Properties>
    <DisplayName>AI API Stripe Deployment</DisplayName>
    <PublisherDisplayName>Juan Hernan</PublisherDisplayName>
    <Logo>Assets\StoreLogo.png</Logo>
  </Properties>
  
  <Dependencies>
    <TargetDeviceFamily Name="Windows.Desktop" MinVersion="10.0.0.0" MaxVersionTested="10.0.19041.0" />
  </Dependencies>
  
  <Resources>
    <Resource Language="en-us" />
  </Resources>
  
  <Applications>
    <Application Id="App" StartPage="AI_API_Stripe.exe">
      <uap:VisualElements
        DisplayName="AI API Stripe"
        Square150x150Logo="Assets\Square150x150Logo.png"
        Square44x44Logo="Assets\Square44x44Logo.png"
        Description="Deploy AI API with Stripe payment integration in one click"
        BackgroundColor="transparent">
        <uap:DefaultTile />
        <uap:SplashScreen Image="Assets\SplashScreen.png" />
      </uap:VisualElements>
    </Application>
  </Applications>
  
</Package>
```

### 3.2 Create Required Images

You'll need these images in an `Assets/` folder:

- `StoreLogo.png` - 50x50 pixels
- `Square150x150Logo.png` - 150x150 pixels
- `Square44x44Logo.png` - 44x44 pixels
- `SplashScreen.png` - 620x300 pixels

**Option A: Use Online Generator**
1. Go to https://www.favicon-generator.org/
2. Upload a 🚀 emoji or logo
3. Download PNG files

**Option B: Quick DIY**
```python
from PIL import Image, ImageDraw, ImageFont

# Create 150x150 logo
img = Image.new('RGB', (150, 150), color='#1a1a2e')
draw = ImageDraw.Draw(img)
draw.text((50, 50), "🚀", fill='#00d4ff', font=None)
img.save('Assets/Square150x150Logo.png')
```

---

## Step 4: Package Your App

Install Windows App Packaging Project tools:

```bash
# Install MSIX packaging tools
# Go to: https://developer.microsoft.com/en-us/windows/downloads/windows-app-sdk/
```

Or use **MakeAppx.exe** (built into Windows):

```bash
# Create MSIX package
MakeAppx pack /d "C:\path\to\app\folder" /p "AI_API_Stripe.msix"
```

---

## Step 5: Sign Your App

### 5.1 Create Self-Signed Certificate

```powershell
# Run PowerShell as Administrator
$cert = New-SelfSignedCertificate -Type CodeSigningCert -CertStoreLocation cert:\CurrentUser\My -Subject "CN=Juan Hernan"
$CertPassword = ConvertTo-SecureString -String "YourPassword123" -Force -AsPlainText
Export-PfxCertificate -Cert $cert -FilePath "certificate.pfx" -Password $CertPassword
```

### 5.2 Sign MSIX Package

```bash
signtool sign /fd SHA256 /f certificate.pfx /p YourPassword123 /t http://timestamp.digicert.com AI_API_Stripe.msix
```

---

## Step 6: Submit to Microsoft Store

1. Go to https://partner.microsoft.com/dashboard
2. Click **"Create a new app"**
3. Enter app name: **"AI API Stripe Deployment"**
4. Fill in details:
   - **Description:** "Deploy AI API with Stripe payment integration in one click"
   - **Category:** Developer Tools / Business
   - **Price:** Free or $4.99+
   - **Content Rating:** Fill questionnaire

5. Upload your **MSIX package** and **images**
6. Add screenshots (show the beautiful GUI!)
7. Click **"Submit for review"**

---

## Step 7: Wait for Approval ⏳

**Timeline:**
- ✅ Automated scan: 2-4 hours
- ✅ Manual review: 24-48 hours
- ✅ Approval: Usually within 3-5 days

You'll get email updates on progress!

---

## Step 8: Launch! 🎉

Once approved:
- ✅ Your app appears on Microsoft Store
- ✅ People can install with one click
- ✅ Auto-updates handled by Microsoft
- ✅ You keep 85% of revenue (15% Microsoft cut)

---

## Store Listing Tips

### Great Title
✅ "AI API Stripe Deployment - One Click Deploy"

### Great Description
```
Deploy your AI API with Stripe payment integration in ONE CLICK!

Features:
🚀 Beautiful desktop GUI
💳 Stripe subscription billing integrated
🤖 Hugging Face AI models
📦 Deploy to cloud instantly
💰 Start making money immediately

Perfect for:
- AI developers
- Indie makers
- SaaS builders
- Anyone wanting passive income

Enter your credentials once, deploy anywhere!
```

### Great Screenshots
1. Show the main GUI with 🚀 avatar
2. Show deployment success message
3. Show local API running
4. Show pricing plans

---

## Troubleshooting

### "MSIX Certificate Error"
```bash
# Re-sign with correct path
signtool sign /fd SHA256 /f "C:\path\to\certificate.pfx" AI_API_Stripe.msix
```

### "App Rejected"
Check Microsoft's content policies:
- No payment processing UI (we handle via Stripe ✅)
- No harmful content (we're good ✅)
- Working functionality (test before submit!)

### "Need to Update?"
1. Increment version in AppxManifest.xml
2. Rebuild MSIX package
3. Resubmit to Store (goes faster next time)

---

## Make Money! 💰

### Pricing Options:

**Free + In-App**
- List for free
- Charge for premium features
- Easy way to get users

**Paid App**
- Charge $4.99 - $99.99
- You keep 85%
- Good for serious tools

**Subscription**
- $9.99/month tier in app
- Recurring revenue
- Microsoft handles billing

**Recommended:** Start FREE to build audience, add premium features later

---

## Next Steps

1. ✅ Build `.exe` → `pyinstaller --onefile --windowed --name="AI_API_Stripe" desktop_app.py`
2. ✅ Create images folder with PNG files
3. ✅ Create AppxManifest.xml
4. ✅ Package with MakeAppx
5. ✅ Sign with certificate
6. ✅ Submit to Partner Dashboard
7. ✅ Wait for approval
8. ✅ Launch! 🚀

---

## Resources

- Microsoft Store Submission: https://docs.microsoft.com/en-us/windows/apps/publish/
- MSIX Packaging: https://docs.microsoft.com/en-us/windows/msix/
- App Manifest Schema: https://docs.microsoft.com/en-us/uwp/schemas/appxpackage/

---

**Questions?** Check Microsoft's official documentation or contact their support.

**Good luck!** Your app will be live soon! 🎉
