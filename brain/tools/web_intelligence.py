import logging
from scrapling import Fetcher

logger = logging.getLogger("FriendlyClaw.WebIntelligence")

def deep_read_url(url: str) -> str:
    """
    Uses Scrapling to perform a deep, clean read of a web page.
    Returns the visible text content optimized for LLM consumption.
    """
    logger.info(f"Deep reading URL: {url}")
    try:
        fetcher = Fetcher(auto_match=True)
        result = fetcher.get(url)
        
        if not result or not result.text:
            return "Error: Could not extract content from this URL."
            
        # Basic cleanup: extract text and limit size to avoid context overflow
        content = result.text.strip()
        
        if len(content) > 15000:
            content = content[:15000] + "\n\n[Content Truncated...]"
            
        return content
    except Exception as e:
        logger.error(f"Scrapling failed for {url}: {e}")
        return f"Failed to read the page: {str(e)}"
