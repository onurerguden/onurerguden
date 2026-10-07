"""Honor visitors' reduced-motion preference in generated contribution snakes."""

from pathlib import Path
import xml.etree.ElementTree as ET

ET.register_namespace("", "http://www.w3.org/2000/svg")
for theme in ("light", "dark"):
    path = Path(f"assets/snake-{theme}.svg")
    tree = ET.parse(path)
    style = tree.find("{http://www.w3.org/2000/svg}style")
    if style is None:
        raise ValueError(f"Missing animation stylesheet: {path}")
    rule = "@media(prefers-reduced-motion:reduce){*{animation:none!important}}"
    if rule not in (style.text or ""):
        style.text = (style.text or "") + rule
    tree.write(path, encoding="unicode")
