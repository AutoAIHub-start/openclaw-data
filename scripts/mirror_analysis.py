import os
import sys
import json
import requests
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

CLIENT_ID = "h5hD74VF0RyuCf82KXFt"
CLIENT_SECRET = os.environ.get("NAVER_CLIENT_SECRET", "")

KEYWORDS = [
    ("벤츠", "백미러"), ("벤츠", "사이드미러"),
    ("BMW", "백미러"), ("BMW", "사이드미러"),
    ("아우디", "백미러"), ("아우디", "사이드미러"),
    ("폭스바겐", "백미러"), ("폭스바겐", "사이드미러"),
    ("혼다", "백미러"), ("혼다", "사이드미러"),
    ("렉서스", "백미러"), ("렉서스", "사이드미러"),
    ("토요타", "백미러"), ("토요타", "사이드미러"),
]

def search_naver(keyword):
    url = "https://openapi.naver.com/v1/search/shop.json"
    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET,
    }
    params = {"query": keyword, "display": 10, "sort": "sim"}
    res = requests.get(url, headers=headers, params=params)
    if res.status_code == 200:
        return res.json()
    return None

results = []
for brand, part in KEYWORDS:
    keyword = f"{brand} {part}"
    data = search_naver(keyword)
    if not data:
        continue
    items = data.get("items", [])
    prices = [int(i["lprice"]) for i in items if i.get("lprice")]
    result = {
        "brand": brand,
        "part": part,
        "keyword": keyword,
        "total": data.get("total", 0),
        "demand": "🟢 활발" if data.get("total", 0) >= 1000 else "🔴 저조",
        "avg": int(sum(prices) / len(prices)) if prices else 0,
        "min": min(prices) if prices else 0,
        "max": max(prices) if prices else 0,
        "items": [
            {
                "name": i.get("title", "").replace("<b>", "").replace("</b>", ""),
                "price": int(i.get("lprice", 0)),
                "mall": i.get("mallName", ""),
                "review": int(i.get("reviewCount", 0)),
            }
            for i in items
        ],
    }
    results.append(result)
    print(f"✅ {keyword}: {result['total']}개")

output = {"updated": datetime.now().strftime("%Y-%m-%d %H:%M"), "results": results}
os.makedirs("data", exist_ok=True)
with open("data/mirror_trend.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
print("mirror_trend.json 저장 완료")
