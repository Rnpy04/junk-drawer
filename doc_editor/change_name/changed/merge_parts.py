
from __future__ import annotations

import glob
import os
import re
import sys

UUID_HEX = re.compile(r"^([0-9a-f]{32})(?:\.part\d+)?$", re.IGNORECASE)


def _extract_uuid(arg: str) -> str:
    base = os.path.basename(arg.strip())
    m = UUID_HEX.match(base)
    if m:
        return m.group(1).lower()
    if re.fullmatch(r"[0-9a-f]{32}", base, re.IGNORECASE):
        return base.lower()
    raise SystemExit(
        "نام معتبر نیست. یکی از پارت‌ها (مثلاً abc...def.part01) یا خود UUID سی‌ودوکاراکتری hex را بدهید."
    )


def _part_sort_key(path: str) -> int:
    m = re.search(r"\.part(\d+)$", os.path.basename(path), re.IGNORECASE)
    return int(m.group(1)) if m else 0


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__.strip())
        sys.exit(1)
    arg = sys.argv[1]
    uid = _extract_uuid(arg)
    if os.path.isfile(arg):
        base_dir = os.path.dirname(os.path.abspath(arg))
    else:
        base_dir = os.getcwd()
    pattern = os.path.join(base_dir, f"{uid}.part*")
    parts = sorted(glob.glob(pattern), key=_part_sort_key)
    if not parts:
        print(f"هیچ پارتی برای UUID «{uid}» در «{base_dir}» پیدا نشد.", file=sys.stderr)
        sys.exit(2)
    out_zip = os.path.join(base_dir, f"{uid}.zip")
    with open(out_zip, "wb") as out:
        for p in parts:
            with open(p, "rb") as inf:
                out.write(inf.read())
    with open(out_zip, "rb") as f:
        header = f.read(4)
    if header[:2] != b"PK":
        alt = os.path.join(base_dir, f"{uid}.merged")
        try:
            os.replace(out_zip, alt)
        except OSError:
            os.rename(out_zip, alt)
        out_zip = alt
        print(f"نوشت: {out_zip} (امضای ZIP دیده نشد؛ در صورت نیاز پسوند را خودتان عوض کنید)")
    else:
        print(f"نوشت: {out_zip}")
    print(f"از {len(parts)} پارت به‌هم چسبانده شد.")


if __name__ == "__main__":
    main()
