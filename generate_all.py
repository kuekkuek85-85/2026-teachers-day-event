"""
1-1 ~ 1-8 전 반 일괄 생성: python generate_all.py
"""

import sys
from generate import generate, load_config

cfg = load_config()
classes = list(cfg.get("classes", {}).keys())

force = "--force" in sys.argv

print(f"총 {len(classes)}개 반 생성 시작\n")
results = []

for class_id in classes:
    try:
        out = generate(class_id, force_analysis=force)
        results.append((class_id, "✅", str(out)))
    except Exception as e:
        results.append((class_id, "❌", str(e)))

print("\n\n=== 생성 결과 ===")
for class_id, status, msg in results:
    print(f"  {status} {class_id}: {msg}")
