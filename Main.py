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

    await page.goto(f'http://app.zoom.us/wc/join/{meetingcode}')
    await page.waitForXPath('//input[@type="text"]')
    await asyncio.sleep(2)  # Wait a bit more after page load

    # Type the user name
    await page.type('input[type="text"]', user)
    await asyncio.sleep(2)  # Wait a bit after typing user name

    # Type the password
    await page.type('input[type="password"]', passcode)
    await asyncio.sleep(2)  # Wait a bit after typing password

    # Click the "Join" button
    join_button = await page.waitForXPath('//button[contains(@class,"preview-join-button")]')
    await join_button.click()

    print(f"{name} sleep for {wait_time} seconds ...")
    await asyncio.sleep(wait_time)

    try:
        # Wait for and click on the "Join Audio by Computer" button
        print(f"{name} waiting for 'Join Audio by Computer' button...")
        await page.waitForXPath('//button[contains(@class,"join-audio-by-voip__join-btn")]')
        mic_button = await page.Jx('//button[contains(@class,"join-audio-by-voip__join-btn")]')
        await mic_button[0].click()
        print(f"{name} clicked 'Join Audio by Computer' button.")
    except Exception as e:
        print(f"{name} failed to join audio by computer:", e)

    print(f"{name} ended!")

    await browser.close()

async def main():
    number = 10
    meetingcode = "82732570230"
    passcode = "TRADE123"

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
