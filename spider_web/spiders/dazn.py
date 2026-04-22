import scrapy
from datetime import datetime
from scrapy_playwright.page import PageMethod

from spider_web.items import DaznItem


class DaznSpider(scrapy.Spider):
    name = "dazn"

    def start_requests(self):
        yield scrapy.Request(
            "https://www.dazn.com/en-SG/sport/Sport:289u5typ3vp4ifwh5thalohmq",
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_load_state", "domcontentloaded"),
                    PageMethod("wait_for_timeout", 5000),
                    PageMethod("evaluate", "window.scrollTo(0, document.body.scrollHeight)"),
                    PageMethod("wait_for_timeout", 5000),
                ],
                "playwright_context_kwargs": {
                    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                                  "Chrome/120.0.0.0 Safari/537.36",
                    "viewport": {"width": 1920, "height": 1080},
                    "locale": "en-SG",
                },
            },
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]

        # Try to accept cookies, ignore if not found
        try:
            btn = page.locator(
                "button:has-text('Accept'), button:has-text('Accept All'), "
                "button[id*='accept'], [class*='accept-all']"
            ).first
            if await btn.is_visible(timeout=2000):
                await btn.click()
                self.logger.info("Accepted cookies")
                await page.wait_for_timeout(2000)
        except Exception:
            self.logger.info("No cookie banner found, skipping")

        # Scroll multiple times to load all content
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(3000)

        data = await page.evaluate("""() => {
            const results = [];

            document.querySelectorAll('h2').forEach(h2 => {
                const sectionName = h2.textContent.trim();
                if (!sectionName || sectionName.toLowerCase().includes('privacy')) return;

                let container = h2.parentElement;
                for (let i = 0; i < 8; i++) {
                    if (!container) break;
                    const imgs = container.querySelectorAll('img[src^="http"]');
                    if (imgs.length < 2) { container = container.parentElement; continue; }

                    imgs.forEach(img => {
                        let card = img;
                        for (let j = 0; j < 4; j++) {
                            card = card.parentElement;
                            if (!card) break;
                            if (['BUTTON', 'A', 'LI'].includes(card.tagName)) break;
                        }

                        let title = '';
                        let desc = '';
                        if (card) {
                            const texts = Array.from(card.querySelectorAll('span, p'))
                                .map(s => s.textContent.trim())
                                .filter(t => t.length > 0);
                            title = texts[0] || '';
                            desc = texts[1] || '';
                        }

                        if (img.src && !img.src.includes('cookielaw')) {
                            results.push({
                                section: sectionName,
                                image_url: img.src,
                                title: title,
                                description: desc,
                            });
                        }
                    });
                    break;
                }
            });

            return results;
        }""")

        await page.close()

        self.logger.info("Extracted %d items", len(data))
        for d in data:
            if d.get("image_url"):
                item = DaznItem()
                item["url"] = response.url
                item["title"] = d.get("title", "")
                item["description"] = d.get("description", "")
                item["image_url"] = d.get("image_url", "")
                item["section"] = d.get("section", "")
                item["crawled_at"] = datetime.now().isoformat()
                yield item
