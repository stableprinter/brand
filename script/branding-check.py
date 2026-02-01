#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List, Tuple

HEX_COLOR_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")

REQUIRED_JSON_PATHS = [
    # identifiers
    "identifiers.androidBundleId",
    "identifiers.iosBundleId",
    "identifiers.webAppDomain",
    "identifiers.deepLinkScheme",
    # api
    "api.apiBaseUrl",
    "api.apiVersion",
    "api.websocketUrl",
    "api.cdnBaseUrl",
    "api.imageBaseUrl",
    # branding
    "branding.appName",
    "branding.companyName",
    "branding.primaryColor",
    "branding.accentColor",
    "branding.logoUrl",
    "branding.logoDarkUrl",
    "branding.supportEmail",
    "branding.supportUrl",
    "branding.privacyPolicyUrl",
    "branding.termsUrl",
    # stores
    "stores.iosAppStoreId",
    "stores.androidPlayStoreId",
]

# Files you showed in your tree (strict)
REQUIRED_FILES_BY_ENV = [
    # root JSON
    "{env}.json",

    # iOS AppIcon set
    "asset/{env}/appicon/Assets.xcassets/AppIcon.appiconset/Contents.json",
    "asset/{env}/appicon/Assets.xcassets/AppIcon.appiconset/29.png",
    "asset/{env}/appicon/Assets.xcassets/AppIcon.appiconset/40.png",
    "asset/{env}/appicon/Assets.xcassets/AppIcon.appiconset/57.png",
    "asset/{env}/appicon/Assets.xcassets/AppIcon.appiconset/58.png",
    "asset/{env}/appicon/Assets.xcassets/AppIcon.appiconset/60.png",
    "asset/{env}/appicon/Assets.xcassets/AppIcon.appiconset/80.png",
    "asset/{env}/appicon/Assets.xcassets/AppIcon.appiconset/87.png",
    "asset/{env}/appicon/Assets.xcassets/AppIcon.appiconset/1024.png",
    "asset/{env}/appicon/Assets.xcassets/AppIcon.appiconset/114.png",
    "asset/{env}/appicon/Assets.xcassets/AppIcon.appiconset/120.png",
    "asset/{env}/appicon/Assets.xcassets/AppIcon.appiconset/180.png",

    # Store icons
    "asset/{env}/appicon/appstore.png",
    "asset/{env}/appicon/playstore.png",

    # Android launcher icons
    "asset/{env}/appicon/android/mipmap-mdpi/ic_launcher.png",
    "asset/{env}/appicon/android/mipmap-hdpi/ic_launcher.png",
    "asset/{env}/appicon/android/mipmap-xhdpi/ic_launcher.png",
    "asset/{env}/appicon/android/mipmap-xxhdpi/ic_launcher.png",
    "asset/{env}/appicon/android/mipmap-xxxhdpi/ic_launcher.png",

    # Fonts
    "asset/{env}/fonts/brand.ttf",

    # Splash
    "asset/{env}/splashscreen/splashscreen.png",
]

def eprint(msg: str) -> None:
    print(msg, file=sys.stderr)

def load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_by_path(obj: Dict[str, Any], dotted: str) -> Any:
    cur: Any = obj
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur

def is_non_empty_value(v: Any) -> bool:
    if v is None:
        return False
    if isinstance(v, str):
        return v.strip() != ""
    if isinstance(v, (list, dict)):
        return len(v) > 0
    # numbers/bools are acceptable if present
    return True

def check_required_files(repo_root: str, env: str) -> List[str]:
    missing: List[str] = []
    for rel in REQUIRED_FILES_BY_ENV:
        rel_path = rel.format(env=env)
        abs_path = os.path.join(repo_root, rel_path)
        if not os.path.isfile(abs_path):
            missing.append(rel_path)
    return missing

def check_json(repo_root: str, env: str, check_logo_files: bool) -> List[str]:
    issues: List[str] = []
    json_rel = f"{env}.json"
    json_path = os.path.join(repo_root, json_rel)

    if not os.path.isfile(json_path):
        issues.append(f"Missing JSON: {json_rel}")
        return issues

    try:
        data = load_json(json_path)
    except Exception as ex:
        issues.append(f"Invalid JSON ({json_rel}): {ex}")
        return issues

    # required keys + non-empty
    for p in REQUIRED_JSON_PATHS:
        v = get_by_path(data, p)
        if v is None:
            issues.append(f"Missing key: {p}")
        elif not is_non_empty_value(v):
            issues.append(f"Empty value: {p}")

    # color validation
    primary = get_by_path(data, "branding.primaryColor")
    accent = get_by_path(data, "branding.accentColor")
    if isinstance(primary, str) and not HEX_COLOR_RE.match(primary.strip()):
        issues.append(f"Invalid color branding.primaryColor (expected #RRGGBB): {primary!r}")
    if isinstance(accent, str) and not HEX_COLOR_RE.match(accent.strip()):
        issues.append(f"Invalid color branding.accentColor (expected #RRGGBB): {accent!r}")

    # logo files exist (optional)
    if check_logo_files:
        logo = get_by_path(data, "branding.logoUrl")
        logo_dark = get_by_path(data, "branding.logoDarkUrl")

        def resolve_logo(v: Any) -> Tuple[str, str]:
            # treat as relative to asset/<env>/images/
            rel = str(v).strip()
            assumed_rel = f"asset/{env}/images/{rel}"
            return rel, assumed_rel

        for key, val in [("branding.logoUrl", logo), ("branding.logoDarkUrl", logo_dark)]:
            if isinstance(val, str) and val.strip():
                _, assumed = resolve_logo(val)
                if not os.path.isfile(os.path.join(repo_root, assumed)):
                    issues.append(f"{key} points to {val!r}, but missing file at: {assumed}")

    return issues

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".", help="Repo root path (default: .)")
    ap.add_argument("--env", choices=["production", "staging", "both"], default="both")
    ap.add_argument("--check-logo-files", action="store_true",
                    help="Also verify branding.logoUrl/logoDarkUrl exist under asset/<env>/images/")
    args = ap.parse_args()

    repo_root = os.path.abspath(args.repo_root)
    envs = ["production", "staging"] if args.env == "both" else [args.env]

    all_errors: List[str] = []
    for env in envs:
        missing_files = check_required_files(repo_root, env)
        json_issues = check_json(repo_root, env, args.check_logo_files)

        if missing_files or json_issues:
            all_errors.append(f"\n=== {env.upper()} CHECK FAILED ===")
            if missing_files:
                all_errors.append("Missing required files:")
                all_errors.extend([f"  - {p}" for p in missing_files])
            if json_issues:
                all_errors.append("JSON issues:")
                all_errors.extend([f"  - {x}" for x in json_issues])
        else:
            print(f"✅ {env}: OK")

    if all_errors:
        eprint("\n".join(all_errors))
        return 1

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
