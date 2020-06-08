# Busy Tone Re-Dialer
## A script to use the Google Hangouts Web UI to place calls automatically until they are answered by something other than a busy tone
### Prerequisites 
#### On VM:
- Running Windows 10
- Screen Resolution of 1024x768
- Chrome Installed and Logged In to Google
- AutoHotkey Installed

### Setup (for control from host)
- Create a shared folder between VM and host containing this project's files
- On VM Run "init.bat"
- On VM Ensure that all windows are closed
- On Host Run "host_ui.pyw"

### Setup (for isolated VM)
- Run scripts\run.bat from root project directory

### "phonenumbers" file - Can be updated in real time
```
#Lines starting with # are comments
#Each phone number needs its own line

5555551234
5555555678
#5555559012
5555553456
``` 

