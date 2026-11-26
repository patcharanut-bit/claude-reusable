#!/usr/bin/env python3
"""Figma node JSON -> flat spec table (padding / gap / color / font / text).

Usage:  python3 -I parse_figma.py node.json
Input:  the response body of GET /v1/files/<key>/nodes?ids=<node>
Prints every node with its auto-layout, padding, spacing, colors and text style
so you can map exact values into React Native instead of eyeballing a screenshot.
"""
import json
import sys


def rgba(c):
    if not c:
        return ""
    r, g, b = round(c.get("r", 0) * 255), round(c.get("g", 0) * 255), round(c.get("b", 0) * 255)
    a = c.get("a", 1)
    return f"#{r:02X}{g:02X}{b:02X}" + (f" a={a:.2f}" if a < 1 else "")


def fill_str(fills):
    out = []
    for f in fills or []:
        if f.get("visible", True) is False:
            continue
        if f.get("type") == "SOLID":
            out.append(rgba(f.get("color")))
        elif "GRADIENT" in f.get("type", ""):
            out.append(f.get("type"))
    return ",".join(out)


def walk(n, d=0):
    ind = "  " * d
    t, name = n.get("type"), n.get("name", "")
    bb = n.get("absoluteBoundingBox") or {}
    rb = n.get("absoluteRenderBounds") or {}
    size = f'{round(bb.get("width", 0))}x{round(bb.get("height", 0))}' if bb else ""
    print(f'{ind}[{t}] "{name}" {size}')

    # overflow hint: rendered box taller/wider than the layout box
    if bb and rb and (round(rb.get("height", 0)) > round(bb.get("height", 0))
                      or round(rb.get("width", 0)) > round(bb.get("width", 0))):
        print(f'{ind}   render {round(rb.get("width",0))}x{round(rb.get("height",0))} (overflows layout box)')

    lm = n.get("layoutMode")
    if lm and lm != "NONE":
        pad = f'pad(T{n.get("paddingTop",0)} R{n.get("paddingRight",0)} B{n.get("paddingBottom",0)} L{n.get("paddingLeft",0)})'
        print(f'{ind}   AUTO={lm} gap={n.get("itemSpacing",0)} {pad} align={n.get("primaryAxisAlignItems","")}/{n.get("counterAxisAlignItems","")}')

    if n.get("cornerRadius") is not None:
        print(f'{ind}   radius={n.get("cornerRadius")}')
    elif n.get("rectangleCornerRadii"):
        print(f'{ind}   radii={n.get("rectangleCornerRadii")}')

    fs = fill_str(n.get("fills"))
    if fs:
        print(f'{ind}   fill={fs}')
    st = fill_str(n.get("strokes"))
    if st:
        print(f'{ind}   stroke={st} w={n.get("strokeWeight","")}')

    if t == "TEXT":
        s = n.get("style", {})
        print(f'{ind}   TEXT="{n.get("characters","")}" font={s.get("fontFamily","")} {s.get("fontWeight","")} '
              f'size={s.get("fontSize","")} lh={s.get("lineHeightPx","")} ls={s.get("letterSpacing","")} color={fs}')

    for c in n.get("children", []):
        walk(c, d + 1)


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: python3 -I parse_figma.py node.json")
    data = json.load(open(sys.argv[1]))
    for entry in data.get("nodes", {}).values():
        walk(entry["document"])


if __name__ == "__main__":
    main()
