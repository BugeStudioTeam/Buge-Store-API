# Buge Store API Documentation

## Base URL

```
https://raw.githubusercontent.com/BugeStudioTeam/Buge-Store-API/main/api/v1/
```

## Endpoints

### Get All Apps

```
GET /apps.json
```

**Response:**

```
{
  "version": 1,
  "last_updated": "2026-07-17T10:00:00Z",
  "total_apps": 2,
  "apps": [
    {
      "package": "com.example.app1",
      "name": "Example App",
      "icon": "https://raw.githubusercontent.com/BugeStudioTeam/Buge-Store-API/main/apps/com.example.app1/metadata/icon.webp",
      "categories": ["Tools", "Utilities"],
      "latest_version": "1.0.0",
      "download_url": "https://github.com/example/repo/releases/download/v1.0.0/app.apk",
      "size_mb": 5.2,
      "signature": "AB:CD:EF:12:34:56:78:90:AB:CD:EF:12:34:56:78:90",
      "min_sdk": 21,
      "developer": "BugeStudioTeam"
    }
  ]
}
```

### Get Categories

```
GET /categories.json
```

**Response:**

```
{
  "categories": [
    {
      "name": "Tools",
      "count": 1,
      "apps": ["com.example.app1"]
    },
    {
      "name": "Utilities",
      "count": 1,
      "apps": ["com.example.app1"]
    }
  ]
}
```

### Get Trending Apps

```
GET /trending.json
```

**Response:**

```
{
  "last_updated": "2026-07-17T10:00:00Z",
  "trending": [
    {
      "package": "com.example.app1",
      "name": "Example App",
      "downloads": 0,
      "trend_score": 0
    }
  ]
}
```

## Usage Examples

### JavaScript

```
const response = await fetch(
  'https://raw.githubusercontent.com/BugeStudioTeam/Buge-Store-API/main/api/v1/apps.json'
);
const data = await response.json();
console.log(data.apps);
```

### Android (Kotlin)

```
val client = OkHttpClient()
val request = Request.Builder()
    .url("https://raw.githubusercontent.com/BugeStudioTeam/Buge-Store-API/main/api/v1/apps.json")
    .build()
client.newCall(request).execute().use { response ->
    val json = response.body?.string()
    // Parse JSON
}
```

### Python

```
import requests
response = requests.get(
    'https://raw.githubusercontent.com/BugeStudioTeam/Buge-Store-API/main/api/v1/apps.json'
)
apps = response.json()['apps']
```

## Rate Limiting

GitHub Raw API has rate limits for unauthenticated requests:

- 60 requests per hour from a single IP
- 5,000 requests per hour with authentication

For production use, consider implementing a caching proxy or using a CDN.

## Error Handling

All endpoints return HTTP 200 on success. Common error scenarios:

- Rate limiting: HTTP 403 or 429
- File not found: HTTP 404
- Network issues: Connection errors

Always validate the response structure before parsing.