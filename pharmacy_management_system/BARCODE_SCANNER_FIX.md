# Barcode Scanner Camera Fix - Quick Guide

## What Was Fixed

The barcode scanner camera feature has been improved with:

1. ✅ **Better Error Messages** - Clear feedback when camera fails
2. ✅ **Permission Detection** - Detects when camera permission is denied
3. ✅ **Browser Compatibility Check** - Warns if browser doesn't support camera
4. ✅ **Camera Already In Use Detection** - Detects if another app is using the camera
5. ✅ **HTTPS Warning** - Alerts if security settings block camera

## Common Issues & Solutions

### 🔴 Issue: "Camera permission denied"

**Solution:**
1. Look for the camera icon in your browser's address bar (usually left side)
2. Click it and select "Allow" or "Always allow"
3. Refresh the page
4. Try starting the camera again

**Alternative:**
- Chrome: Settings → Privacy and security → Site Settings → Camera
- Firefox: Settings → Privacy & Security → Permissions → Camera
- Edge: Settings → Cookies and site permissions → Camera

---

### 🔴 Issue: "No cameras found"

**Solution:**
1. Connect a webcam to your computer
2. Make sure the webcam is not being used by another application (Zoom, Teams, etc.)
3. Refresh the page

---

### 🔴 Issue: "Camera is already in use"

**Solution:**
1. Close any other applications using the camera (Zoom, Teams, Skype, etc.)
2. Close other browser tabs that might be using the camera
3. Try again

---

### 🔴 Issue: Camera only works on HTTPS (not HTTP)

**Explanation:**
Modern browsers require HTTPS for camera access for security reasons.

**Solution:**
- For development: Use `localhost` (already secure)
- For production: Deploy with HTTPS/SSL certificate
- For local network testing: Use Chrome with flag:
  ```
  chrome.exe --unsafely-treat-insecure-origin-as-secure="http://YOUR-IP:5173"
  ```

---

### 🔴 Issue: "Camera access not supported in this browser"

**Solution:**
- Use a modern browser: Chrome, Firefox, Edge, Safari (iOS)
- Update your browser to the latest version
- Avoid Internet Explorer (not supported)

---

## How to Use Barcode Scanner

### Option 1: USB Scanner (Recommended)
1. Click "USB Scanner / Manual Input"
2. Connect your USB barcode scanner
3. Click in the input field
4. Scan the barcode
5. Medicine details appear automatically

### Option 2: Webcam Scanner
1. Click "Webcam Scanner"
2. Select your camera from dropdown
3. Click "Start Camera"
4. Allow camera permission if prompted
5. Hold barcode in front of camera
6. Scanner automatically detects and searches

### Option 3: Manual Entry
1. Click "USB Scanner / Manual Input"
2. Type the barcode number
3. Press Enter or click Search

---

## Supported Barcode Formats

The scanner supports these formats:
- ✅ CODE 128 (most common)
- ✅ CODE 39
- ✅ EAN-13
- ✅ EAN-8
- ✅ UPC-A
- ✅ UPC-E
- ✅ QR Codes

---

## Testing the Scanner

### Test with USB Scanner:
1. Connect USB scanner
2. Open Barcode Scanner page
3. Click in input field
4. Scan any medicine barcode
5. Should instantly display results

### Test with Webcam:
1. Go to Barcode Scanner page
2. Click "Webcam Scanner"
3. Select camera
4. Click "Start Camera"
5. Hold a barcode in front of camera
6. Should scan within 1-2 seconds

### Test with Manual Input:
1. Type any medicine barcode (e.g., `MED001`)
2. Press Enter
3. Should display medicine details

---

## Browser Console Debugging

If camera still doesn't work, check browser console (F12):

1. Open DevTools (press F12)
2. Go to Console tab
3. Look for errors related to:
   - `getUserMedia`
   - `NotAllowedError`
   - `NotFoundError`
   - `Camera`

Common console errors and meanings:
- `NotAllowedError` → Permission denied
- `NotFoundError` → No camera detected
- `NotReadableError` → Camera in use by another app
- `SecurityError` → HTTPS required

---

## Mobile Device Usage

### iOS (iPhone/iPad):
- ✅ Works in Safari, Chrome
- Requires iOS 11+
- Must use HTTPS in production
- Camera permission: Settings → Safari → Camera

### Android:
- ✅ Works in Chrome, Firefox
- Requires Android 5+
- Camera permission: Settings → Apps → Browser → Permissions

---

## Performance Tips

1. **Good Lighting**: Ensure barcode is well-lit
2. **Steady Hand**: Hold barcode steady for 1-2 seconds
3. **Distance**: Hold barcode 6-12 inches from camera
4. **Clean Lens**: Make sure camera lens is clean
5. **Print Quality**: High-quality printed barcodes work best

---

## Still Not Working?

If camera still doesn't work after trying everything:

1. **Check browser version**: Must be recent (Chrome 53+, Firefox 49+, Safari 11+)
2. **Check camera hardware**: Try camera in other applications
3. **Try different browser**: Test in Chrome if using Firefox, vice versa
4. **Check OS permissions**: Some OS restrict camera access
5. **Use USB scanner instead**: More reliable for high-volume scanning

---

## Technical Details

**Frontend:**
- Using `html5-qrcode` library v2.3.8
- Camera access via WebRTC API
- Automatic barcode format detection

**API Endpoints:**
- Medicine lookup: `GET /api/medicines/barcode/:barcode`
- Batch lookup: `GET /api/inventory/barcode/:barcode`

**Security:**
- Camera access requires user permission
- HTTPS enforced by browsers
- No barcode images stored on server
