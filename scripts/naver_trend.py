"""
네이버 데이터랩 쇼핑인사이트 - 자동차 부품 트렌드 분석
Client ID: h5hD74VF0RyuCf82KXFt
"""
import os
import sys
import requests
import json
from datetime import datetime, timedelta

sys.stdout.reconfigure(encoding='utf-8')

CLIENT_ID = "h5hD74VF0RyuCf82KXFt"
CLIENT_SECRET = os.environ.get("NAVER_CLIENT_SECRET", "")

URL = "https://openapi.naver.com/v1/datalab/shopping/categories"

def get_trend(keywords: list, start_date: str, end_date: str):
    body = {
        "startDate": start_date,
        "endDate": end_date,
        "timeUnit": "month",
        "category": [
            {"name": kw, "param": [kw]} for kw in keywords
        ],
        "device": "",
        "gender": "",
        "ages": []
    }
    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET,
        "Content-Type": "application/json"
    }
    res = requests.post(URL, headers=headers, json=body)
    if res.status_code == 200:
        return res.json()
    else:
        print(f"에러: {res.status_code}")
        print(res.text)
        return None

if __name__ == "__main__":
    keywords = ["브레이크패드", "엔진오일", "타이어", "배터리", "와이퍼"]
    end = datetime.today()
    start = end - timedelta(days=180)
    data = get_trend(
        keywords=keywords,
        start_date=start.strftime("%Y-%m-%d"),
        end_date=end.strftime("%Y-%m-%d")
    )
    if data:
        os.makedirs("data", exist_ok=True)
        with open("data/daily_trend.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("daily_trend.json 저장 완료")
    else:
        print("데이터 수집 실패")
