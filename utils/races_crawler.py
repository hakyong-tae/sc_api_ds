from datetime import datetime, timezone, timedelta
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LAST_EVENT_FILE = "last_event_id.txt"

def fetch_competition(usedata_code):
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        url = f"https://smartchip.co.kr/Search_Ballyno.html?usedata={usedata_code}"
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'textfitted'))
        )

        title_element = driver.find_element(By.CLASS_NAME, 'textfitted')
        competition_name = title_element.text.strip()

        list_items = driver.find_elements(By.CSS_SELECTOR, 'div.list_box li')

        competition_date = "정보 없음"
        competition_place = "정보 없음"

        for item in list_items:
            text = item.text.strip()
            if text.startswith("일시"):
                competition_date = text.replace("일시 :", "").strip()
            elif text.startswith("장소"):
                competition_place = text.replace("장소 :", "").strip()

        driver.quit()

        if not competition_name:
            return None

        return {
            "usedata": usedata_code,
            "대회명": competition_name,
            "대회일자": competition_date,
            "대회장소": competition_place
        }

    except Exception as e:
        print(f"Error fetching usedata={usedata_code}: {e}")
        return None

def main():
    if os.path.exists(LAST_EVENT_FILE):
        with open(LAST_EVENT_FILE, "r") as f:
            start_code = int(f.read().strip())
    else:
        start_code = 202550000060  # 최초 시작

    max_success = 7
    max_fail = 10
    success_count = 0
    fail_count = 0
    collected_events = []

    while success_count < max_success and fail_count < max_fail:
        print(f"Checking usedata={start_code}...")
        data = fetch_competition(start_code)

        if data:
            print(f"✅ Event Found: {data['대회명']}")
            collected_events.append(data)
            success_count += 1
            fail_count = 0
        else:
            print("❓ No usable event")
            fail_count += 1

        start_code += 1

    if collected_events:
        save_dir = "output"
        os.makedirs(save_dir, exist_ok=True)
        KST = timezone(timedelta(hours=9))
        utc_now = datetime.now(timezone.utc)   # <- 이게 핵심
        kst_now = utc_now.astimezone(KST)
        today = kst_now.strftime("%Y-%m-%d")
        save_path = os.path.join(save_dir, f"events_{today}.json")


        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(collected_events, f, ensure_ascii=False, indent=2)

        print(f"\n📦 Saved {len(collected_events)} events to {save_path}")
    else:
        print("\n⚠️ No events collected, nothing saved.")

    with open(LAST_EVENT_FILE, "w") as f:
        f.write(str(start_code))

if __name__ == "__main__":
    main()
