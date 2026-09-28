import json, os, re, urllib.request, urllib.error
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deals.json"
API_KEY = os.environ["OPENAI_API_KEY"]
JST = timezone(timedelta(hours=9))
today = datetime.now(JST).strftime("%Y-%m-%d")

prompt = f"""
今日は {today}。
日本国内で現在実際に使える「得する情報」を最新Web検索してください。

対象:
- クーポン
- 無料券
- ポイント還元
- キャッシュバック
- キャンペーン
- 公的な優遇・節約制度で、一般個人が使いやすいもの

ルール:
1. 必ず公式サイト、公式キャンペーンページ、官公庁など一次情報で確認する。
2. 今日時点で期限切れの情報は絶対に含めない。
3. 開始日、終了日、対象条件、上限、エントリー要否を確認する。
4. 不要な購入を促すものは原則除外する。
5. Amazonの購入はAmazonカード、それ以外はRecruit Cardを基本に実質メリットを考える。
6. 数より確度を優先し、最大10件。
7. value は一般的な1回利用で合理的に金額換算できる場合だけ数値。難しければ0。
8. source_url は必ず確認した公式ページのURL。
9. 古いまとめサイトや出典不明ページを根拠にしない。

出力は説明文なしで、次のJSONだけにしてください:
{{
  "verified_at":"YYYY-MM-DD",
  "deals":[
    {{
      "title":"",
      "provider":"",
      "value":0,
      "start_date":"",
      "end_date":"",
      "conditions":"",
      "summary":"",
      "source":"",
      "source_url":""
    }}
  ]
}}
"""

payload = {
    "model": "gpt-5.6-luna",
    "tools": [{"type": "web_search"}],
    "input": prompt
}

req = urllib.request.Request(
    "https://api.openai.com/v1/responses",
    data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    method="POST"
)

with urllib.request.urlopen(req, timeout=180) as resp:
    obj = json.loads(resp.read().decode("utf-8"))

texts = []
for item in obj.get("output", []):
    if item.get("type") == "message":
        for c in item.get("content", []):
            if c.get("type") == "output_text" and c.get("text"):
                texts.append(c["text"])
text = "\n".join(texts).strip()
if not text:
    raise RuntimeError("OpenAI response had no output_text")

try:
    data = json.loads(text)
except json.JSONDecodeError:
    m = re.search(r"\{[\s\S]*\}", text)
    if not m:
        raise
    data = json.loads(m.group(0))

if not isinstance(data, dict) or not isinstance(data.get("deals"), list):
    raise RuntimeError("Invalid deals JSON")
data["verified_at"] = today

# Minimum sanitation
clean = []
for d in data["deals"][:10]:
    if not isinstance(d, dict):
        continue
    title = str(d.get("title","")).strip()
    if not title:
        continue
    clean.append({
        "title": title,
        "provider": str(d.get("provider","")).strip(),
        "value": float(d.get("value",0) or 0),
        "start_date": str(d.get("start_date","")).strip(),
        "end_date": str(d.get("end_date","")).strip(),
        "conditions": str(d.get("conditions","")).strip(),
        "summary": str(d.get("summary","")).strip(),
        "source": str(d.get("source","")).strip(),
        "source_url": str(d.get("source_url","")).strip(),
    })
data["deals"] = clean

OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {len(clean)} deals to {OUT}")
