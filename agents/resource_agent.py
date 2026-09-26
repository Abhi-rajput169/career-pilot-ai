from ddgs import DDGS
from pydantic import BaseModel, Field


# ============================================================
# RESOURCE MODEL
# ============================================================

class LearningResource(BaseModel):
    title: str
    url: str
    why_recommended: str


class ResourceReport(BaseModel):
    resources: list[LearningResource]


# ============================================================
# URL VALIDATION
# ============================================================

def is_youtube_url(url: str) -> bool:
    """Accept only real youtube.com video URLs."""
    if not url:
        return False
    url_lower = url.lower()
    return (
        "youtube.com/watch" in url_lower or
        "youtu.be/" in url_lower
    )


# ============================================================
# SEARCH YOUTUBE FOR A SKILL
# ============================================================

MAX_RESOURCES_PER_GAP = 3

def search_youtube_resources(requirement: str, user_status: str) -> ResourceReport:
    """
    Search YouTube directly for tutorial videos on this requirement.
    Returns at most MAX_RESOURCES_PER_GAP real YouTube video URLs.
    """

    # Determine user level for targeted query
    status_lower = user_status.strip().lower()
    if any(w in status_lower for w in ["beginner", "no ", "none", "0 year", "not "]):
        level = "for beginners"
    elif any(w in status_lower for w in ["intermediate", "1 year", "2 year"]):
        level = "intermediate tutorial"
    else:
        level = "tutorial"

    queries = [
        f"{requirement} full course {level} site:youtube.com",
        f"learn {requirement} {level} site:youtube.com",
        f"{requirement} tutorial site:youtube.com",
    ]

    collected: list[LearningResource] = []
    seen_urls: set[str] = set()

    for query in queries:
        if len(collected) >= MAX_RESOURCES_PER_GAP:
            break
        try:
            with DDGS() as ddgs:
                results = ddgs.text(query, max_results=5)
                for result in results:
                    if len(collected) >= MAX_RESOURCES_PER_GAP:
                        break
                    url = result.get("href", "")
                    if not is_youtube_url(url):
                        continue
                    if url in seen_urls:
                        continue
                    seen_urls.add(url)
                    title = result.get("title", "").strip()
                    # Clean up title (remove " - YouTube" suffix)
                    if title.endswith(" - YouTube"):
                        title = title[:-10].strip()
                    collected.append(
                        LearningResource(
                            title=title or requirement,
                            url=url,
                            why_recommended=(
                                f"Free YouTube tutorial for {requirement}"
                            ),
                        )
                    )
        except Exception as e:
            print(f"⚠️ YouTube search failed for '{query}': {e}. Continuing...")
            continue

    return ResourceReport(resources=collected)


# ============================================================
# MAIN RESOURCE FUNCTION
# ============================================================

def find_resources_for_gap(
    requirement: str,
    category: str,
    importance: str,
    user_status: str,
) -> ResourceReport:

    print(f"\n📺 Searching YouTube for: {requirement}")

    report = search_youtube_resources(requirement, user_status)

    if report.resources:
        print(f"  ✅ Found {len(report.resources)} YouTube video(s).")
    else:
        print(f"  ⚠️ No YouTube videos found for: {requirement}")

    return report