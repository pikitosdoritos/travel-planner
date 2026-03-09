import httpx

ARTIC_BASE_URL = "https://api.artic.edu/api/v1/artworks"

async def fetch_artwork_by_id(external_id: int) -> dict | None:
    url = f"{ARTIC_BASE_URL}/{external_id}"

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)

    if response.status_code != 200:
        return None

    data = response.json()
    artwork = data.get("data")

    if not artwork:
        return None

    return {
        "external_id": artwork["id"],
        "title": artwork.get("title", f"Artwork {artwork['id']}"),
        "api_link": artwork.get("api_link")
    }