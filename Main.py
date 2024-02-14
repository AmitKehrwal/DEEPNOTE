import asyncio
import nest_asyncio
from pyppeteer import launch
from pyppeteer_stealth import stealth
import indian_names  # Import the indian_names library

nest_asyncio.apply()

running = True  # Define the 'running' variable

async def start(name, user, wait_time, meetingcode, passcode):
    print(f"{name} started!")

    browser = await launch(
        headless=True,
        args=['--no-sandbox', '--disable-dev-shm-usage']
    )
    page = await browser.newPage()

    # Apply pyppeteer-stealth to mimic a real browser
    await stealth(page)

    await page.goto(f'https://zoom.us/wc/join/{meetingcode}')

    try:
        await page.click('//button[@id="onetrust-accept-btn-handler"]', timeout=5000)
    except Exception as e:
        pass

    try:
        await page.click('//button[@id="wc_agree1"]', timeout=5000)
    except Exception as e:
        pass

    try:
        await page.waitForSelector('input[type="text"]', timeout=200000)
        await page.type('input[type="text"]', user)
        await page.type('input[type="password"]', passcode)
        join_button = await page.waitForSelector('button.preview-join-button', timeout=200000)
        await join_button.click()
    except Exception as e:
        pass

    try:
        await page.waitForSelector('button[class*="join-audio-by-voip__join-btn"]', timeout=300000)
        mic_button_locator = await page.querySelector('button[class*="join-audio-by-voip__join-btn"]')
        await asyncio.sleep(5)
        await mic_button_locator.click()
        print(f"{name} mic aayenge.")
    except Exception as e:
        print(f"{name} mic nahe aayenge. ", e)

    print(f"{user} sleep for {wait_time} seconds ...")
    while running and wait_time > 0:
        await asyncio.sleep(1)
        wait_time -= 1
    print(f"{user} ended!")

    await browser.close()

async def main():
    number = 10
    meetingcode = "82725009687"
    passcode = "0"

    sec = 90
    wait_time = sec * 80

    loop = asyncio.get_event_loop()
    tasks = []

    for i in range(number):
        user = indian_names.get_full_name()  # Generate a random Indian name
        task = loop.create_task(start(f'[Thread{i}]', user, wait_time, meetingcode, passcode))
        tasks.append(task)

    try:
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        # Wait for tasks to complete
        await asyncio.gather(*tasks, return_exceptions=True)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
