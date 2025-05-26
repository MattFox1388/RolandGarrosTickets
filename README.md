# Roland Garros Ticket Automation

An automated ticket booking script for Roland Garros that uses Selenium with Firefox and includes comprehensive anti-detection measures.

## Features

- **Anti-Detection Measures**: Implements multiple techniques to avoid bot detection
- **Firefox with Privacy Badger**: Uses Firefox browser with Privacy Badger extension for enhanced privacy
- **Private Browsing**: Runs in private window mode
- **Human-like Behavior**: Random delays and realistic interaction patterns
- **Proxy Compatible**: Works with VPN applications like Proton VPN

## Anti-Detection Features

- Disables `navigator.webdriver` property
- Custom user agent string
- Privacy-focused Firefox preferences
- Random window sizes
- Human-like delays between actions
- Privacy Badger extension for tracker blocking
- Private browsing mode
- Disabled automation indicators

## Prerequisites

1. **Python 3.7+**
2. **Firefox Browser** (latest version recommended)
3. **Proton VPN** (or your preferred VPN) running
4. **Internet connection**

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Start your VPN** (Proton VPN or preferred VPN service)

2. **Run the script**:
   ```bash
   python roland_garros_automation.py
   ```

3. **Manual Login Phase**:
   - The script will open Firefox and navigate to Roland Garros ticket site
   - **You must manually log in** and navigate to the ticket selection page
   - The automation will wait for the trigger text to appear

4. **Automation Phase**:
   - Once the text "All spectators must now present their tickets via the Roland-Garros mobile application." appears, automation starts
   - The script will automatically:
     - Look for "FRI 30 MAY" or "SAT 31 MAY" dates
     - Check for available tickets (divs without "off" class)
     - Click on available ticket links
     - Use random delays to mimic human behavior

5. **Manual Purchase Phase**:
   - When tickets are found, the browser stays open
   - **You manually complete the purchase process**
   - Press Ctrl+C to close the browser when done

## How It Works

### User Flow

1. **Navigation**: Script opens Roland Garros ticket site
2. **Manual Login**: User logs in manually
3. **Trigger Detection**: Waits for specific text to appear
4. **Date Selection**: Automatically clicks on available dates
5. **Ticket Search**: Checks collection lists for available tickets
6. **Manual Purchase**: User completes purchase manually

### Anti-Detection Strategy

The script implements multiple layers of protection:

- **Browser Fingerprinting**: Randomized window sizes and realistic user agent
- **Behavioral Mimicking**: Random delays between 0.2-1 seconds
- **Privacy Extensions**: Privacy Badger blocks trackers
- **Firefox Preferences**: Disabled automation indicators
- **Private Browsing**: No persistent data storage

## Configuration

### Adjusting Delays

Modify delays in the script:
```python
def human_like_delay(self, min_delay=0.2, max_delay=1.0):
    # Adjust these values as needed
```

### Changing Target Dates

Update the target dates:
```python
target_dates = ["FRI 30 MAY", "SAT 31 MAY"]
# Add or modify dates as needed
```

### VPN Considerations

- Ensure your VPN is running before starting the script
- The script works with any VPN service (Proton VPN, ExpressVPN, etc.)
- Consider using servers in France for better performance

## Troubleshooting

### Common Issues

1. **Geckodriver not found**:
   - The script automatically downloads geckodriver
   - Ensure you have internet connection

2. **Privacy Badger download fails**:
   - Check internet connection
   - The script will continue without the extension

3. **Trigger text not found**:
   - Ensure you're on the correct page
   - The text must be exactly: "All spectators must now present their tickets via the Roland-Garros mobile application."

4. **No tickets found**:
   - The script will try multiple times
   - Tickets may genuinely be unavailable

### Debug Mode

Add debug prints by modifying the script:
```python
# Add more verbose logging
print(f"Current URL: {self.driver.current_url}")
print(f"Page title: {self.driver.title}")
```

## Important Notes

### Legal and Ethical Considerations

- This script is for educational purposes
- Ensure compliance with Roland Garros terms of service
- Use responsibly and don't overload their servers
- Respect ticket purchase limits

### Limitations

- Requires manual login (intentional for security)
- Requires manual purchase completion
- May need updates if website structure changes
- Success depends on ticket availability

## Security Features

- **No credential storage**: Login is always manual
- **Private browsing**: No persistent data
- **VPN compatible**: Works with any VPN service
- **Extension support**: Privacy Badger for tracker blocking

## Support

If you encounter issues:

1. Check that Firefox is updated
2. Verify VPN is running
3. Ensure you're on the correct Roland Garros page
4. Check console output for error messages

## Disclaimer

This tool is provided as-is for educational purposes. Users are responsible for:
- Complying with website terms of service
- Using the tool ethically and legally
- Not overwhelming servers with requests
- Respecting ticket purchase policies

The authors are not responsible for any misuse or consequences of using this tool. 