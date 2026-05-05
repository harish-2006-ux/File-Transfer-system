# 🧪 VaultX Testing Guide

Complete guide for testing all features of VaultX.

---

## 🎯 Quick Test (5 Minutes)

### 1. Start the Application
```bash
python app.py
```

Expected output:
```
============================================================
VaultX - Secure File Sharing System
============================================================
Server starting on http://127.0.0.1:8000
Upload folder: /path/to/server_files
============================================================
🔐 Advanced Features Enabled:
  ✅ Suspicious Login Detection
  ✅ Email Notifications
  ✅ Real-time WebSocket Updates
  ✅ Analytics Dashboard
  ✅ Advanced Search System
  ✅ Security Monitoring
============================================================
```

### 2. Create Account
1. Go to http://127.0.0.1:8000
2. Click "Sign Up"
3. Enter:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `Test123!@#`
4. Click "Create Account"
5. ✅ Should see "Account created successfully!"

### 3. Login
1. Enter username and password
2. Check terminal for OTP (if email not configured)
3. Enter OTP
4. ✅ Should redirect to dashboard

### 4. Upload File
1. Drag a file to the upload zone
2. Click "Upload & Encrypt"
3. ✅ Should see success message
4. ✅ File should appear in file list
5. ✅ Should see real-time notification (top-right)

### 5. Check Features
1. Click "Analytics" in sidebar
   - ✅ Should see statistics and charts
2. Click "Search" in sidebar
   - ✅ Should see search interface
3. Click "Security" in sidebar
   - ✅ Should see security dashboard

---

## 🔐 Authentication Testing

### Test 1: User Registration
**Steps:**
1. Go to `/signup`
2. Enter valid credentials
3. Submit form

**Expected:**
- ✅ User created in database
- ✅ Password hashed (not plain text)
- ✅ Redirect to login page
- ✅ Success message displayed

**Test Cases:**
- ✅ Valid registration
- ✅ Duplicate username (should fail)
- ✅ Empty fields (should fail)
- ✅ Invalid email format (should fail)

---

### Test 2: Login with OTP
**Steps:**
1. Go to `/login`
2. Enter valid credentials
3. Check email/terminal for OTP
4. Enter OTP on verification page

**Expected:**
- ✅ OTP sent to email (or shown in terminal)
- ✅ OTP verification page displayed
- ✅ Correct OTP allows login
- ✅ Incorrect OTP shows error
- ✅ Session created on success

**Test Cases:**
- ✅ Valid login
- ✅ Invalid password
- ✅ Invalid username
- ✅ Correct OTP
- ✅ Incorrect OTP
- ✅ Expired session

---

### Test 3: Suspicious Login Detection
**Steps:**
1. Login from one browser/IP
2. Note your IP and user agent
3. Login from different browser or use VPN
4. Check security dashboard

**Expected:**
- ✅ Suspicious login detected
- ✅ Email alert sent (if configured)
- ✅ Security event logged
- ✅ Event visible in security dashboard

**Test Cases:**
- ✅ Different IP address
- ✅ Different browser/device
- ✅ Different country (use VPN)
- ✅ Multiple failed attempts

---

### Test 4: Failed Login Lockout
**Steps:**
1. Attempt login with wrong password 5 times
2. Try to login with correct password

**Expected:**
- ✅ After 5 attempts, IP is locked
- ✅ "Too many failed attempts" message
- ✅ Cannot login even with correct password
- ✅ Lockout lasts 15 minutes
- ✅ Security events logged

---

### Test 5: Rate Limiting
**Steps:**
1. Attempt to login 6 times in 1 minute

**Expected:**
- ✅ After 5 attempts, rate limit triggered
- ✅ "Rate limit exceeded" error
- ✅ Must wait before trying again

---

## 📁 File Management Testing

### Test 6: File Upload
**Steps:**
1. Login to dashboard
2. Select a file (< 10MB)
3. Click "Upload & Encrypt"

**Expected:**
- ✅ File uploaded successfully
- ✅ File encrypted with AES-256
- ✅ Original file removed
- ✅ `.enc` file created in `server_files/`
- ✅ File appears in dashboard
- ✅ Activity logged
- ✅ Real-time notification shown
- ✅ Email notification sent (if configured)

**Test Cases:**
- ✅ Small file (< 1MB)
- ✅ Large file (5-10MB)
- ✅ File > 10MB (should fail)
- ✅ Special characters in filename
- ✅ Drag & drop upload
- ✅ Click to browse upload

---

### Test 7: File Download
**Steps:**
1. Click "Download" on an uploaded file

**Expected:**
- ✅ File decrypted temporarily
- ✅ File downloaded to browser
- ✅ Temporary decrypted file removed
- ✅ Activity logged
- ✅ Real-time notification shown

**Test Cases:**
- ✅ Download existing file
- ✅ Download non-existent file (should 404)
- ✅ Multiple simultaneous downloads

---

### Test 8: File Deletion
**Steps:**
1. Click "Delete" (X) on a file
2. Confirm deletion

**Expected:**
- ✅ Confirmation dialog shown
- ✅ File removed from storage
- ✅ File removed from dashboard
- ✅ Activity logged
- ✅ Real-time notification shown

---

### Test 9: File Search
**Steps:**
1. Upload multiple files
2. Use search box on dashboard
3. Type partial filename

**Expected:**
- ✅ Matching files shown
- ✅ Non-matching files hidden
- ✅ Case-insensitive search
- ✅ Real-time filtering

---

## 📊 Analytics Testing

### Test 10: Analytics Dashboard
**Steps:**
1. Perform various actions (upload, download, login)
2. Go to `/analytics`

**Expected:**
- ✅ Statistics cards show correct counts
- ✅ Activity timeline chart displays
- ✅ Activity distribution chart displays
- ✅ Hourly activity chart displays
- ✅ Security insights shown
- ✅ Charts are interactive

**Test Cases:**
- ✅ View with no activity
- ✅ View with some activity
- ✅ View with lots of activity
- ✅ Different time periods

---

### Test 11: Chart Data API
**Steps:**
1. Open browser console
2. Call: `fetch('/api/analytics/chart/activity_timeline')`

**Expected:**
- ✅ JSON response with chart data
- ✅ Correct data format
- ✅ Labels and datasets present

---

### Test 12: Report Generation
**Steps:**
1. Call: `fetch('/api/analytics/report?type=summary')`

**Expected:**
- ✅ JSON report generated
- ✅ User stats included
- ✅ Security insights included
- ✅ Timestamp present

---

## 🔍 Search Testing

### Test 13: File Search
**Steps:**
1. Go to `/search`
2. Select "Files" search type
3. Enter filename or partial name
4. Click "Search"

**Expected:**
- ✅ Matching files displayed
- ✅ Result count shown
- ✅ File details visible
- ✅ Timestamps shown

**Test Cases:**
- ✅ Exact filename match
- ✅ Partial filename match
- ✅ Case-insensitive search
- ✅ No results found
- ✅ Empty query

---

### Test 14: Activity Search
**Steps:**
1. Select "Activity" search type
2. Search for action type (e.g., "UPLOAD")

**Expected:**
- ✅ Matching activities displayed
- ✅ Action badges shown
- ✅ IP addresses visible
- ✅ Timestamps shown

---

### Test 15: Security Search
**Steps:**
1. Select "Security" search type
2. Search for security events

**Expected:**
- ✅ Security events displayed
- ✅ Event types shown
- ✅ IP addresses visible
- ✅ Details included

---

### Test 16: Search Suggestions
**Steps:**
1. Start typing in search box
2. Wait for suggestions

**Expected:**
- ✅ Suggestions appear after 2 characters
- ✅ Based on file history
- ✅ Clickable suggestions
- ✅ Suggestions update as you type

---

## 🔐 Security Testing

### Test 17: Security Dashboard
**Steps:**
1. Go to `/security`
2. Review displayed information

**Expected:**
- ✅ Security statistics shown
- ✅ Recent events listed
- ✅ Color-coded by severity
- ✅ Login locations displayed
- ✅ Recommendations shown

---

### Test 18: Security Events API
**Steps:**
1. Call: `fetch('/api/security/events?limit=10')`

**Expected:**
- ✅ JSON array of events
- ✅ Event details included
- ✅ Sorted by date (newest first)
- ✅ Limited to requested count

---

### Test 19: Password Strength
**Steps:**
1. Try registering with different passwords:
   - "weak"
   - "Stronger1"
   - "VeryStr0ng!"

**Expected:**
- ✅ Weak passwords accepted (but not recommended)
- ✅ Strong passwords accepted
- ✅ All passwords hashed

---

## ⚡ WebSocket Testing

### Test 20: WebSocket Connection
**Steps:**
1. Login to dashboard
2. Open browser console
3. Check for "WebSocket connected" message

**Expected:**
- ✅ WebSocket connects automatically
- ✅ User joins personal room
- ✅ Connection confirmed in console

---

### Test 21: Real-time Notifications
**Steps:**
1. Upload a file
2. Watch for notification

**Expected:**
- ✅ Toast notification appears (top-right)
- ✅ Shows file upload message
- ✅ Auto-dismisses after 5 seconds
- ✅ Slide-in animation

**Test Cases:**
- ✅ File upload notification
- ✅ File download notification
- ✅ File delete notification
- ✅ Login notification
- ✅ Suspicious activity alert

---

### Test 22: Multiple Clients
**Steps:**
1. Login in two different browsers
2. Perform action in one browser
3. Check other browser

**Expected:**
- ✅ Both clients receive notifications
- ✅ User-specific notifications only to that user
- ✅ System broadcasts to all clients

---

## 📧 Email Testing

### Test 23: Login Notification Email
**Steps:**
1. Configure email in `.env`
2. Login to account
3. Check email inbox

**Expected:**
- ✅ Email received
- ✅ HTML formatting correct
- ✅ Login details included
- ✅ Location shown
- ✅ Device info shown
- ✅ Timestamp correct

---

### Test 24: Suspicious Login Email
**Steps:**
1. Login from different IP/browser
2. Check email inbox

**Expected:**
- ✅ Alert email received
- ✅ Red/warning styling
- ✅ Reasons listed
- ✅ Recommendations included
- ✅ Action buttons present

---

### Test 25: File Upload Email
**Steps:**
1. Upload a file
2. Check email inbox

**Expected:**
- ✅ Confirmation email received
- ✅ Filename shown
- ✅ File size shown
- ✅ Encryption status shown
- ✅ Link to dashboard

---

## 🌐 Network Testing

### Test 26: Network Dashboard
**Steps:**
1. Go to `/network`

**Expected:**
- ✅ Server info displayed
- ✅ Network stats shown
- ✅ Connection logs visible
- ✅ Real-time updates

---

### Test 27: Network Stats API
**Steps:**
1. Call: `fetch('/network-stats')`

**Expected:**
- ✅ JSON response
- ✅ Bytes sent/received
- ✅ CPU usage
- ✅ Memory usage

---

## 🗄️ Database Testing

### Test 28: SQLite (Default)
**Steps:**
1. Run app with `DATABASE_TYPE=sqlite`
2. Perform actions
3. Check `users.db` and `transfers.db`

**Expected:**
- ✅ Databases created automatically
- ✅ Tables created
- ✅ Data persisted
- ✅ Queries work correctly

---

### Test 29: Supabase (Optional)
**Steps:**
1. Configure Supabase in `.env`
2. Set `DATABASE_TYPE=supabase`
3. Run app
4. Perform actions

**Expected:**
- ✅ Connects to Supabase
- ✅ Data stored in cloud
- ✅ Queries work correctly
- ✅ RLS policies enforced

---

## 🎨 UI/UX Testing

### Test 30: Responsive Design
**Steps:**
1. Open dashboard
2. Resize browser window
3. Test on mobile device

**Expected:**
- ✅ Layout adapts to screen size
- ✅ Sidebar collapses on mobile
- ✅ Mobile menu button appears
- ✅ All features accessible
- ✅ Touch-friendly buttons

---

### Test 31: Dark Theme
**Steps:**
1. Navigate through all pages

**Expected:**
- ✅ Consistent dark theme
- ✅ Good contrast
- ✅ Readable text
- ✅ Visible buttons
- ✅ Proper gradients

---

### Test 32: Animations
**Steps:**
1. Interact with various elements

**Expected:**
- ✅ Smooth transitions
- ✅ Hover effects work
- ✅ Loading animations
- ✅ Toast slide-in/out
- ✅ No janky animations

---

## 🔧 Error Handling Testing

### Test 33: Invalid Routes
**Steps:**
1. Go to `/nonexistent`

**Expected:**
- ✅ 404 error page
- ✅ Redirect to login or error page

---

### Test 34: Unauthorized Access
**Steps:**
1. Logout
2. Try to access `/analytics`

**Expected:**
- ✅ Redirect to login
- ✅ "Please log in" message

---

### Test 35: File Not Found
**Steps:**
1. Try to download non-existent file

**Expected:**
- ✅ 404 error
- ✅ Error message shown

---

### Test 36: Upload Errors
**Steps:**
1. Try to upload file > 10MB
2. Try to upload without selecting file

**Expected:**
- ✅ Error message shown
- ✅ Upload prevented
- ✅ User informed of limit

---

## 📊 Performance Testing

### Test 37: Load Time
**Steps:**
1. Clear browser cache
2. Load dashboard
3. Measure load time

**Expected:**
- ✅ Page loads in < 2 seconds
- ✅ Charts render quickly
- ✅ No blocking resources

---

### Test 38: Multiple Files
**Steps:**
1. Upload 10+ files
2. Check dashboard performance

**Expected:**
- ✅ File list renders quickly
- ✅ Search still responsive
- ✅ No lag in UI

---

### Test 39: Concurrent Users
**Steps:**
1. Login from multiple browsers
2. Perform actions simultaneously

**Expected:**
- ✅ All actions complete
- ✅ No conflicts
- ✅ Data integrity maintained
- ✅ WebSocket works for all

---

## ✅ Test Results Template

Use this template to track your testing:

```
## Test Session: [Date]

### Environment
- OS: 
- Browser: 
- Python Version: 
- Database: SQLite / Supabase

### Test Results

#### Authentication (Tests 1-5)
- [ ] Test 1: User Registration - PASS/FAIL
- [ ] Test 2: Login with OTP - PASS/FAIL
- [ ] Test 3: Suspicious Login - PASS/FAIL
- [ ] Test 4: Failed Login Lockout - PASS/FAIL
- [ ] Test 5: Rate Limiting - PASS/FAIL

#### File Management (Tests 6-9)
- [ ] Test 6: File Upload - PASS/FAIL
- [ ] Test 7: File Download - PASS/FAIL
- [ ] Test 8: File Deletion - PASS/FAIL
- [ ] Test 9: File Search - PASS/FAIL

#### Analytics (Tests 10-12)
- [ ] Test 10: Analytics Dashboard - PASS/FAIL
- [ ] Test 11: Chart Data API - PASS/FAIL
- [ ] Test 12: Report Generation - PASS/FAIL

#### Search (Tests 13-16)
- [ ] Test 13: File Search - PASS/FAIL
- [ ] Test 14: Activity Search - PASS/FAIL
- [ ] Test 15: Security Search - PASS/FAIL
- [ ] Test 16: Search Suggestions - PASS/FAIL

#### Security (Tests 17-19)
- [ ] Test 17: Security Dashboard - PASS/FAIL
- [ ] Test 18: Security Events API - PASS/FAIL
- [ ] Test 19: Password Strength - PASS/FAIL

#### WebSocket (Tests 20-22)
- [ ] Test 20: WebSocket Connection - PASS/FAIL
- [ ] Test 21: Real-time Notifications - PASS/FAIL
- [ ] Test 22: Multiple Clients - PASS/FAIL

#### Email (Tests 23-25)
- [ ] Test 23: Login Notification - PASS/FAIL/SKIP
- [ ] Test 24: Suspicious Login Email - PASS/FAIL/SKIP
- [ ] Test 25: File Upload Email - PASS/FAIL/SKIP

#### Network (Tests 26-27)
- [ ] Test 26: Network Dashboard - PASS/FAIL
- [ ] Test 27: Network Stats API - PASS/FAIL

#### Database (Tests 28-29)
- [ ] Test 28: SQLite - PASS/FAIL
- [ ] Test 29: Supabase - PASS/FAIL/SKIP

#### UI/UX (Tests 30-32)
- [ ] Test 30: Responsive Design - PASS/FAIL
- [ ] Test 31: Dark Theme - PASS/FAIL
- [ ] Test 32: Animations - PASS/FAIL

#### Error Handling (Tests 33-36)
- [ ] Test 33: Invalid Routes - PASS/FAIL
- [ ] Test 34: Unauthorized Access - PASS/FAIL
- [ ] Test 35: File Not Found - PASS/FAIL
- [ ] Test 36: Upload Errors - PASS/FAIL

#### Performance (Tests 37-39)
- [ ] Test 37: Load Time - PASS/FAIL
- [ ] Test 38: Multiple Files - PASS/FAIL
- [ ] Test 39: Concurrent Users - PASS/FAIL

### Issues Found
1. 
2. 
3. 

### Notes

```

---

## 🎉 Testing Complete!

Once all tests pass, your VaultX installation is ready for production!

---

*VaultX - Secure File Sharing System*
