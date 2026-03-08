import requests, json
key = "AIzaSyAiFhHWlQQ8-RLuCIxGUy_B3sCaqyAYGxo"
# Try v1 API instead of v1beta
for base in ["v1", "v1beta"]:
    for model in ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"]:
        url = f"https://generativelanguage.googleapis.com/{base}/models/{model}:generateContent?key={key}"
        try:
            r = requests.post(url, json={"contents":[{"parts":[{"text":"Say OK"}]}]}, timeout=15)
            d = r.json()
            if "candidates" in d:
                print(f"WORKS: {base}/{model} -> {d['candidates'][0]['content']['parts'][0]['text'][:40]}")
            else:
                err = d.get('error',{}).get('message','?')[:70]
                print(f"FAIL {base}/{model}: {err}")
        except Exception as e:
            print(f"EXC {base}/{model}: {e}")
