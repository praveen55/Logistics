from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# --- Browser Setup ---
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
# options.add_argument("--headless=new")  # Uncomment for headless CI/CD runs
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

try:
    # 1. Access Logistics Portal
    driver.get("https://example-logistics-portal.com/login")

    # 2. Authentication
    wait.until(EC.visibility_of_element_located((By.ID, "username"))).send_keys("dispatcher_ops")
    driver.find_element(By.ID, "password").send_keys("SecurePass123!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # 3. Create a New Shipment (Dispatch Workflow)
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Create Consignment"))).click()

    # Fill Origin & Destination Addresses
    wait.until(EC.visibility_of_element_located((By.ID, "origin_hub"))).send_keys("Warehouse A - Dallas")
    driver.find_element(By.ID, "dest_hub").send_keys("Distribution Center 4 - Austin")

    # Select Service Type (Dropdown)
    service_dropdown = Select(driver.find_element(By.ID, "shipping_tier"))
    service_dropdown.select_by_visible_text("Express Next-Day Air")

    # Input Cargo Details
    driver.find_element(By.NAME, "package_weight_kg").send_keys("45.5")
    driver.find_element(By.NAME, "cargo_type").send_keys("Fragile Electronics")

    # Submit Shipment and Capture Generated Waybill/AWB
    driver.find_element(By.ID, "btn-generate-waybill").click()

    awb_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".waybill-tracking-number")))
    generated_awb = awb_element.text
    print(f"[SUCCESS] Shipment created. AWB: {generated_awb}")

    # 4. Verify Shipment Status in Track & Trace
    driver.find_element(By.LINK_TEXT, "Track & Trace").click()

    search_box = wait.until(EC.visibility_of_element_located((By.ID, "track_input")))
    search_box.send_keys(generated_awb)
    driver.find_element(By.ID, "track_btn").click()

    status_badge = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".status-badge")))
    assert "Dispatched" in status_badge.text or "Manifest Created" in status_badge.text
    print(f"[VERIFIED] Live Status: {status_badge.text}")

finally:
    driver.quit()
