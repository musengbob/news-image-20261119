#!/usr/bin/env python3
"""Compose the 19 November 2026 front page: masthead, three leads, hero
illustration, 33 more verified stories in three columns, and a world-map
panel with 12 numbered markers. Output: entry.png, 1024x1024, PNG."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/liberation"

INK = (17, 17, 17)
PAPER = (247, 243, 234)
RED = (178, 34, 34)
GREY = (90, 88, 82)
RULE = (150, 146, 136)
SEA = (214, 228, 238)
LAND = (46, 74, 98)
MAPINK = (30, 30, 30)

def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

F_NAME = lambda s: font("LiberationSerif-Bold.ttf", s)
F_HEAD = lambda s: font("LiberationSerif-Bold.ttf", s)
F_SANSB = lambda s: font("LiberationSans-Bold.ttf", s)
F_SANS = lambda s: font("LiberationSans-Regular.ttf", s)
F_SERIFI = lambda s: font("LiberationSerif-Italic.ttf", s)

def fit_text(draw, text, fname, size, max_w):
    """Return a font of fname at the largest size <= size that fits max_w."""
    s = size
    while s > 7:
        f = font(fname, s)
        if draw.textlength(text, font=f) <= max_w:
            return f
        s -= 1
    return font(fname, 7)

def wrap(draw, text, f, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

# ---------------------------------------------------------------- stories
LEAD_DECK = (
    "The first trilateral summit of the three leaders opens at APEC as "
    "Iran strikes a U.S. base in Kuwait and Vice City opens its doors."
)

COLUMNS = [
    ("WAR & DIPLOMACY", RED, [
        ("EU plans \u20ac45bn loan for Kyiv", "Repaid only once Russia pays reparations, Brussels proposes."),
        ("Russia plans 20m drones for 2027", "EU defence chief warns of doubled drone output for Ukraine war."),
        ("Israeli tanks push into central Gaza", "First ground operation since the ceasefire began, dozens flee."),
        ("Somalia accuses UAE of secret bases", "Mogadishu says Abu Dhabi built bases without federal approval."),
        ("Australia sanctions Israeli settlers", "Canberra acts over West Bank expansion by settlers and groups."),
        ("Saudi Arabia: danger has passed", "Alerts lifted in three southern cities, Riyadh says."),
        ("LPG tanker off Bulgaria is hit", "Vessel struck by projectiles off the Black Sea coast, officials say."),
        ("Qatar's emir meets Merz in Berlin", "Steinmeier and the chancellor receive Sheikh Tamim on state visit."),
        ("EU\u2013Western Balkans summit opens", "Leaders gather in Brussels as the General Affairs Council meets."),
        ("APEC leaders hold plenary", "Shenzhen hosts the leaders' session as Korea's Lee wraps his visit."),
        ("Kuwait calls strikes 'dangerous'", "Iran attacks 'undermine diplomacy', Kuwait's foreign ministry says."),
    ]),
    ("AMERICAS & MARKETS", RED, [
        ("Jeffries set to be first Black Speaker", "Democrats nominate Hakeem Jeffries to lead the House."),
        ("Peltola wins Alaska Senate seat", "Democrat's victory gives the party a 56\u201344 Senate majority."),
        ("Liu Yunping takes caucus chair", "First Taiwanese American to chair the House Democratic Caucus."),
        ("U.S. tightens green-card rules", "Tougher employment-based rules mean a longer hiring process."),
        ("Senators warn on AI cyber threats", "AI-enabled attacks are outpacing U.S. defences, senators tell Trump."),
        ("NSA network suffers outage", "Classified internal communications go down, disrupting spy work."),
        ("Nvidia chief promises early rises", "Acting CEO Kress pledges December pay rises and more stock grants."),
        ("Nvidia halts H-series chips to China", "Hopper shipments to the mainland stop, earnings call confirms."),
        ("Anthropic starts Nasdaq trading", "AI lab lists after a $64.35bn IPO priced on Wednesday."),
        ("Fed minutes point to more hikes", "Most officials expect further rate rises, October minutes show."),
        ("Oil prices fall on Gulf tensions", "Risk aversion outweighs supply fears as markets turn volatile."),
    ]),
    ("ASIA, SCIENCE & SPORT", RED, [
        ("Cyclone Akvan nears India's coast", "Landfall expected between Machilipatnam and Puri; railways on alert."),
        ("India and Japan open 2+2 talks", "Defence and foreign ministers review ties in Tokyo."),
        ("COP31 talks continue in Antalya", "India demands climate justice and delivery of climate finance."),
        ("Modi meets William and Kate", "Prince and Princess of Wales wrap their three-day India visit."),
        ("Deutsche Bank's $582m Epstein link", "Bank handled Epstein-linked deals in 2013\u201318, expos\u00e9 finds."),
        ("Voyager 1 reaches one light-day", "NASA to confirm the 50-year probe's milestone on Thursday."),
        ("Earth's 'missing' billion years", "Scientists may have found why a billion years of geology vanished."),
        ("Islam 'to be largest faith by 2035'", "Pew report projects Islam overtaking Christianity within a decade."),
        ("Lula faces Fl\u00e1vio Bolsonaro", "Brazil rivals clash before Sunday's run-off; polls tied 50\u201350."),
        ("Duckett's 133 lifts England", "Opener puts England on top in the third ODI against Australia."),
        ("Cocaine and pills seized in Libya", "Eastern Libya haul includes millions of pills, officials say."),
    ]),
]

MARKERS = [
    (1, "SHENZHEN", 114.1, 22.5),
    (2, "KUWAIT", 48.0, 29.4),
    (3, "GAZA", 34.5, 31.5),
    (4, "KYIV", 30.5, 50.5),
    (5, "WASHINGTON", -77.0, 38.9),
    (6, "MUMBAI", 72.9, 19.1),
    (7, "BRAS\u00cdLIA", -47.9, -15.8),
    (8, "CANBERRA", 149.1, -35.3),
    (9, "ANTALYA", 30.7, 36.9),
    (10, "BERLIN", 13.4, 52.5),
    (11, "ANCHORAGE", -149.9, 61.2),
    (12, "MOGADISHU", 45.3, 2.0),
]

# Simplified continent outlines (lon, lat), equirectangular.
CONTINENTS = [
    [(-168, 66), (-150, 70), (-135, 70), (-125, 71), (-110, 68), (-95, 69),
     (-85, 70), (-80, 73), (-70, 62), (-60, 60), (-55, 52), (-60, 46),
     (-65, 44), (-70, 42), (-75, 35), (-80, 26), (-84, 30), (-90, 21),
     (-97, 16), (-104, 18), (-105, 23), (-112, 29), (-120, 34), (-125, 42),
     (-125, 49), (-132, 56), (-145, 60), (-158, 58), (-165, 60), (-168, 66)],
    [(-79, 9), (-72, 12), (-62, 9), (-52, 5), (-50, 0), (-44, -3),
     (-35, -8), (-39, -15), (-41, -23), (-48, -28), (-54, -34), (-58, -38),
     (-65, -41), (-68, -50), (-70, -54), (-73, -50), (-73, -37), (-71, -30),
     (-70, -19), (-75, -15), (-80, -6), (-81, 2), (-79, 9)],
    [(-17, 15), (-16, 21), (-10, 30), (-6, 34), (0, 36), (10, 37),
     (11, 34), (20, 32), (25, 32), (30, 31), (32, 31), (35, 28),
     (38, 22), (43, 12), (48, 11), (51, 12), (48, 5), (41, -2),
     (40, -10), (36, -18), (33, -26), (28, -33), (20, -35), (17, -32),
     (14, -22), (12, -18), (13, -12), (9, -1), (9, 4), (0, 6),
     (-8, 5), (-13, 8), (-17, 15)],
    [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (-2, 48), (0, 50),
     (2, 51), (5, 53), (8, 55), (8, 58), (11, 58), (18, 56),
     (21, 55), (24, 58), (26, 60), (30, 62), (30, 70), (35, 68),
     (40, 68), (44, 68), (48, 69), (55, 69), (60, 69), (55, 65),
     (50, 60), (45, 55), (40, 52), (35, 50), (30, 48), (28, 46),
     (25, 45), (23, 40), (20, 42), (16, 44), (12, 44), (8, 44),
     (3, 43), (0, 40), (-2, 37), (-6, 36), (-10, 36)],
    [(30, 70), (40, 68), (50, 69), (60, 69), (70, 72), (80, 73),
     (95, 76), (110, 76), (125, 73), (140, 72), (155, 70), (170, 67),
     (178, 65), (170, 60), (162, 58), (158, 53), (150, 60), (142, 50),
     (141, 44), (140, 39), (135, 34), (130, 33), (127, 35), (124, 40),
     (121, 38), (120, 32), (118, 25), (112, 22), (108, 18), (105, 10),
     (101, 8), (98, 12), (97, 16), (94, 17), (92, 21), (89, 22),
     (86, 20), (83, 17), (80, 13), (77, 8), (75, 15), (73, 20),
     (70, 22), (66, 25), (61, 25), (57, 26), (52, 28), (50, 30),
     (48, 30), (44, 29), (40, 32), (36, 36), (33, 36), (30, 36),
     (30, 42), (33, 45), (38, 47), (42, 50), (46, 55), (48, 60),
     (44, 65), (40, 68), (30, 70)],
    [(113, -22), (114, -28), (115, -33), (118, -35), (124, -33), (129, -32),
     (134, -33), (137, -35), (140, -38), (144, -38), (147, -39), (150, -37),
     (153, -32), (153, -27), (150, -23), (146, -19), (142, -11), (137, -12),
     (132, -12), (127, -14), (122, -17), (118, -20), (113, -22)],
]

def lonlat_to_xy(lon, lat, x0, y0, x1, y1):
    x = x0 + (lon + 180.0) / 360.0 * (x1 - x0)
    y = y0 + (75.0 - lat) / 130.0 * (y1 - y0)
    return x, y

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 24
    rx = W - mx

    # --- masthead
    f_name = fit_text(d, "THE WORLD TODAY", "LiberationSerif-Bold.ttf", 62, rx - mx)
    d.text((W / 2, 14), "THE WORLD TODAY", font=f_name, fill=INK, anchor="ma")
    f_small = font("LiberationSans-Bold.ttf", 10)
    d.text((mx, 20), "EST. 2026", font=f_small, fill=GREY, anchor="la")
    d.text((rx, 20), "ONE DAY \u2022 ONE PAGE", font=f_small, fill=GREY, anchor="ra")
    d.line([(mx, 82), (rx, 82)], fill=RED, width=4)
    # --- date strip
    f_date = font("LiberationSerif-Bold.ttf", 19)
    d.text((mx, 90), "THURSDAY, 19 NOVEMBER 2026", font=f_date, fill=INK, anchor="la")
    f_tag = font("LiberationSans-Bold.ttf", 11)
    d.text((rx, 94), "36 STORIES \u2022 SIX CONTINENTS", font=f_tag, fill=RED, anchor="ra")
    d.line([(mx, 114), (rx, 114)], fill=RULE, width=1)

    # --- lead headlines
    f_lead = fit_text(d, "TRUMP, XI AND PUTIN MEET IN SHENZHEN",
                      "LiberationSerif-Bold.ttf", 37, rx - mx)
    d.text((W / 2, 122), "THREE LEADERS, ONE TABLE", font=f_lead, fill=INK, anchor="ma")
    f_lead2 = fit_text(d, "TRUMP, XI AND PUTIN MEET IN SHENZHEN",
                       "LiberationSerif-Bold.ttf", 37, rx - mx)
    d.text((W / 2, 160), "TRUMP, XI AND PUTIN MEET IN SHENZHEN",
           font=f_lead2, fill=INK, anchor="ma")
    f_sub = fit_text(d, "IRAN HITS U.S. BASE IN KUWAIT  \u2022  VICE CITY OPENS AS GTA VI LAUNCHES",
                     "LiberationSans-Bold.ttf", 15, rx - mx)
    d.text((W / 2, 204), "IRAN HITS U.S. BASE IN KUWAIT  \u2022  VICE CITY OPENS AS GTA VI LAUNCHES",
           font=f_sub, fill=RED, anchor="ma")
    f_deck = font("LiberationSerif-Italic.ttf", 14)
    deck_lines = wrap(d, LEAD_DECK, f_deck, rx - mx)
    y = 224
    for ln in deck_lines:
        d.text((W / 2, y), ln, font=f_deck, fill=(60, 58, 52), anchor="ma")
        y += 18

    # --- hero image
    hero = Image.open(os.path.join(HERE, "hero.webp")).convert("RGB")
    hx0, hy0, hx1, hy1 = mx, 262, rx, 432
    hw, hh = hx1 - hx0, hy1 - hy0
    scale = max(hw / hero.width, hh / hero.height)
    nw, nh = int(hero.width * scale), int(hero.height * scale)
    hero = hero.resize((nw, nh), Image.LANCZOS)
    ox, oy = (nw - hw) // 2, (nh - hh) // 2
    img.paste(hero.crop((ox, oy, ox + hw, oy + hh)), (hx0, hy0))
    d.rectangle([hx0, hy0, hx1, hy1], outline=INK, width=2)
    f_cap = font("LiberationSerif-Italic.ttf", 11)
    d.text((mx, 438), "Leaders shake hands in Shenzhen as warships gather in the Gulf "
           "and neon lights up Vice City.  (Illustration)",
           font=f_cap, fill=GREY, anchor="la")
    d.line([(mx, 456), (rx, 456)], fill=RULE, width=1)

    # --- three story columns
    col_w = (rx - mx - 2 * 18) / 3
    f_sect = font("LiberationSans-Bold.ttf", 13)
    y_top = 464
    for i, (title, color, stories) in enumerate(COLUMNS):
        x0 = mx + i * (col_w + 18)
        x1 = x0 + col_w
        d.text((x0, y_top), title, font=f_sect, fill=color, anchor="la")
        d.line([(x0, y_top + 18), (x1, y_top + 18)], fill=color, width=2)
        y = y_top + 26
        for hl, dk in stories:
            fh = fit_text(d, hl, "LiberationSans-Bold.ttf", 11, col_w)
            d.text((x0, y), hl, font=fh, fill=INK, anchor="la")
            y += 13
            fd = fit_text(d, dk, "LiberationSans-Regular.ttf", 8, col_w)
            d.text((x0, y), dk, font=fd, fill=(70, 68, 62), anchor="la")
            y += 11
            d.line([(x0, y + 1), (x1, y + 1)], fill=(215, 210, 198), width=1)
            y += 4
    d.line([(mx, 806), (rx, 806)], fill=RULE, width=1)

    # --- map panel
    f_maph = font("LiberationSans-Bold.ttf", 12)
    d.text((mx, 812), "THE WORLD IN ONE MAP \u2014 12 PLACES THAT MADE THE DAY",
           font=f_maph, fill=INK, anchor="la")
    d.text((rx, 812), "19 NOV 2026", font=f_maph, fill=RED, anchor="ra")
    mx0, my0, mx1, my1 = mx, 832, rx, 962
    d.rectangle([mx0, my0, mx1, my1], fill=SEA, outline=INK, width=1)
    for poly in CONTINENTS:
        pts = [lonlat_to_xy(lo, la, mx0 + 4, my0 + 4, mx1 - 4, my1 - 4) for lo, la in poly]
        d.polygon(pts, fill=LAND)
    f_num = font("LiberationSans-Bold.ttf", 9)
    f_lab = font("LiberationSans-Bold.ttf", 8)
    # Labels only for well-separated markers; the crowded Europe/Middle East
    # cluster is number-only (the footer legend names every marker).
    LABELED = {1, 5, 6, 7, 8, 11, 12}
    for num, name, lon, lat in MARKERS:
        cx, cy = lonlat_to_xy(lon, lat, mx0 + 4, my0 + 4, mx1 - 4, my1 - 4)
        r = 7
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED, outline=(255, 255, 255), width=1)
        d.text((cx, cy - 1), str(num), font=f_num, fill=(255, 255, 255), anchor="mm")
        if num not in LABELED:
            continue
        lx = cx + 11 if cx < (mx0 + mx1) / 2 else cx - 11
        anchor = "lm" if cx < (mx0 + mx1) / 2 else "rm"
        d.text((lx, cy), name, font=f_lab, fill=MAPINK, anchor=anchor,
               stroke_width=2, stroke_fill=SEA)

    # --- footer legend + colophon
    legend = ("MAP:  1 Shenzhen  \u00b7  2 Kuwait  \u00b7  3 Gaza  \u00b7  4 Kyiv  \u00b7  "
              "5 Washington  \u00b7  6 Mumbai  \u00b7  7 Bras\u00edlia  \u00b7  8 Canberra  \u00b7  "
              "9 Antalya  \u00b7  10 Berlin  \u00b7  11 Anchorage  \u00b7  12 Mogadishu")
    f_leg = fit_text(d, legend, "LiberationSans-Regular.ttf", 10, rx - mx)
    d.text((W / 2, 970), legend, font=f_leg, fill=(70, 68, 62), anchor="ma")
    d.line([(mx, 992), (rx, 992)], fill=RULE, width=1)
    f_foot = font("LiberationSans-Bold.ttf", 9)
    d.text((mx, 998), "THE WORLD TODAY \u2014 THURSDAY 19 NOVEMBER 2026",
           font=f_foot, fill=GREY, anchor="la")
    d.text((rx, 998), "36 VERIFIED STORIES \u2022 SIX CONTINENTS",
           font=f_foot, fill=GREY, anchor="ra")

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")

if __name__ == "__main__":
    main()
