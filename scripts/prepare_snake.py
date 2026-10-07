"""Decorate Platane's real contribution route with an expressive, growing snake.

No route or contribution values are invented. Growth is a bounded visual trail,
not a replacement game solver. This runs after the pinned upstream generator.
"""

from bisect import bisect_right
from math import atan2, ceil, degrees, hypot
from statistics import median
from pathlib import Path
import re
import xml.etree.ElementTree as ET

NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)
VERSION = "3"


def element(parent, tag, **attributes):
    return ET.SubElement(parent, f"{{{NS}}}{tag}", {k.rstrip("_").replace("_", "-"): str(v) for k, v in attributes.items()})


def keyframes(css):
    return dict(re.findall(r"@keyframes\s+([\w-]+)\{((?:[^{}]|\{[^{}]*\})*)\}", css))


def parse_route(css):
    body = keyframes(css).get("s0", "")
    route = {}
    for selectors, x, y in re.findall(r"([^{}]+)\{transform:translate\((-?[\d.]+)px,(-?[\d.]+)px\)\}", body):
        for time in selectors.split(","):
            route[float(time.strip().rstrip("%"))] = (float(x), float(y))
    if 0 not in route or len(route) < 2:
        raise ValueError("Upstream snake head route is missing or has changed")
    route[100.0] = route[0.0]
    return sorted(route.items())


def position(route, time):
    time %= 100
    times = [t for t, _ in route]
    i = max(0, bisect_right(times, time) - 1)
    a, (x, y) = route[i]
    b, (nx, ny) = route[min(i + 1, len(route) - 1)]
    ratio = (time - a) / (b - a) if b > a else 0
    return x + (nx - x) * ratio, y + (ny - y) * ratio


def trailing_frames(route, lag):
    points = {(t + lag) % 100: xy for t, xy in route[:-1]}
    points[0] = points[100] = position(route, -lag)
    return "".join(f"{t:.5f}%{{transform:translate({x:.3f}px,{y:.3f}px)}}" for t, (x, y) in sorted(points.items()))


def pulses(times, property_name, idle, peak, before, after):
    points = {0: idle, 100: idle}
    for time in times:
        points[max(0, time - before)] = idle
        points[time] = peak
        points[min(99.9, time + after)] = idle
    return "".join(f"{t:.5f}%{{{property_name}:{value}}}" for t, value in sorted(points.items()))


def decorate(path):
    tree = ET.parse(path)
    root = tree.getroot()
    if root.get("data-snake-character") == VERSION:
        return
    if root.get("data-snake-character") is not None:
        raise ValueError("Generate a fresh upstream SVG before changing decoration versions")
    style = root.find(f"{{{NS}}}style")
    if style is None:
        raise ValueError(f"Missing animation stylesheet: {path}")
    css = style.text or ""
    route = parse_route(css)
    duration_match = re.search(r"\.s\{[^}]*?(\d+)ms", css)
    if duration_match is None:
        raise ValueError("Upstream snake animation duration is missing")
    duration = int(duration_match[1])
    frames = keyframes(css)
    # Each cell animation clears the actual contribution square at this time.
    food = []
    for cell in root.findall(f"{{{NS}}}rect"):
        classes = cell.get("class", "").split()
        if len(classes) == 2 and classes[0] == "c":
            match = re.search(r"([\d.]+)%,100%\{fill:var\(--ce\)\}", frames.get(classes[1], ""))
            if match:
                food.append((float(match[1]), float(cell.get("x")) + 6, float(cell.get("y")) + 6))
    food.sort()
    # Preserve the contribution grid; remove the upstream collection/progress bar.
    css = re.sub(r"@keyframes\s+u[\w-]*\{((?:[^{}]|\{[^{}]*\})*)\}", "", css)
    css = re.sub(r"\.u(?:\.u[\w-]+)?\{[^}]*\}", "", css)
    root.set("height", "160")
    root.set("viewBox", "-16 -32 880 160")
    for node in list(root):
        if node.get("class", "").split()[:1] in (["s"], ["u"]):
            root.remove(node)
    extra = [f".snake-trail{{fill:var(--cs);stroke:none;animation-duration:{duration}ms;animation-timing-function:linear;animation-iteration-count:infinite}}"]
    # Use route speed so daily path duration does not alter body-piece spacing.
    speeds = [hypot(bx-ax, by-ay) / (bt-at) for (at, (ax, ay)), (bt, (bx, by)) in zip(route, route[1:]) if bt > at and (ax, ay) != (bx, by)]
    half_cell_lag = 8 / median(speeds)
    # Eight overlapping half-cell pieces begin at four cells long; at most 12 cells.
    base, growing = 8, min(16, len(food))
    for index in reversed(range(base + growing)):
        lag = (index + 1) * half_cell_lag
        x, y = position(route, -lag)
        name = f"trail{index}"
        moving = element(root, "g", class_="snake-trail")
        moving.set("style", f"transform:translate({x:.3f}px,{y:.3f}px);animation-name:{name}")
        extra.append(f"@keyframes {name}{{{trailing_frames(route,lag)}}}")
        visible = element(moving, "g")
        if index >= base:
            ordinal = index - base + 1
            trigger = food[ceil(ordinal * len(food) / growing) - 1][0]
            grow_name = f"growth{index}"
            visible.set("class", "snake-growth")
            visible.set("style", f"animation-name:{grow_name}")
            fade_start = max(97.0, trigger)
            fade_end = min(100.0, max(99.5, fade_start + .1))
            extra.append(f"@keyframes {grow_name}{{0%,{max(0,trigger-.08):.5f}%{{opacity:0}}{trigger:.5f}%,{fade_start:.5f}%{{opacity:1}}{fade_end:.5f}%,100%{{opacity:0}}}}")
        radius = 6.2 - 2.4 * index / max(1, base + growing - 1)
        element(visible, "circle", cx=8, cy=8, r=f"{radius:.2f}")
    extra.append(f".snake-growth{{opacity:0;animation-duration:{duration}ms;animation-timing-function:linear;animation-iteration-count:infinite}}")
    # Short rings at the consumed cell are synchronized with its upstream clearing.
    for index, (time, x, y) in enumerate(food):
        name = f"meal{index}"
        ring = element(root, "circle", cx=x, cy=y, r=7, fill="none", stroke="var(--cs)", stroke_width=1, opacity=0)
        ring.set("style", f"animation:{name} {duration}ms linear infinite")
        extra.append(f"@keyframes {name}{{{pulses([time], 'opacity', '0', '.3', .10, .48)}}}")
    head = element(root, "g");head.set("class", "s s0")
    face = element(head, "g");face.set("class", "snake-face")
    angle_points = []
    for index, (time, (x, y)) in enumerate(route[:-1]):
        nx, ny = route[index + 1][1]
        if (x, y) != (nx, ny):
            angle_points.append((time, degrees(atan2(ny-y, nx-x))))
    if not angle_points:
        raise ValueError("Snake route has no movement")
    orientation = "".join(f"{t:.5f}%{{transform:rotate({a:g}deg)}}" for t, a in angle_points)
    orientation += f"100%{{transform:rotate({angle_points[0][1]:g}deg)}}"
    extra.append(f".snake-face{{transform:rotate({angle_points[0][1]:g}deg);transform-origin:8px 8px;animation:heading {duration}ms step-end infinite}}@keyframes heading{{{orientation}}}")
    # A flat rounded head and dot eyes keep the character friendly and simple.
    element(face, "ellipse", cx=8, cy=8, rx=8.4, ry=7, fill="var(--cs)")
    for cy in (4.6, 11.4):
        element(face, "circle", cx=10.5, cy=cy, r=1.35, fill="#203143")
    tongue = element(face, "path", d="M15.8 8h4.2m0 0 2.3-1.3m-2.3 1.3 2.3 1.3", fill="none", stroke="#e5a4b0", stroke_width=1, stroke_linecap="round")
    tongue.set("class", "snake-tongue")
    extra.append(".snake-tongue{opacity:0;transform-origin:15.8px 8px;animation:taste 3100ms ease-in-out infinite}@keyframes taste{0%,62%,100%{opacity:0;transform:scaleX(.3)}68%,76%{opacity:1;transform:scaleX(1)}72%{opacity:1;transform:scaleX(.7)}82%{opacity:0;transform:scaleX(.3)}}")
    extra.append("@media(prefers-reduced-motion:reduce){*{animation:none!important}.snake-growth,.snake-tongue{opacity:0!important}}")
    style.text = css + "".join(extra)
    root.set("data-snake-character", VERSION)
    root.set("data-food-cells", str(len(food)))
    root.set("data-initial-body-pieces", str(base))
    root.set("data-max-body-pieces", str(base + growing))
    desc = root.find(f"{{{NS}}}desc")
    desc.text = "Contribution route generated by Platane/snk. Soft dot eyes, a small forked tongue, subtle eating rings and bounded growth by Onur Ergüden. Growth follows consumed contribution squares; animation respects reduced motion."
    tree.write(path, encoding="unicode")
    print(f"{path}: {len(food)} food cells, {base} to {base+growing} body pieces, {duration}ms loop")


if __name__ == "__main__":
    for theme in ("light", "dark"):
        decorate(Path(f"assets/contribution-snake-soft-{theme}.svg"))
