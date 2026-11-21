import sys
from playwright.sync_api import sync_playwright
url,out=sys.argv[1],sys.argv[2]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/chromium-browser", args=["--disable-gpu","--disable-dev-shm-usage"])
    pg=b.new_page(viewport={"width":1440,"height":1080})
    try: pg.goto(url, wait_until="commit", timeout=40000)
    except Exception as e: print("goto", e)
    pg.wait_for_timeout(8000); pg.mouse.wheel(0,400); pg.wait_for_timeout(1500); pg.mouse.wheel(0,-400); pg.wait_for_timeout(12000)
    pg.screenshot(path=out, animations="disabled", timeout=60000)
    b.close()
