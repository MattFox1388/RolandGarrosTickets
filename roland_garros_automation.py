#!/usr/bin/env python3
"""
Roland Garros Ticket Automation Script
Using Playwright with Firefox for enhanced stealth
"""

import time
import random
import asyncio
from playwright.async_api import async_playwright, Page, Browser, BrowserContext
import json
import os

class RolandGarrosAutomation:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.selected_dates = set()
        self.retry_count = 0
        self.max_retries = 3
        
    async def download_privacy_badger(self):
        """Download Privacy Badger extension"""
        extension_url = "https://addons.mozilla.org/firefox/downloads/latest/privacy-badger17/addon-506646-latest.xpi"
        extension_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "privacy_badger.xpi")
        
        if not os.path.exists(extension_path):
            print("Downloading Privacy Badger extension...")
            try:
                import httpx
                async with httpx.AsyncClient() as client:
                    response = await client.get(extension_url)
                    response.raise_for_status()
                    with open(extension_path, 'wb') as f:
                        f.write(response.content)
                print("Privacy Badger downloaded successfully")
            except Exception as e:
                print(f"Failed to download Privacy Badger: {e}")
                return None
        
        return extension_path

    async def setup_browser(self):
        """Initialize Playwright Firefox with enhanced stealth"""
        try:
            print("Setting up Playwright Firefox...")
            
            if not self.playwright:
                print("Initializing Playwright...")
                self.playwright = await async_playwright().start()
            
            print("Launching Firefox...")
            try:
                # Launch Firefox browser with enhanced stealth
                self.browser = await self.playwright.firefox.launch(
                    headless=False,
                    firefox_user_prefs={
                        # Language and locale
                        'intl.accept_languages': 'fr-FR,fr',
                        'general.useragent.locale': 'fr-FR',
                        
                        # Disable automation detection
                        'dom.webdriver.enabled': False,
                        'marionette.enabled': False,
                        
                        # Privacy and fingerprinting
                        'privacy.resistFingerprinting': True,
                        'privacy.trackingprotection.enabled': True,
                        'dom.webaudio.enabled': False,
                        'media.peerconnection.enabled': False,
                        'media.navigator.enabled': False,
                        'media.navigator.streams.fake': True,
                        
                        # Disable various detection vectors
                        'dom.maxHardwareConcurrency': 4,
                        'toolkit.telemetry.enabled': False,
                        'datareporting.healthreport.uploadEnabled': False,
                        'datareporting.policy.dataSubmissionEnabled': False,
                        'app.shield.optoutstudies.enabled': False,
                        'browser.newtabpage.activity-stream.feeds.telemetry': False,
                        'browser.newtabpage.activity-stream.telemetry': False,
                        'browser.ping-centre.telemetry': False,
                        
                        # Network settings
                        'network.http.sendRefererHeader': 2,
                        'network.http.referer.spoofSource': True,
                        'network.captive-portal-service.enabled': False,
                        'network.connectivity-service.enabled': False,
                        
                        # Disable notifications and popups
                        'dom.webnotifications.enabled': False,
                        'dom.push.enabled': False,
                        'permissions.default.desktop-notification': 2
                    }
                )
                
                if not self.browser:
                    raise Exception("Failed to launch browser")
                
                print("Browser launched successfully")
                
                print("Creating browser context...")
                # Create context with enhanced stealth
                self.context = await self.browser.new_context(
                    viewport={'width': 1366, 'height': 768},
                    locale='fr-FR',
                    timezone_id='Europe/Paris',
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
                    extra_http_headers={
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                        'Accept-Language': 'fr-FR,fr;q=0.8,en-US;q=0.5,en;q=0.3',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'DNT': '1',
                        'Connection': 'keep-alive',
                        'Upgrade-Insecure-Requests': '1',
                        'Sec-Fetch-Dest': 'document',
                        'Sec-Fetch-Mode': 'navigate',
                        'Sec-Fetch-Site': 'none',
                        'Sec-Fetch-User': '?1'
                    }
                )
                
                if not self.context:
                    raise Exception("Failed to create browser context")
                
                # Add stealth scripts to context
                await self.context.add_init_script("""
                    // Remove webdriver property
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined,
                    });
                    
                    // Mock plugins
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [1, 2, 3, 4, 5],
                    });
                    
                    // Mock languages
                    Object.defineProperty(navigator, 'languages', {
                        get: () => ['fr-FR', 'fr', 'en-US', 'en'],
                    });
                    
                    // Override permissions
                    const originalQuery = window.navigator.permissions.query;
                    window.navigator.permissions.query = (parameters) => (
                        parameters.name === 'notifications' ?
                            Promise.resolve({ state: Notification.permission }) :
                            originalQuery(parameters)
                    );
                    
                    // Add realistic screen properties
                    Object.defineProperty(screen, 'availTop', { get: () => 23 });
                    Object.defineProperty(screen, 'availLeft', { get: () => 0 });
                    
                    // Mock chrome object for Firefox
                    window.chrome = {
                        runtime: {},
                        loadTimes: function() {},
                        csi: function() {},
                        app: {}
                    };
                """)
                
                print("Context created successfully")
                
                print("Creating new page...")
                pages = self.context.pages
                self.page = pages[0] if pages else None
                
                if not self.page:
                    print("No existing page, creating new one...")
                    self.page = await self.context.new_page()
                    
                if not self.page:
                    raise Exception("Failed to create or get page")
                
                print("Page created successfully")
                print("Setting page timeout...")
                try:
                    await self.page.set_default_timeout(30000)
                    print("Page timeout set successfully")
                except Exception as timeout_error:
                    print(f"Error setting page timeout: {str(timeout_error)}")
                    print(f"Page object: {self.page}")
                    print(f"Page type: {type(self.page)}")
                    # Try without timeout for now
                    print("Continuing without setting timeout...")
                
                print("Playwright Firefox setup complete")
                return True
                
            except Exception as e:
                print(f"Error launching Firefox: {str(e)}")
                if self.context:
                    print("Context state:", self.context)
                    await self.context.close()
                if self.browser:
                    print("Browser state:", self.browser)
                    await self.browser.close()
                raise
            
        except Exception as e:
            print(f"Error in setup_browser: {str(e)}")
            print(f"Current state - playwright: {self.playwright}, browser: {self.browser}, context: {self.context}, page: {self.page}")
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            self.browser = None
            self.context = None
            self.page = None
            self.playwright = None
            return False

    def load_storage_state(self):
        """Load stored browser state if exists"""
        storage_file = 'browser_storage.json'
        if os.path.exists(storage_file):
            with open(storage_file, 'r') as f:
                return json.load(f)
        return None
        
    async def save_storage_state(self):
        """Save browser state for future use"""
        if self.context:
            storage = await self.context.storage_state()
            with open('browser_storage.json', 'w') as f:
                json.dump(storage, f)

    async def simulate_human_behavior(self):
        """Simulate realistic human behavior"""
        try:
            # Much longer initial delay
            await asyncio.sleep(random.uniform(5, 10))
            
            # Simulate reading behavior - slow scrolling
            for _ in range(random.randint(3, 6)):
                scroll_y = random.randint(50, 150)
                await self.page.evaluate(f"""
                    window.scrollBy({{
                        top: {scroll_y},
                        left: 0,
                        behavior: 'smooth'
                    }});
                """)
                # Much longer pauses between scrolls
                await asyncio.sleep(random.uniform(2, 5))
            
            # Simulate mouse movements - very slow and natural
            for _ in range(random.randint(2, 4)):
                x = random.randint(100, 800)
                y = random.randint(100, 600)
                
                # Move mouse very slowly with many steps
                await self.page.mouse.move(x, y, steps=random.randint(20, 40))
                await asyncio.sleep(random.uniform(1, 3))
                
                # Sometimes hover over elements
                if random.random() < 0.3:
                    await asyncio.sleep(random.uniform(0.5, 1.5))
            
            # Simulate typing behavior occasionally
            if random.random() < 0.2:
                await self.page.keyboard.press('Tab')
                await asyncio.sleep(random.uniform(0.5, 1))
            
            # Random longer pause to simulate thinking
            if random.random() < 0.4:
                await asyncio.sleep(random.uniform(3, 8))
            
        except Exception as e:
            print(f"Human behavior simulation error (non-critical): {e}")

    async def find_available_date(self):
        """Find and click on available dates"""
        # Check if already in English before changing language
        try:
            # Look for the language dropdown specifically - it contains "en" or "fr" text
            lang_dropdowns = await self.page.query_selector_all('div.nav-dropdown.w-dropdown')
            for dropdown in lang_dropdowns:
                # Check if this dropdown contains language text
                dropdown_text = await dropdown.text_content()
                if dropdown_text and ('en' in dropdown_text.lower() or 'fr' in dropdown_text.lower()):
                    # Found the language dropdown, check if it's already set to English
                    if 'en' in dropdown_text.lower() and 'welcome' not in dropdown_text.lower():
                        print("✅ Already in English, skipping language change")
                        break
                    elif 'fr' in dropdown_text.lower() and 'welcome' not in dropdown_text.lower():
                        print("🌐 Currently in French, switching to English...")
                        
                        # Find the dropdown toggle within this specific dropdown
                        dropdown_toggle = await dropdown.query_selector('div.dropdown-toggle.w-dropdown-toggle')
                        if dropdown_toggle:
                            print("✅ Found language dropdown toggle - clicking...")
                            await dropdown_toggle.click()
                            await asyncio.sleep(random.uniform(0.5, 1))
                            
                            # Find and click English link within this dropdown
                            english_link = await dropdown.query_selector('a[href="/en/ticket/calendrier"]')
                            if english_link:
                                print("✅ Found 'En - English' link - clicking...")
                                await english_link.click()
                                await asyncio.sleep(random.uniform(1, 2))
                                print("✅ Language set to English")
                            else:
                                print("⚠️ 'En - English' link not found")
                        else:
                            print("⚠️ Language dropdown toggle not found")
                        break
        except Exception as e:
            print(f"⚠️ Error checking/setting language (non-critical): {e}")
        
        target_dates = ["FRI 30 MAY", "THU 29 MAY"]
        
        for date_text in target_dates:
            if date_text in self.selected_dates:
                continue
                
            print(f"Looking for date: {date_text}")
            
            # Check for blocking when looking for dates
            if await self.check_for_blocking():
                print("💀 Detected blocking while looking for dates - stopping")
                return False
            
            try:
                # Find date element
                date_element = await self.page.wait_for_selector(
                    f"text={date_text}",
                    timeout=5000
                )
                
                if date_element:
                    # Hover first
                    await date_element.hover()
                    await asyncio.sleep(random.uniform(0.3, 0.7))
                    
                    # Click with random offset
                    box = await date_element.bounding_box()
                    if box:
                        x = box['x'] + random.randint(5, max(6, int(box['width'] - 5)))
                        y = box['y'] + random.randint(5, max(6, int(box['height'] - 5)))
                        await self.page.mouse.click(x, y)
                        
                        print(f"Clicked on date: {date_text}")
                        await asyncio.sleep(random.uniform(1, 2))
                        
                        # Check for tickets after clicking
                        if await self.check_collection_list():
                            self.selected_dates.add(date_text)
                            return True
                        else:
                            print(f"No available tickets found for {date_text}, continuing...")
                        
            except Exception as e:
                print(f"Error finding date {date_text}: {e}")
                
                # Check if it's a timeout error and play game over sound
                if "timeout" in str(e).lower() or "30000ms exceeded" in str(e).lower():
                    print("💀 TIMEOUT DETECTED - Playing game over sound! 💀")
                    
                    # Play Pac-Man style game over sound (descending tones)
                    import subprocess
                    import sys
                    try:
                        if sys.platform == "win32":
                            import winsound
                            # Pac-Man style descending tones
                            winsound.Beep(659, 300)  # E
                            winsound.Beep(622, 300)  # D#
                            winsound.Beep(587, 300)  # D
                            winsound.Beep(554, 300)  # C#
                            winsound.Beep(523, 600)  # C (longer)
                        elif sys.platform == "darwin":  # macOS
                            # Generate Pac-Man style descending tones using osascript
                            tones = [659, 622, 587, 554, 523]  # E, D#, D, C#, C
                            durations = [0.3, 0.3, 0.3, 0.3, 0.6]  # Last note longer
                            
                            for tone, duration in zip(tones, durations):
                                subprocess.run([
                                    "osascript", "-e", 
                                    f'do shell script "python3 -c \\"import math, wave, struct; '
                                    f'sample_rate=22050; duration={duration}; frequency={tone}; '
                                    f'frames=int(duration*sample_rate); '
                                    f'sound=[int(32767*math.sin(2*math.pi*frequency*i/sample_rate)) for i in range(frames)]; '
                                    f'data=struct.pack(\\\"<\\\" + \\\"h\\\"*len(sound), *sound); '
                                    f'w=wave.open(\\\"/tmp/beep.wav\\\", \\\"wb\\\"); '
                                    f'w.setnchannels(1); w.setsampwidth(2); w.setframerate(sample_rate); '
                                    f'w.writeframes(data); w.close()\\" && afplay /tmp/beep.wav"'
                                ], check=False, capture_output=True)
                        elif sys.platform == "linux":
                            # Try to generate tones on Linux
                            try:
                                import math
                                import os
                                tones = [659, 622, 587, 554, 523]
                                for tone in tones:
                                    duration = 0.3 if tone != 523 else 0.6
                                    os.system(f"speaker-test -t sine -f {tone} -l 1 -s 1 >/dev/null 2>&1 & sleep {duration}; kill $!")
                            except:
                                subprocess.run(["paplay", "/usr/share/sounds/alsa/Front_Right.wav"], check=False)
                        else:
                            # For other platforms, use system sound as fallback
                            if sys.platform == "darwin":
                                subprocess.run(["afplay", "/System/Library/Sounds/Sosumi.aiff"], check=False)
                            elif sys.platform == "linux":
                                subprocess.run(["paplay", "/usr/share/sounds/alsa/Front_Right.wav"], check=False)
                    except Exception as beep_error:
                        print(f"Could not play game over sound: {beep_error}")
                        # Fallback: multiple bell characters
                        print("\a" * 10)  # ASCII bell character
                
                continue
        
        # Clear selected dates to try again
        print("Clearing selected dates to try again...")
        self.selected_dates.clear()
        return False

    async def check_for_blocking(self):
        """Check if we've been blocked and play game over sound"""
        try:
            print("🔍 Checking for blocking text...")
            page_content = await self.page.content()
            if "vous avez été bloqué(e)" in page_content.lower():
                print("💀 GAME OVER - Vous avez été bloqué(e)! 💀")
                
                # Play Pac-Man style game over sound (descending tones)
                import subprocess
                import sys
                try:
                    if sys.platform == "win32":
                        import winsound
                        # Pac-Man style descending tones
                        winsound.Beep(659, 300)  # E
                        winsound.Beep(622, 300)  # D#
                        winsound.Beep(587, 300)  # D
                        winsound.Beep(554, 300)  # C#
                        winsound.Beep(523, 600)  # C (longer)
                    elif sys.platform == "darwin":  # macOS
                        # Generate Pac-Man style descending tones using osascript
                        tones = [659, 622, 587, 554, 523]  # E, D#, D, C#, C
                        durations = [0.3, 0.3, 0.3, 0.3, 0.6]  # Last note longer
                        
                        for tone, duration in zip(tones, durations):
                            subprocess.run([
                                "osascript", "-e", 
                                f'do shell script "python3 -c \\"import math, wave, struct; '
                                f'sample_rate=22050; duration={duration}; frequency={tone}; '
                                f'frames=int(duration*sample_rate); '
                                f'sound=[int(32767*math.sin(2*math.pi*frequency*i/sample_rate)) for i in range(frames)]; '
                                f'data=struct.pack(\\\"<\\\" + \\\"h\\\"*len(sound), *sound); '
                                f'w=wave.open(\\\"/tmp/beep.wav\\\", \\\"wb\\\"); '
                                f'w.setnchannels(1); w.setsampwidth(2); w.setframerate(sample_rate); '
                                f'w.writeframes(data); w.close()\\" && afplay /tmp/beep.wav"'
                            ], check=False, capture_output=True)
                    elif sys.platform == "linux":
                        # Try to generate tones on Linux
                        try:
                            import math
                            import os
                            tones = [659, 622, 587, 554, 523]
                            for tone in tones:
                                duration = 0.3 if tone != 523 else 0.6
                                os.system(f"speaker-test -t sine -f {tone} -l 1 -s 1 >/dev/null 2>&1 & sleep {duration}; kill $!")
                        except:
                            subprocess.run(["paplay", "/usr/share/sounds/alsa/Front_Right.wav"], check=False)
                    else:
                        # For other platforms, use system sound as fallback
                        if sys.platform == "darwin":
                            subprocess.run(["afplay", "/System/Library/Sounds/Sosumi.aiff"], check=False)
                        elif sys.platform == "linux":
                            subprocess.run(["paplay", "/usr/share/sounds/alsa/Front_Right.wav"], check=False)
                except Exception as beep_error:
                    print(f"Could not play game over sound: {beep_error}")
                    # Fallback: multiple bell characters
                    print("\a" * 10)  # ASCII bell character
                
                return True
            else:
                print("✅ No blocking text detected")
            return False
        except Exception as e:
            print(f"Error checking for blocking: {e}")
            return False

    async def handle_ticket_purchase(self):
        """Handle ticket quantity selection and add to cart"""
        try:
            # Check for blocking first
            if await self.check_for_blocking():
                return False
                
            # Check if we're on a ticket page with "Outside Courts"
            outside_courts_span = await self.page.query_selector('span')
            if outside_courts_span:
                span_text = await outside_courts_span.text_content()
                if span_text and "outside courts" in span_text.lower():
                    print("🎫 Found 'Outside Courts' span - handling ticket purchase...")
                    
                    # First, find and click "Full price" option
                    print("🔍 Looking for 'Full price' h2 element...")
                    h2_elements = await self.page.query_selector_all('h2')
                    full_price_clicked = False
                    
                    for h2 in h2_elements:
                        h2_text = await h2.text_content()
                        if h2_text and "full price" in h2_text.lower():
                            print(f"✅ Found 'Full price' h2: '{h2_text}'")
                            
                            # Get parent div and click it
                            # Find div with class containing "bt-main offre hori active-category"
                            full_price_div = await self.page.query_selector('div[class*="bt-main offre hori active-category"]')
                            if full_price_div:
                                print("🖱️ Clicking 'Full price' div...")
                                await full_price_div.click()
                                await asyncio.sleep(random.uniform(0.3, 0.5))
                                print("✅ Clicked 'Full price' option")
                                full_price_clicked = True
                                
                                # Check for blocking after clicking full price
                                if await self.check_for_blocking():
                                    return False
                                break
                            else:
                                print("❌ Could not find parent div of 'Full price' h2")
                    
                    if not full_price_clicked:
                        print("⚠️ 'Full price' option not found, continuing anyway...")
                    
                    # Find and click increment button twice
                    increment_button = await self.page.query_selector('button.increment.less.button.w-button')
                    if increment_button:
                        print("🔢 Found increment button - clicking twice...")
                        await increment_button.click()
                        await asyncio.sleep(random.uniform(0.5, 1))
                        
                        # Check for blocking after first click
                        if await self.check_for_blocking():
                            return False
                            
                        await increment_button.click()
                        await asyncio.sleep(random.uniform(0.5, 1))
                        print("✅ Clicked increment button twice")
                        
                        # Check for blocking after second click
                        if await self.check_for_blocking():
                            return False
                    else:
                        print("❌ Increment button not found")
                        return False
                    
                    # Find and click add to cart button
                    add_to_cart_button = await self.page.query_selector('button[class*="add-to-cart"]')
                    if add_to_cart_button:
                        print("🛒 Found add-to-cart button - clicking...")
                        await add_to_cart_button.click()
                        await asyncio.sleep(random.uniform(1, 2))
                        print("✅ Clicked add-to-cart button")
                        
                        # Check for blocking after add to cart
                        if await self.check_for_blocking():
                            return False
                            
                        return True
                    else:
                        print("❌ Add-to-cart button not found")
                        return False
                else:
                    print("ℹ️ Span found but doesn't contain 'Outside Courts'")
                    return False
            else:
                print("ℹ️ No span element found")
                return False
                
        except Exception as e:
            print(f"❌ Error handling ticket purchase: {e}")
            return False

    async def check_collection_list(self):
        """Check the collection list for available tickets"""
        try:
            collection_list = await self.page.query_selector('div.collection-list-2.w-dyn-items[role="list"]')
            if not collection_list:
                return False
            
            # Find all collection-item-2 w-dyn-item divs
            print("Searching for collection items...")
            collection_items = await self.page.query_selector_all('div.collection-item-2.w-dyn-item')
            
            for item_div in collection_items:
                # Get the class list to check if it's available (not "off")
                class_list = await item_div.evaluate('el => el.className')
                print(f"Found collection item with classes: {class_list}")
                
                # Skip if this item is marked as "off" (unavailable)
                if "off" in class_list.lower():
                    print("Item marked as 'off' (unavailable), skipping...")
                    continue
                
                # Check if this available item contains BOTH "Single ticket" h4 AND "Outside Courts" text
                h4_elements = await item_div.query_selector_all('h4')
                has_single_ticket = False
                has_outside_courts = False
                
                # Check for "Single ticket" in h4 elements
                for h4 in h4_elements:
                    h4_text = await h4.text_content()
                    if h4_text and "single ticket" in h4_text.lower():
                        print(f"✅ Found 'Single ticket' h4 with text: '{h4_text}'")
                        has_single_ticket = True
                        break
                
                # Check for "Outside Courts" anywhere in the div
                div_text = await item_div.text_content()
                if div_text and "unlimited access to the outside courts" in div_text.lower():
                    print(f"✅ Found 'unlimited access to the outside courts' text in div")
                    
                    # Check if div contains excluded text
                    if "court philippe-chatrier" in div_text.lower() or "court simonne-mathieu" in div_text.lower():
                        excluded_court = "Court Philippe-Chatrier" if "court philippe-chatrier" in div_text.lower() else "Court Simonne-Mathieu"
                        print(f"❌ Skipping - div contains '{excluded_court}'")
                        has_outside_courts = False
                    else:
                        # DEBUG: Print the entire div structure
                        print("🔍 DEBUG: Printing parent div and all nested elements:")
                        div_html = await item_div.evaluate('el => el.outerHTML')
                        print("=" * 80)
                        print(div_html)
                        print("=" * 80)
                        print(f"Full div text content: '{div_text}'")
                        print("=" * 80)
                        
                        has_outside_courts = True
                
                if has_single_ticket and has_outside_courts:
                    print(f"🎉 AVAILABLE SINGLE TICKET + OUTSIDE COURTS FOUND! 🎉")
                    print(f"Collection item classes: {class_list}")
                    
                    # Make audible beep sound
                    import subprocess
                    import sys
                    try:
                        if sys.platform == "darwin":  # macOS
                            subprocess.run(["afplay", "/System/Library/Sounds/Glass.aiff"], check=False)
                        elif sys.platform == "linux":
                            subprocess.run(["paplay", "/usr/share/sounds/alsa/Front_Left.wav"], check=False)
                        elif sys.platform == "win32":
                            import winsound
                            winsound.Beep(1000, 1000)  # 1000Hz for 1 second
                    except Exception as beep_error:
                        print(f"Could not play beep sound: {beep_error}")
                        # Fallback: print bell character
                        print("\a" * 5)  # ASCII bell character
                    
                    # Find the first <a> link within this collection item (recursively)
                    try:
                        print("Searching for <a> link within the collection item...")
                        link = await item_div.evaluate_handle('''
                            (element) => {
                                // Recursively search for the first <a> tag
                                function findFirstLink(node) {
                                    if (node.tagName === 'A') {
                                        return node;
                                    }
                                    for (let child of node.children) {
                                        const link = findFirstLink(child);
                                        if (link) return link;
                                    }
                                    return null;
                                }
                                return findFirstLink(element);
                            }
                        ''')
                        
                        if link:
                            # Get link details for logging
                            link_href = await link.evaluate('el => el.href')
                            link_text = await link.evaluate('el => el.textContent.trim()')
                            print(f"Found link: '{link_text}' -> {link_href}")
                            
                            # Click the link
                            await link.click()
                            print("✅ Successfully clicked on the ticket link!")
                            await asyncio.sleep(random.uniform(0, 1))
                            
                            # Wait for page to load and handle ticket purchase
                            # Wait for either ticket quantity selector or blocking text to appear
                            try:
                                await self.page.wait_for_selector('button.increment.less.button.w-button, div.blocking-text', timeout=5000)
                            except:
                                print("⚠️ Timeout waiting for ticket page elements")
                            if await self.handle_ticket_purchase():
                                print("🎉 Successfully handled ticket purchase!")
                            
                            return True
                        else:
                            print("❌ No <a> link found within the collection item")
                            # Fallback: try clicking the div itself
                            print("Trying to click the collection item as fallback...")
                            await item_div.click()
                            print("Clicked on collection item (fallback)")
                            await asyncio.sleep(random.uniform(0, 1))
                            
                            # Wait for page to load and handle ticket purchase
                            try:
                                await self.page.wait_for_selector('button.increment.less.button.w-button, div.blocking-text', timeout=5000)
                            except:
                                print("⚠️ Timeout waiting for ticket page elements")
                           
                            if await self.handle_ticket_purchase():
                                print("🎉 Successfully handled ticket purchase!")
                            
                            return True
                            
                    except Exception as click_error:
                        print(f"❌ Error finding/clicking link: {click_error}")
                        # Final fallback: try clicking the div
                        try:
                            await item_div.click()
                            print("Clicked on collection item (final fallback)")
                            await asyncio.sleep(random.uniform(0, 0.3))
                            
                            # Wait for page to load and handle ticket purchase
                            try:
                                await self.page.wait_for_selector('button.increment.less.button.w-button, div.blocking-text', timeout=5000)
                            except:
                                print("⚠️ Timeout waiting for ticket page elements")
                            
                            if await self.handle_ticket_purchase():
                                print("🎉 Successfully handled ticket purchase!")
                            
                            return True
                        except Exception as final_error:
                            print(f"❌ Final fallback also failed: {final_error}")
                            continue  # Try next item
                else:
                    print("Available item found but no 'Single ticket' h4 inside")
            
            print("No available single tickets found")
            return False
            
        except Exception as e:
            print(f"Error checking collection list: {e}")
            return False

    async def handle_login(self):
        """Handle automatic login if login form is detected"""
        try:
            # Check if login form is present
            username_input = await self.page.query_selector('input[name="username"]')
            password_input = await self.page.query_selector('input[name="password"]')
            
            if username_input and password_input:
                print("🔐 Login form detected - filling credentials...")
                
                # Fill username
                await username_input.fill("mzorro102@gmail.com")
                print("✅ Username filled")
                await asyncio.sleep(random.uniform(0.5, 1))
                
                # Fill password
                await password_input.fill("g!antMint26")
                print("✅ Password filled")
                await asyncio.sleep(random.uniform(0.5, 1))
                
                # Find and click submit button
                submit_button = await self.page.query_selector('button[type="submit"]')
                if submit_button:
                    await submit_button.click()
                    print("✅ Login form submitted")
                    await asyncio.sleep(random.uniform(2, 4))
                    return True
                else:
                    print("❌ Submit button not found")
                    return False
            
            return False
            
        except Exception as e:
            print(f"❌ Error handling login: {e}")
            return False

    async def run_automation(self, url: str):
        """Main automation flow - runs indefinitely"""
        attempt_count = 0
        
        try:
            # Initial setup and navigation
            print(f"\n🔄 Setting up browser and initial navigation...")
            
            # Setup browser if needed
            if not self.browser or not self.context or not self.page:
                if not await self.setup_browser():
                    print("Browser setup failed, retrying in 10 minutes...")
                    await asyncio.sleep(600)
                    return
            
            # Navigate to the page once
            print(f"Navigating to: {url}")
            try:
                await self.page.goto(url, wait_until='domcontentloaded', timeout=60000)
                await asyncio.sleep(random.uniform(5, 10))
            except Exception as nav_error:
                print(f"Navigation error: {nav_error}")
                await asyncio.sleep(300)
                return
            
            # Check for and handle login form
            print("🔍 Checking for login form...")
            try:
                login_form = await self.page.query_selector('form[action*="login"]')
                if login_form:
                    print("✅ Login form found")
                    if await self.handle_login():
                        print("🎉 Login successful, waiting for page to load...")
                        await asyncio.sleep(random.uniform(3, 5))
                else:
                    print("ℹ️ No login form found")
            except Exception as login_check_error:
                print(f"⚠️ Error checking for login form (page may have redirected): {login_check_error}")
                print("Continuing with automation...")
                await asyncio.sleep(2)
            
            # Check page content once
            page_content = await self.page.content()
            page_url = self.page.url
            
            # Check for slider/CAPTCHA verification
            captcha_indicators = [
                "slider",
                "captcha",
                "verification",
                "prove you are human",
                "drag the slider",
                "slide to verify",
                "security check",
                "bot detection",
                "pourquoi cette vérification ? quelque chose dans le comportement du navigateur nous a intrigué"
            ]
            
            is_captcha_page = any(indicator in page_content.lower() for indicator in captcha_indicators)
            
            if is_captcha_page:
                print("🤖 CAPTCHA/Slider verification detected - skipping human behavior simulation")
                print("Please solve the verification manually...")
                # Wait for user to solve CAPTCHA
                await asyncio.sleep(30)
                
                # Check for login form after CAPTCHA completion
                print("🔍 Checking for login form after CAPTCHA...")
                try:
                    login_form_after_captcha = await self.page.query_selector('form[action*="login"]')
                    if login_form_after_captcha:
                        print("✅ Login form found after CAPTCHA")
                        if await self.handle_login():
                            print("🎉 Login successful after CAPTCHA, waiting for page to load...")
                            await asyncio.sleep(random.uniform(3, 5))
                    else:
                        print("ℹ️ No login form found after CAPTCHA")
                except Exception as captcha_login_error:
                    print(f"⚠️ Error checking for login form after CAPTCHA: {captcha_login_error}")
                    print("Continuing with automation...")
                    await asyncio.sleep(2)
            else:
                # Only simulate human behavior if NOT on CAPTCHA page
                for i in range(random.randint(2, 4)):
                    print(f"Simulating human behavior {i+1}...")
                    await self.simulate_human_behavior()
                    await asyncio.sleep(random.uniform(2, 5))
            
            # Check for actual blocking pages
            blocking_indicators = [
                "vous avez été bloqué",
                "you have been blocked", 
                "access denied",
                "unusual activity"
            ]
            
            # Check for success indicators
            success_indicators = [
                "roland-garros mobile application",
                "spectators must now present",
                "tickets via the",
                "billets",
                "spectateurs"
            ]
            
            # Check if we're blocked
            if any(indicator in page_content.lower() for indicator in blocking_indicators):
                print(f"\n🚫 Blocking detected on page: {page_url}")
                print("Waiting 30-60 minutes before retrying...")
                await self.save_storage_state()
                await asyncio.sleep(random.uniform(1800, 3600))
                return
            
            # Check if we're on a success page
            if any(indicator in page_content.lower() for indicator in success_indicators):
                print("✅ SUCCESS! Reached the ticket application page!")
                await self.save_storage_state()
            
            # Now continuously cycle through dates without re-navigating
            while True:  # Run indefinitely
                attempt_count += 1
                try:
                    print(f"\n🎫 Ticket search cycle {attempt_count}")
                    
                    # Check for blocking before searching
                    if await self.check_for_blocking():
                        print("💀 Detected blocking - stopping automation")
                        break
                    
                    # Always try to find tickets (this will cycle through dates)
                    if await self.find_available_date():
                        print("🎉 Found and clicked on available ticket!")
                        # Don't break - keep monitoring in case more become available
                        await asyncio.sleep(10)  # Wait a bit longer after finding a ticket
                    
                    # Check for blocking after ticket search
                    if await self.check_for_blocking():
                        print("💀 Detected blocking after ticket search - stopping automation")
                        break
                    
                    # Short wait before next cycle
                    wait_time = random.uniform(1, 3)
                    print(f"⏰ Waiting {wait_time:.1f} seconds before next cycle...")
                    await asyncio.sleep(wait_time)
                    
                except Exception as e:
                    print(f"❌ Error in cycle {attempt_count}: {str(e)}")
                    print("Waiting 30 seconds before retrying...")
                    await asyncio.sleep(30)
                    
        except KeyboardInterrupt:
            print("\n🛑 Automation stopped by user")
        finally:
            # Cleanup
            print("🧹 Cleaning up resources...")
            if self.context:
                await self.save_storage_state()
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            print("✅ Cleanup complete")

async def main():
    """Main async function"""
    print("🎾 Roland Garros Ticket Automation Starting...")
    
    # Test the alert sound so user knows what to expect
    print("Testing alert sound...")
    import subprocess
    import sys
    try:
        if sys.platform == "darwin":  # macOS
            subprocess.run(["afplay", "/System/Library/Sounds/Glass.aiff"], check=False)
        elif sys.platform == "linux":
            subprocess.run(["paplay", "/usr/share/sounds/alsa/Front_Left.wav"], check=False)
        elif sys.platform == "win32":
            import winsound
            winsound.Beep(1000, 1000)  # 1000Hz for 1 second
    except Exception as beep_error:
        print(f"Could not play test sound: {beep_error}")
        # Fallback: print bell character
        print("\a" * 3)  # ASCII bell character
    
    print("That's the sound you'll hear when an available ticket is found! 🔊")
    await asyncio.sleep(2)
    
    roland_garros_url = "https://tickets.rolandgarros.com/"
    
    automation = RolandGarrosAutomation()
    await automation.run_automation(roland_garros_url)

if __name__ == "__main__":
    asyncio.run(main()) 