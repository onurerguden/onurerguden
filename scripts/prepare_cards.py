"""Produce readable narrow cards from the same generated public GitHub data."""

from pathlib import Path
import xml.etree.ElementTree as ET

NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)


def add(root, tag, text=None, **attributes):
    node = ET.SubElement(root, f"{{{NS}}}{tag}", {k.replace("_", "-"): str(v) for k, v in attributes.items()})
    node.text = text
    return node


def card(title, description, theme):
    dark = theme == "dark"
    root = ET.Element(f"{{{NS}}}svg", {"width": "330", "height": "180", "viewBox": "0 0 330 180", "role": "img"})
    add(root, "title", title)
    add(root, "desc", description)
    add(root, "rect", x=.5, y=.5, width=329, height=179, rx=12, fill="#080e1c" if dark else "#ffffff", stroke="#30363d" if dark else "#d0d7de")
    add(root, "style", f"text{{font-family:'Segoe UI',Ubuntu,sans-serif;fill:{'#c9d1d9' if dark else '#24292f'}}}.title{{font-size:17px;font-weight:600;fill:{'#7fc8ff' if dark else '#235a83'}}}.label{{font-size:13px}}.value{{font-size:14px;font-weight:600}}")
    add(root, "text", title, x=24, y=32, **{"class": "title"})
    return root


def build(theme):
    stats = ET.parse(f"assets/activity-{theme}.svg").getroot()
    values = {n.get("data-testid"): (n.text or "").strip() for n in stats.iter() if n.tag.endswith("text")}
    keys = ("stars", "commits", "prs", "prs_merged")
    if any(not values.get(key) for key in keys):
        raise ValueError("Generated stats structure changed")
    labels = ("Stars", "Commits (last year)", "Pull requests", "Merged pull requests")
    description = ", ".join(f"{label}: {values[key]}" for key, label in zip(keys, labels))
    root = card("GitHub activity", description, theme)
    for index, (key, label) in enumerate(zip(keys, labels)):
        y = 65 + index * 26
        add(root, "text", label, x=24, y=y, **{"class": "label"})
        add(root, "text", values[key], x=306, y=y, text_anchor="end", **{"class": "value"})
    ET.ElementTree(root).write(f"assets/activity-narrow-{theme}.svg", encoding="unicode")

    languages = ET.parse(f"assets/code-languages-{theme}.svg").getroot()
    names = [(n.text or "").strip() for n in languages.iter() if n.get("data-testid") == "lang-name"]
    colors = [n.get("fill") for n in languages.iter() if n.tag.endswith("circle")]
    bars = [n for n in languages.iter() if n.get("data-testid") == "lang-progress"]
    if len(names) != 6 or len(colors) != 6 or len(bars) != 6:
        raise ValueError("Generated language card structure changed")
    root = card("Languages in public repos", "; ".join(names) + ". Code size, not proficiency.", theme)
    total = sum(float(b.get("width")) for b in bars)
    x = 24
    for bar in bars:
        width = float(bar.get("width")) / total * 282
        add(root, "rect", x=f"{x:.3f}", y=50, width=f"{width:.3f}", height=8, fill=bar.get("fill"))
        x += width
    for index, (name, color) in enumerate(zip(names, colors)):
        x = 24 if index < 3 else 181
        y = 84 + (index % 3) * 26
        add(root, "circle", cx=x+3, cy=y-4, r=3, fill=color)
        add(root, "text", name, x=x+12, y=y, **{"class": "label"})
    ET.ElementTree(root).write(f"assets/code-languages-narrow-{theme}.svg", encoding="unicode")
    print(f"{theme}: generated narrow cards from existing stats and language values")


if __name__ == "__main__":
    for theme in ("light", "dark"):
        build(theme)
