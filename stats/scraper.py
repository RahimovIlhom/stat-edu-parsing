import asyncio
from playwright.async_api import async_playwright
from django.utils import timezone
from .models import Institution, StatisticsSnapshot
import logging
from asgiref.sync import sync_to_async

logger = logging.getLogger(__name__)

@sync_to_async
def get_or_create_institution(otm_code, otm_name, ownership_type):
    return Institution.objects.get_or_create(
        otm_code=otm_code,
        defaults={
            'otm_name': otm_name,
            'ownership_type': ownership_type
        }
    )

@sync_to_async
def update_or_create_snapshot(institution, snapshot_date, data):
    return StatisticsSnapshot.objects.update_or_create(
        institution=institution,
        snapshot_date=snapshot_date,
        defaults=data
    )

async def scrape_and_save_statistics():
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            # Navigate to the statistics page
            await page.goto("https://stat.edu.uz/tables?id=5")
            await page.wait_for_selector("table", timeout=30000)
            await asyncio.sleep(2)  # Additional wait to ensure data is loaded

            # Get today's date for the snapshot
            today = timezone.now().date()

            # Extract and process table data
            # Specifically target the tbody and its rows to avoid header and footer
            rows = await page.query_selector_all("table tbody tr")

            for row in rows[1:]:
                cells = await row.query_selector_all("td")
                if len(cells) < 15:  # Skip rows with insufficient data
                    continue

                # Extract data from cells
                data = [await cell.inner_text() for cell in cells]
                data = [item.strip() or '0' for item in data]

                try:
                    # Get or create institution
                    institution, _ = await get_or_create_institution(data[0], data[1], data[2])

                    # Prepare data for snapshot
                    snapshot_data = {
                        'bachelor_full_time': int(data[3]),
                        'bachelor_evening': int(data[4]),
                        'bachelor_part_time': int(data[5]),
                        'bachelor_special': int(data[6]),
                        'bachelor_joint': int(data[7]),
                        'bachelor_distance': int(data[8]),
                        'secondary_full_time': int(data[9]),
                        'secondary_evening': int(data[10]),
                        'secondary_part_time': int(data[11]),
                        'masters_full_time': int(data[12]),
                        'masters_evening': int(data[13]),
                        'masters_part_time': int(data[14]),
                        'masters_special': int(data[15]) if len(data) > 15 else 0,
                        'masters_joint': int(data[16]) if len(data) > 16 else 0,
                        'masters_distance': int(data[17]) if len(data) > 17 else 0,
                    }

                    # Create or update statistics snapshot
                    await update_or_create_snapshot(institution, today, snapshot_data)

                except (ValueError, IndexError) as e:
                    logger.error(f"Error processing row for institution {data[0]}: {str(e)}")
                    continue

            await browser.close()
            logger.info(f"Successfully updated statistics for {today}")

    except Exception as e:
        logger.error(f"Error scraping statistics: {str(e)}")
        raise

