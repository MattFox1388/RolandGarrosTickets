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
    def __init__(self, date_switch_delay=0.7, found_ticket_delay=2.0):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.selected_dates = set()
        self.retry_count = 0
        self.max_retries = 3
        self.date_switch_delay = date_switch_delay  # Delay when no tickets found
        self.found_ticket_delay = found_ticket_delay  # Longer delay when tickets found
        
        # Login credentials - change these as needed
        self.credentials = {
            "username": "mzorro102@gmail.com",
            "password": "g!antMint26"
        }
        
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
            # Minimal initial delay
            await asyncio.sleep(0.2)
            
            # Single quick scroll
            scroll_y = random.randint(50, 150)
            await self.page.evaluate(f"""
                window.scrollBy({{
                    top: {scroll_y},
                    left: 0,
                    behavior: 'smooth'
                }});
            """)
            await asyncio.sleep(0.1)
            
            # Single quick mouse movement
            x = random.randint(100, 800)
            y = random.randint(100, 600)
            await self.page.mouse.move(x, y, steps=5)
            
        except Exception as e:
            print(f"Human behavior simulation error (non-critical): {e}")

    async def find_available_date(self):
        """Find and click on available dates"""
        target_dates = ["FRI 30 MAY", "THU 29 MAY"]
        tickets_found = False
        
        for date_text in target_dates:
            if date_text in self.selected_dates:
                continue
                
            try:
                date_element = await self.page.wait_for_selector(
                    f"text={date_text}",
                    timeout=2000
                )
                
                if date_element:
                    await date_element.hover()
                    await asyncio.sleep(0.1)
                    
                    box = await date_element.bounding_box()
                    if box:
                        x = box['x'] + random.randint(5, max(6, int(box['width'] - 5)))
                        y = box['y'] + random.randint(5, max(6, int(box['height'] - 5)))
                        await self.page.mouse.click(x, y)
                        
                        if await self.check_collection_list():
                            self.selected_dates.add(date_text)
                            tickets_found = True
                            print(f"🎫 Found tickets! Sleeping for {self.found_ticket_delay}s...")
                            await asyncio.sleep(self.found_ticket_delay)
                            return True
                        
                        print(f"⏰ No tickets found, sleeping for {self.date_switch_delay}s...")
                        await asyncio.sleep(self.date_switch_delay)

            except Exception as e:
                print(f"Error finding date {date_text}: {e}")
                if "Page.wait_for_selector: Timeout" in str(e):
                    print("⚠️ Date selection timed out, checking for login form...")
                    try:
                        # Check for login form
                        username_input = await self.page.wait_for_selector('input[name="username"]', timeout=2000)
                        if username_input:
                            print("✅ Found login form, attempting login...")
                            await self.handle_login()
                            await asyncio.sleep(0.5)
                            return False
                    except Exception as login_error:
                        if "Timeout" in str(login_error):
                            print("⚠️ Both date and login timeouts occurred, trying back button...")
                            try:
                                back_button = await self.page.wait_for_selector('button.bt-back.small.w-inline-block', timeout=2000)
                                if back_button:
                                    await back_button.click()
                                    await asyncio.sleep(0.5)
                            except Exception as back_error:
                                print(f"❌ Error clicking back button: {back_error}")
                        else:
                            print(f"❌ Error handling login: {login_error}")
                continue
        
        self.selected_dates.clear()
        return False

    async def check_for_blocking(self):
        """Check if we've been blocked and play game over sound"""
        try:
            print("🔍 Checking for blocking text...")
            page_content = await self.page.content()
            if "vous avez été bloqué(e)" in page_content.lower():
                print("💀 GAME OVER - Vous avez été bloqué(e)! 💀")
                return True
            return False
        except Exception as e:
            print(f"Error checking for blocking: {e}")
            if "Target page, context or browser has been closed" in str(e):
                print("🔄 Browser closed unexpectedly - restarting script...")
                import sys, os
                os.execv(sys.executable, ['python'] + sys.argv)
            return False

    async def handle_ticket_purchase(self):
        """Handle ticket quantity selection and add to cart"""
        try:
            print("🎫 Starting handle_ticket_purchase method...")
            
            # Check for blocking first
            print("🔍 Checking for blocking before starting...")
            if await self.check_for_blocking():
                print("❌ Blocking detected at start of handle_ticket_purchase")
                return False
            print("✅ No blocking detected, proceeding...")
                
            # Check if we're on a ticket page with "Outside Courts"
            print("🔍 Looking for span elements on the page...")
            outside_courts_span = await self.page.query_selector('span')
            if outside_courts_span:
                print("✅ Found a span element, checking its content...")
                span_text = await outside_courts_span.text_content()
                print(f"📝 Span text content: '{span_text}'")
                
                if span_text and "outside courts" in span_text.lower():
                    print("🎫 Found 'Outside Courts' span - handling Outside Courts ticket purchase...")
                    
                    # First, find and click "Full price" option
                    print("🔍 Looking for 'Full price' h2 element...")
                    h2_elements = await self.page.query_selector_all('h2')
                    print(f"📊 Found {len(h2_elements)} h2 elements on page")
                    
                    full_price_clicked = False
                    
                    for i, h2 in enumerate(h2_elements):
                        h2_text = await h2.text_content()
                        print(f"📝 H2 element {i+1}: '{h2_text}'")
                        if h2_text and "full price" in h2_text.lower():
                            print(f"✅ Found 'Full price' h2: '{h2_text}'")
                            
                            # Get parent div and click it
                            # Find div with class containing "bt-main offre hori active-category"
                            print("🔍 Looking for full price div with active-category class...")
                            full_price_div = await self.page.query_selector('div[class*="bt-main offre hori active-category"]')
                            if full_price_div:
                                print("🖱️ Clicking 'Full price' div...")
                                await full_price_div.click()
                                await asyncio.sleep(random.uniform(0.3, 0.5))
                                print("✅ Clicked 'Full price' option")
                                full_price_clicked = True

                                # After selecting category, look for increment button and add to cart
                                print("🔍 Looking for increment button after category selection...")
                                increment_button = await self.page.query_selector('button.increment.less.button.w-button')
                                if increment_button:
                                    print("✅ Found increment button after category selection")
                                    print("🔢 Clicking increment button first time...")
                                    await increment_button.click()
                                    print("✅ First increment click completed")
                                    
                                    print("🔢 Clicking increment button second time...")
                                    await increment_button.click()
                                    print("✅ Second increment click completed")
                                    
                                else:
                                    print("⚠️ Increment button not found after category selection, continuing...")
                                
                                # Find and click add to cart button
                                print("🔍 Looking for add-to-cart button after category selection...")
                                add_to_cart_button = await self.page.query_selector('button[class*="add-to-cart"]')
                                if add_to_cart_button:
                                    print("✅ Found add-to-cart button")
                                    print("🛒 Clicking add-to-cart button...")
                                    await add_to_cart_button.click()
                                    print("✅ Add-to-cart click completed")
                                    
                                    print("🔍 Checking for blocking after add-to-cart...")
                                    if await self.check_for_blocking():
                                        print("❌ Blocking detected after add-to-cart")
                                        return False
                                    print("✅ No blocking after add-to-cart")
                                        
                                    print("🎉 Category ticket purchase completed successfully!")
                                    return True
                                else:
                                    print("❌ Add-to-cart button not found after category selection")
                                    return False
                                
                            else:
                                print("❌ Could not find parent div of 'Full price' h2")
                    
                    if not full_price_clicked:
                        print("⚠️ 'Full price' option not found, continuing anyway...")
                    
                    # Find and click increment button twice
                    print("🔍 Looking for increment button...")
                    increment_button = await self.page.query_selector('button.increment.less.button.w-button')
                    if increment_button:
                        print("✅ Found increment button")
                        print("🔢 Clicking increment button first time...")
                        await increment_button.click()
                        await asyncio.sleep(random.uniform(0.5, 1))
                        print("✅ First increment click completed")
                        
                        # Check for blocking after first click
                        print("🔍 Checking for blocking after first increment...")
                        if await self.check_for_blocking():
                            print("❌ Blocking detected after first increment")
                            return False
                        print("✅ No blocking after first increment")
                            
                        print("🔢 Clicking increment button second time...")
                        await increment_button.click()
                        await asyncio.sleep(random.uniform(0.5, 1))
                        print("✅ Second increment click completed")
                        
                        # Check for blocking after second click
                        print("🔍 Checking for blocking after second increment...")
                        if await self.check_for_blocking():
                            print("❌ Blocking detected after second increment")
                            return False
                        print("✅ No blocking after second increment")
                    else:
                        print("❌ Increment button not found")
                        return False
                    
                    # Find and click add to cart button
                    print("🔍 Looking for add-to-cart button...")
                    add_to_cart_button = await self.page.query_selector('button[class*="add-to-cart"]')
                    if add_to_cart_button:
                        print("✅ Found add-to-cart button")
                        print("🛒 Clicking add-to-cart button...")
                        await add_to_cart_button.click()
                        await asyncio.sleep(random.uniform(1, 2))
                        print("✅ Add-to-cart click completed")
                        
                        # Check for blocking after add to cart
                        print("🔍 Checking for blocking after add-to-cart...")
                        if await self.check_for_blocking():
                            print("❌ Blocking detected after add-to-cart")
                            return False
                        print("✅ No blocking after add-to-cart")
                            
                        print("🎉 Outside Courts ticket purchase completed successfully!")
                        return True
                    else:
                        print("❌ Add-to-cart button not found")
                        return False
                else:
                    print("ℹ️ Span found but doesn't contain 'Outside Courts' - looking for category grid...")
                    
                    # Look for the category grid container
                    try:
                        print("🔍 Looking for category grid container...")
                        # Find both category and polygon in parallel with minimal timeout
                        [available_category, polygon] = await asyncio.gather(
                            self.page.wait_for_selector(
                                'div.category.dropdown-np.w-dropdown-toggle:not(.disabled)',
                                timeout=1000
                            ),
                            self.page.wait_for_selector(
                                'polygon:not(.disabled)',
                                timeout=1000
                            )
                        )
                        
                        if available_category and polygon:
                            await available_category.click()
                            await asyncio.sleep(0.1)  # Minimal wait
                            await polygon.click()
                            return True
                        else:
                            print("❌ No available seats found")
                            return False
                    except Exception as grid_error:
                        print(f"❌ Error looking for category grid: {grid_error}")
                        if "Page.wait_for_selector: " in str(grid_error):
                            print("⚠️ Category grid not found, trying to go back...")
                            try:
                                back_button = await self.page.wait_for_selector('button.bt-back.small.w-inline-block', timeout=2000)
                                if back_button:
                                    await back_button.click()
                                    await asyncio.sleep(0.5)
                            except Exception as back_error:
                                print(f"❌ Error clicking back button: {back_error}")
                        return False
            else:
                print("❌ No span element found on the page")
                return False
                
        except Exception as e:
            print(f"❌ Unexpected error in handle_ticket_purchase: {e}")
            print(f"📍 Error type: {type(e).__name__}")
            import traceback
            print(f"📍 Traceback: {traceback.format_exc()}")
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
                
                # Check for "Single ticket" in h4 elements
                h4_elements = await item_div.query_selector_all('h4')
                has_single_ticket = False
                has_outside_courts = False
                
                # Get div text content before checking
                div_text = await item_div.text_content()
                
                # Check if div contains excluded text
                if "court simonne-mathieu" in div_text.lower():
                    excluded_court = "Court Simonne-Mathieu"
                    print(f"❌ Skipping - div contains '{excluded_court}'")
                    has_outside_courts = False
                else:
                    # Check for "Single ticket" in h4 elements
                    for h4 in h4_elements:
                        h4_text = await h4.text_content()
                        if h4_text and "single ticket" in h4_text.lower():
                            print(f"✅ Found 'Single ticket' h4 with text: '{h4_text}'")
                            has_single_ticket = True
                            break
                    
                    # Check if div contains excluded text
                    if "court simonne-mathieu" in div_text.lower():
                        excluded_court = "Court Simonne-Mathieu"
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
                            
                            # If link text is "Unavailable", reload page and continue
                            if "unavailable" in link_text.lower():
                                print("⚠️ Found unavailable link, reloading page...")
                                await self.page.reload(wait_until='domcontentloaded', timeout=30000)
                                await asyncio.sleep(0.5)
                                return False
                            
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
            username_input = await self.page.query_selector('input[name="username"]')
            password_input = await self.page.query_selector('input[name="password"]')
            
            if username_input and password_input:
                await username_input.fill(self.credentials["username"])
                await asyncio.sleep(0.1)
                await password_input.fill(self.credentials["password"])
                await asyncio.sleep(0.1)
                
                submit_button = await self.page.query_selector('button[type="submit"]')
                if submit_button:
                    await submit_button.click()
                    await asyncio.sleep(0.5)
                    return True
                
            return False
            
        except Exception as e:
            print(f"❌ Error handling login: {e}")
            return False

    async def run_automation(self, url: str):
        """Main automation flow"""
        try:
            if not self.browser or not self.context or not self.page:
                if not await self.setup_browser():
                    await asyncio.sleep(60)
                    return
            
            await self.page.goto(url, wait_until='domcontentloaded', timeout=30000)
            await asyncio.sleep(0.5)
            
            attempt_count = 0  # Initialize counter
            while True:
                attempt_count += 1
                try:
                    if await self.check_for_blocking():
                        break
                    
                    if await self.find_available_date():
                        await asyncio.sleep(0.5)
                    
                    if await self.check_for_blocking():
                        break
                    
                    await asyncio.sleep(0.2)
                    
                except Exception as e:
                    print(f"❌ Error in cycle {attempt_count}: {str(e)}")
                    await asyncio.sleep(5)
                    
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
    
    # Get delays from command line arguments or use defaults
    import sys
    date_switch_delay = float(sys.argv[1]) if len(sys.argv) > 1 else 0.7
    found_ticket_delay = float(sys.argv[2]) if len(sys.argv) > 2 else 2.0
    print(f"Using delays - No tickets: {date_switch_delay}s, Found tickets: {found_ticket_delay}s")
    
    roland_garros_url = "https://tickets.rolandgarros.com/"
    automation = RolandGarrosAutomation(date_switch_delay=date_switch_delay, found_ticket_delay=found_ticket_delay)
    await automation.run_automation(roland_garros_url)

if __name__ == "__main__":
    asyncio.run(main()) 