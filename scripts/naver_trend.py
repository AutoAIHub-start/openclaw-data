"""
네이버 데이터랩 쇼핑인사이트 - 자동차 부품 트렌드 분석
Client ID: h5hD74VF0RyuCf82KXFt
"""
import os
import requests
import json
from datetime import datetime, timedelta

CLIENT_ID = "h5hD74VF0RyuCf82KXFt"
CLIENT_SECRET = os.environ.get("NAVER_CLIENT_SECRET", "")

URL = "https://openapi.naver.com/v1/datalab/shopping/categories"

def get_trend(keywords: list, start_date: str, end_date: str):
    """
    키워드 트렌드 조회
    keywords: 조회할 카테고리/키워드 리스트
    start_date: 시작일 (예: "2025-01-01")
    end_date:   종료일 (예: "2025-04-30")
    """
    body = {
        "startDate": start_date,
        "endDate": end_date,
        "timeUnit": "month",   # week / month / date
        "category": [
            {"name": kw, "param": [kw]} for kw in keywords
        ],
        "device": "",          # pc / mo / "" (전체)
        "gender": "",          # f / m / ""
        "ages": []             # ["10","20","30"] 등
    }
import sys
sys.stdout.reconfigure(encoding='utf-8')
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

def print_report(data):
    """결과를 보기 좋게 출력"""
    if not data:
        return

    print("\n" + "="*50)
    print("  자동차 부품 쇼핑 트렌드 리포트")
    print("="*50)

    for result in data.get("results", []):
        name = result["title"]
        print(f"\n[{name}]")
        for point in result["data"]:
            bar = "█" * int(point["ratio"] / 5)
            print(f"  {point['period']}  {bar} {point['ratio']:.1f}")

    print("\n" + "="*50)

if __name__ == "__main__":
    # 조회할 자동차 부품 키워드
    keywords = [
        "브레이크패드",
        "엔진오일",
        "타이어",
        "배터리",
        "와이퍼"
    ]

    # 최근 6개월
    end = datetime.today()
    start = end - timedelta(days=180)

    data = get_trend(
        keywords=keywords,
        start_date=start.strftime("%Y-%m-%d"),
        end_date=end.strftime("%Y-%m-%d")
    )

    print_report(data)

    # JSON 파일로 저장
    if data:
        filename = f"trend_{datetime.today().strftime('%Y%m%d')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n결과 저장 완료: {filename}")
