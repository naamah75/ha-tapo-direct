"""Small dependency-free repository validation."""
from __future__ import annotations
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
INTEGRATION = ROOT / "custom_components" / "tapo_direct"
required = ["manifest.json", "__init__.py", "config_flow.py", "const.py", "coordinator.py", "light.py", "strings.json", "translations/en.json", "translations/it.json"]
for relative in required:
    path = INTEGRATION / relative
    assert path.is_file(), f"Missing {relative}"
for path in [ROOT / "hacs.json", INTEGRATION / "manifest.json", INTEGRATION / "strings.json", *sorted((INTEGRATION / "translations").glob("*.json"))]:
    json.loads(path.read_text())
manifest = json.loads((INTEGRATION / "manifest.json").read_text())
assert manifest["domain"] == "tapo_direct"
assert manifest["config_flow"] is True
assert manifest["requirements"] == ["python-kasa[speedups]>=0.11.0.1"]
print("VALIDATION_OK")
