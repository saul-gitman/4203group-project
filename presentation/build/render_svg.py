import sys, pathlib
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 2350, "height": 875}, device_scale_factor=2)
    for f in sys.argv[1:]:
        f = pathlib.Path(f)
        pg.goto(f.resolve().as_uri())
        pg.screenshot(path=str(f.with_suffix(".png")), full_page=False)
        print("rendered", f.with_suffix(".png"))
    b.close()
