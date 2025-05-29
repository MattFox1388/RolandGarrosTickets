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
    def __init__(self, date_switch_delay=1.8, found_ticket_delay=1.8):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.selected_dates = set()
        self.retry_count = 0
        self.max_retries = 3
        self.date_switch_delay = date_switch_delay
        self.found_ticket_delay = found_ticket_delay
        self.ticket_found = False
        self.processing_ticket = False
        self.date_processing_lock = False
        
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

    async def _wait_for_ticket_processing(self):
        """Wait for any ongoing ticket processing to complete"""
        if self.processing_ticket:
            print("🚨 TICKET PROCESSING IN PROGRESS - BLOCKING DATE SWITCHING!")
            while self.processing_ticket:
                print("⏳ Waiting for ticket processing to complete...")
                await asyncio.sleep(1)
            print("✅ Ticket processing completed, resuming date switching")
            return True
        return False

    async def _check_ticket_found(self):
        """Check if a ticket has been found"""
        if self.ticket_found:
            print("🚨 Ticket already found - not switching dates!")
            await asyncio.sleep(2)
            return True
        return False

    async def _try_select_date(self, date_text):
        """Try to select a specific date and process tickets"""
        try:
            print(f"🗓️ SWITCHING TO DATE: {date_text}")
            
            # Final checks before clicking
            if self.ticket_found or self.processing_ticket:
                print(f"🚨 TICKET FOUND/PROCESSING - ABORTING DATE SWITCH TO {date_text}!")
                return True
            
            # Reduce timeout and use faster selector
            date_element = await self.page.wait_for_selector(
                f"text={date_text}",
                timeout=1000  # Reduced from 2000
            )
            
            if not date_element:
                return False
                
            print(f"✅ Found date element for {date_text}")
            
            # Click the date with random offset
            box = await date_element.bounding_box()
            if box:
                x = box['x'] + random.randint(5, max(6, int(box['width'] - 5)))
                y = box['y'] + random.randint(5, max(6, int(box['height'] - 5)))
                await self.page.mouse.click(x, y)
                print(f"✅ Successfully clicked on {date_text}")
                await asyncio.sleep(0.1)  # Reduced from 0.3
                return True
            return False
            
        except Exception as e:
            print(f"❌ Error selecting date {date_text}: {e}")
            return False

    async def _process_date_tickets(self, date_text):
        """Process tickets for a selected date"""
        # Final check before processing
        if self.ticket_found:
            print(f"🚨 TICKET ALREADY FOUND - ABORTING PROCESSING FOR {date_text}!")
            return True
            
        # Set processing flag
        print(f"🔒 SETTING PROCESSING FLAG - BLOCKING OTHER DATE SWITCHES")
        self.processing_ticket = True
        
        # Check for tickets
        print(f"🔍 CHECKING FOR TICKETS ON {date_text}...")
        ticket_result = await self.check_collection_list()
        print(f"📊 Ticket check result for {date_text}: {ticket_result}")
        
        # Handle ticket found during check
        if self.ticket_found:
            print(f"🚨 TICKET FOUND DURING CHECK - IMMEDIATELY STOPPING ALL DATE PROCESSING!")
            return True
            
        if ticket_result:
            print(f"✅ Successfully processed tickets for {date_text}")
            self.selected_dates.add(date_text)
            self.processing_ticket = False
            return True
            
        # Final check for found ticket
        if self.ticket_found:
            print(f"🚨 Ticket found for {date_text} but processing may have failed - STILL STOPPING DATE SWITCHING!")
            return True
            
        # Clear processing flag and wait
        print(f"🔓 CLEARING PROCESSING FLAG - NO TICKETS FOUND ON {date_text}")
        self.processing_ticket = False
        print(f"⏰ No tickets found for {date_text}, sleeping for {self.date_switch_delay}s...")
        await asyncio.sleep(self.date_switch_delay)
        return False

    async def _handle_date_error(self, date_text, error):
        """Handle errors during date processing"""
        print(f"❌ Error finding date {date_text}: {error}")
        print(f"🔄 ERROR WITH {date_text} - MOVING TO NEXT DATE")
        
        if "Page.wait_for_selector: Timeout" in str(error):
            print("⚠️ Date selection timed out, checking for login form...")
            try:
                username_input = await self.page.wait_for_selector('input[name="username"]', timeout=2000)
                if username_input:
                    print("✅ Found login form, attempting login...")
                    await self.handle_login()
                    await asyncio.sleep(0.5)
                    return False
            except Exception as login_error:
                if "Timeout" in str(login_error):
                    await self._try_back_button()
                else:
                    print(f"❌ Error handling login: {login_error}")
        return False

    async def find_available_date(self):
        """Find and process available dates"""
        # Check global lock
        if self.date_processing_lock:
            print("🔒 DATE PROCESSING ALREADY IN PROGRESS - BLOCKING THIS CALL!")
            while self.date_processing_lock:
                print("⏳ Waiting for other date processing to complete...")
                await asyncio.sleep(1)
            print("✅ Other date processing completed")
            return False

        # Set global lock
        print("🔒 SETTING GLOBAL DATE PROCESSING LOCK")
        self.date_processing_lock = True
        
        try:
            target_dates = [ "FRI 30 MAY"]
            # target_dates = [ "THU 29 MAY"]
            
            # Wait for any ongoing ticket processing
            await self._wait_for_ticket_processing()
            
            # Check if ticket already found
            if await self._check_ticket_found():
                self.date_processing_lock = False
                return True
            
            for date_text in target_dates:
                # Skip already tried dates
                if date_text in self.selected_dates:
                    print(f"⏭️ Skipping {date_text} - already tried this date")
                    continue
                
                try:
                    # Try to select the date
                    if not await self._try_select_date(date_text):
                        continue
                        
                    # Process tickets for selected date
                    if await self._process_date_tickets(date_text):
                        self.date_processing_lock = False
                        return True
                        
                except Exception as e:
                    await self._handle_date_error(date_text, e)
                continue
        
            # Reset for next cycle
            self.selected_dates.clear()
            return False
            
        except Exception as e:
            print(f"Error finding date: {e}")
            return False
        finally:
            # Always clear the lock
            print("🔓 CLEARING GLOBAL DATE PROCESSING LOCK")
            self.date_processing_lock = False

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

    async def handle_outside_courts_purchase(self):
        """Handle purchase flow specifically for Outside Courts tickets"""
        try:
            # First, find and click "Full price" option
            print("🔍 Looking for 'Full price' h2 element...")
            if not await self._select_full_price_option():
                print("⚠️ 'Full price' option not found, continuing anyway...")

            # Handle quantity and cart
            return await self._handle_quantity_and_cart()
            
        except Exception as e:
            print(f"❌ Error in handle_outside_courts_purchase: {e}")
            return False

    async def _select_full_price_option(self):
        """Select the 'Full price' ticket option if available"""
        h2_elements = await self.page.query_selector_all('h2')
        print(f"📊 Found {len(h2_elements)} h2 elements on page")
        
        for h2 in h2_elements:
            h2_text = await h2.text_content()
            if h2_text and "full price" in h2_text.lower():
                print(f"✅ Found 'Full price' h2: '{h2_text}'")
                full_price_div = await self.page.query_selector('div[class*="bt-main offre hori active-category"]')
                if full_price_div:
                    await full_price_div.click()
                    await asyncio.sleep(random.uniform(0.3, 0.5))
                    print("✅ Clicked 'Full price' option")
                    return True
        return False

    async def _handle_quantity_and_cart(self):
        """Handle ticket quantity selection and add to cart"""
        try:
            # Find and click increment button
            increment_button = await self.page.wait_for_selector('button.increment.less.button.w-button', timeout=1000)
            if increment_button:
                print("✅ Found increment button")
                await increment_button.click()
                await asyncio.sleep(0.3)  # Reduced from 0.5-1.0
                print("✅ Increment click completed")
                
                if await self.check_for_blocking():
                    return False
            else:
                print("❌ Increment button not found")
                return False
            
            # Add to cart
            add_to_cart_button = await self.page.wait_for_selector('button[class*="add-to-cart"]', timeout=1000)
            if add_to_cart_button:
                print("🛒 Clicking add-to-cart button...")
                await add_to_cart_button.click()
                await asyncio.sleep(0.5)  # Reduced from 1-2
                
                if await self.check_for_blocking():
                    return False
                    
                print("🎉 Ticket added to cart successfully!")
                return True
            else:
                print("❌ Add-to-cart button not found")
                return False
                
        except Exception as e:
            print(f"❌ Error in handle_quantity_and_cart: {e}")
            return False

    async def _handle_category_grid_purchase(self):
        """Handle purchase flow for category grid tickets"""
        try:
            print("🔍 Looking for category grid container...")
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
                await asyncio.sleep(0.1)
                await polygon.click()
                return True
            return False
                
        except Exception as e:
            print(f"❌ Error in handle_category_grid_purchase: {e}")
            if "Page.wait_for_selector: " in str(e):
                await self._try_back_button()
            return False

    async def _try_back_button(self):
        """Try to click the back button when needed"""
        try:
            back_button = await self.page.wait_for_selector('button.bt-back.small.w-inline-block', timeout=2000)
            if back_button:
                await back_button.click()
                await asyncio.sleep(0.5)
        except Exception as back_error:
            print(f"❌ Error clicking back button: {back_error}")

    async def handle_ticket_purchase(self):
        """Main entry point for ticket purchase handling"""
        try:
            print("🎫 Starting ticket purchase process...")
            
            if await self.check_for_blocking():
                return False
            
            # Check if we're on an Outside Courts ticket page
            outside_courts_span = await self.page.query_selector('span')
            if not outside_courts_span:
                print("❌ No span element found on the page")
                return False
                
            span_text = await outside_courts_span.text_content()
            print(f"📝 Span text content: '{span_text}'")
            
            if span_text and "outside courts" in span_text.lower():
                print("🎫 Found 'Outside Courts' span - handling Outside Courts ticket...")
                return await self.handle_outside_courts_purchase()
            else:
                print("ℹ️ Not Outside Courts - handling category grid purchase...")
                return await self._handle_category_grid_purchase()
                
        except Exception as e:
            print(f"❌ Unexpected error in handle_ticket_purchase: {e}")
            print(f"📍 Error type: {type(e).__name__}")
            import traceback
            print(f"📍 Traceback: {traceback.format_exc()}")
            return False

    async def _is_valid_ticket(self, item_div):
        """Check if a collection item is a valid ticket (available, single ticket, outside courts)"""
        try:
            # Check if item is available (not "off")
            class_list = await item_div.evaluate('el => el.className')
            if "off" in class_list.lower():
                return False
                
            # Get div text content
            div_text = await item_div.text_content()
            print(f"📝 Div text content: '{div_text}'")
            
            # Skip Simonne-Mathieu court
            # if "court simonne-mathieu" in div_text.lower():
            #     print("❌ Skipping - div contains 'Court Simonne-Mathieu'")
            #     return False
                
            if "night session" in div_text.lower():
                print("❌ Skipping - div contains 'Night Session'") 
                return False
                
            # Check for "Single ticket" in h4 elements
            h4_elements = await item_div.query_selector_all('h4')
            has_single_ticket = False
            for h4 in h4_elements:
                h4_text = await h4.text_content()
                if h4_text and "single ticket" in h4_text.lower():
                    print(f"✅ Found 'Single ticket' h4 with text: '{h4_text}'")
                    has_single_ticket = True
                    break
            
            return has_single_ticket and True  # True for outside courts since we filtered Simonne-Mathieu
            
        except Exception as e:
            print(f"❌ Error checking ticket validity: {e}")
            return False

    async def _find_ticket_link(self, item_div):
        """Find and return the first ticket link in a collection item"""
        try:
            print("Searching for <a> link within the collection item...")
            link = await item_div.evaluate_handle('''
                (element) => {
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
            
            if not link:
                return None
                
            # Get link details for logging
            link_href = await link.evaluate('el => el.href')
            link_text = await link.evaluate('el => el.textContent.trim()')
            print(f"Found link: '{link_text}' -> {link_href}")
            
            # Check price limit
            if "€" in link_text:
                try:
                    # Extract price number from text like "From €205"
                    price = float(link_text.split("€")[1].strip())
                    if price > 250:
                        print(f"❌ Skipping - price {price}€ exceeds 250€ limit")
                        return None
                except Exception as price_error:
                    print(f"⚠️ Could not parse price from '{link_text}', will check link anyway")
            
            # Debug: Show HTML
            try:
                link_html = await link.evaluate('el => el.outerHTML')
                print(f"🔍 Link HTML: {link_html}")
            except Exception as html_error:
                print(f"❌ Could not get link HTML: {html_error}")
            
            return link if "€" in link_text else None
            
        except Exception as e:
            print(f"❌ Error finding ticket link: {e}")
            return None

    async def _handle_ticket_link(self, link):
        """Handle clicking and processing a found ticket link"""
        try:
            print("🚨 STOPPING ALL DATE SWITCHING - TICKET FOUND!")
            self.ticket_found = True
            
            print("🖱️ Clicking ticket link (no href, must click)...")
            await link.scroll_into_view_if_needed()
            await link.click()
            print("✅ Successfully clicked ticket link!")
            
            await asyncio.sleep(1)  # Reduced from 2
            
            # Wait for ticket selection page with reduced timeout
            if not await self._verify_ticket_page():
                return True  # Still return True to prevent date switching
            
            # Handle the purchase
            if await self.handle_ticket_purchase():
                print("🎉 Successfully handled ticket purchase!")
                self.processing_ticket = False
                self.ticket_found = False  # Clear flag to resume automation
                return True
            else:
                print("❌ Ticket purchase failed")
                print("🚨 KEEPING BOTH FLAGS SET - TICKET WAS FOUND!")
                return True
                
        except Exception as e:
            print(f"❌ Error handling ticket link: {e}")
            print("🚨 KEEPING BOTH FLAGS SET TO PREVENT DATE SWITCHING!")
            return True

    async def _verify_ticket_page(self):
        """Verify we're on the ticket selection page"""
        try:
            print("🔍 Waiting for 'Select your ticket' h3...")
            select_ticket_h3 = await self.page.wait_for_selector(
                'h3:has-text("Select your ticket")', 
                timeout=5000  # Reduced from 10000
            )
            if select_ticket_h3:
                print("✅ Found 'Select your ticket' h3 - ticket page loaded!")
                return True
            else:
                print("❌ 'Select your ticket' h3 not found")
                return False
        except Exception as h3_error:
            print(f"❌ Error waiting for 'Select your ticket' h3: {h3_error}")
            print(f"📍 Current URL: {self.page.url}")
            return False

    async def check_collection_list(self):
        """Check the collection list for available tickets"""
        try:
            print(f"🔍 Starting check_collection_list...")
            
            # Find the collection list container
            collection_list = await self.page.query_selector('div.collection-list-2.w-dyn-items[role="list"]')
            if not collection_list:
                print("❌ No collection list found on page")
                return False
            
            # Get all collection items
            print("Searching for collection items...")
            collection_items = await self.page.query_selector_all('div.collection-item-2.w-dyn-item')
            print(f"📊 Found {len(collection_items)} collection items total")
            
            # Process each collection item
            for item_div in collection_items:
                # Check if this is a valid ticket
                if not await self._is_valid_ticket(item_div):
                    continue
                    
                print(f"🎉 AVAILABLE SINGLE TICKET + OUTSIDE COURTS FOUND! 🎉")
                
                # Find the ticket link
                link = await self._find_ticket_link(item_div)
                if not link:
                    continue
                    
                # Handle the found ticket
                return await self._handle_ticket_link(link)
            
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
                    # CRITICAL CHECK: Stop everything if ticket found or being processed
                    if self.ticket_found or self.processing_ticket:
                        print("🚨 TICKET FOUND OR PROCESSING - STOPPING ALL AUTOMATION!")
                        print("🔄 Waiting for ticket processing to complete...")
                        
                        # Keep waiting until both flags are cleared (with timeout)
                        wait_count = 0
                        max_wait_attempts = 2
                        
                        while (self.ticket_found or self.processing_ticket) and wait_count < max_wait_attempts:
                            wait_count += 1
                            await asyncio.sleep(2)
                            print(f"⏳ Still waiting for ticket processing... (attempt {wait_count}/{max_wait_attempts})")
                        
                        if wait_count >= max_wait_attempts:
                            print("⚠️ TIMEOUT: Waited too long for ticket processing!")
                            print("🔄 Resetting flags and resuming date switching...")
                            self.ticket_found = False
                            self.processing_ticket = False
                            await asyncio.sleep(1)  # Brief pause before continuing
                            continue
                            
                        print("✅ Ticket processing completed, resuming automation")
                        await asyncio.sleep(1)  # Brief pause before continuing
                    
                    # Check for blocking
                    if await self.check_for_blocking():
                        print("🚫 Blocking detected - stopping automation")
                        break
                    
                    # Find and process available dates
                    date_result = await self.find_available_date()
                    if date_result:
                        print("🎉 Ticket processing completed successfully!")
                        await asyncio.sleep(5)
                    else:
                        await asyncio.sleep(0.2)
                    
                    # Double check blocking after date processing
                    if await self.check_for_blocking():
                        print("🚫 Blocking detected after date processing - stopping automation")
                        break
                    
                except Exception as e:
                    print(f"❌ Error in cycle {attempt_count}: {str(e)}")
                    await asyncio.sleep(5)
                    if attempt_count >= 3:  # Add max attempts
                        print("⚠️ Max attempts reached - stopping automation")
                        break
            
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
    date_switch_delay = float(sys.argv[1]) if len(sys.argv) > 1 else 2.2
    found_ticket_delay = float(sys.argv[2]) if len(sys.argv) > 2 else 2.2
    print(f"Using delays - No tickets: {date_switch_delay}s, Found tickets: {found_ticket_delay}s")
    
    roland_garros_url = "https://tickets.rolandgarros.com/"
    automation = RolandGarrosAutomation(date_switch_delay=date_switch_delay, found_ticket_delay=found_ticket_delay)
    await automation.run_automation(roland_garros_url)

if __name__ == "__main__":
    asyncio.run(main()) 