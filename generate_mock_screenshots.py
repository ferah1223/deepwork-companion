from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path

W, H = 1600, 1200
ROOT = Path(__file__).resolve().parent
OUTDIR = ROOT / 'screenshots_v2'
OUTDIR.mkdir(parents=True, exist_ok=True)

FONT_TITLE_CANDIDATES = [
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    '/Library/Fonts/Arial Bold.ttf',
    'C:/Windows/Fonts/arialbd.ttf',
]
FONT_BODY_CANDIDATES = [
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    '/Library/Fonts/Arial.ttf',
    'C:/Windows/Fonts/arial.ttf',
]


def resolve_font(candidates):
    for candidate in candidates:
        if Path(candidate).exists():
            return candidate
    return None


FONT_TITLE = resolve_font(FONT_TITLE_CANDIDATES)
FONT_BODY = resolve_font(FONT_BODY_CANDIDATES)


def font(size, bold=False):
    font_path = FONT_TITLE if bold else FONT_BODY
    if font_path:
        return ImageFont.truetype(font_path, size)
    return ImageFont.load_default()


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def add_blob(img, x, y, r, color):
    blob = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(blob)
    bdraw.ellipse((x - r, y - r, x + r, y + r), fill=color)
    blob = blob.filter(ImageFilter.GaussianBlur(48))
    return Image.alpha_composite(img, blob)


def make_background():
    base = Image.new('RGBA', (W, H), '#0a0f1d')
    base = add_blob(base, 220, 140, 260, (120, 93, 255, 120))
    base = add_blob(base, 1370, 160, 220, (80, 215, 255, 90))
    base = add_blob(base, 1180, 920, 300, (116, 108, 255, 70))
    return base


def create_shadow(size, radius=32, alpha=90):
    w, h = size
    shadow = Image.new('RGBA', (w + 80, h + 80), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle((40, 32, 40 + w, 32 + h), radius=radius, fill=(0, 0, 0, alpha))
    return shadow.filter(ImageFilter.GaussianBlur(24))


def draw_chip(draw, box, text, active=False):
    fill = (20, 62, 88, 255) if active else (255, 255, 255, 18)
    outline = (100, 220, 255, 255) if active else (255, 255, 255, 30)
    rounded(draw, box, 22, fill, outline, 1)
    draw.text((box[0] + 16, box[1] + 11), text, fill=(237, 243, 255), font=font(14))


def draw_window_bar(draw, title='Deepwork Companion', url='localhost:5173'):
    rounded(draw, (250, 82, 1350, 126), 16, (236, 239, 246, 255))
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        x = 278 + i * 18
        draw.ellipse((x, 97, x + 10, 107), fill=c)
    rounded(draw, (360, 92, 1240, 116), 10, (248, 249, 252, 255), (215, 219, 228, 255), 1)
    draw.text((392, 95), url, fill=(109, 117, 133), font=font(13))
    draw.text((1288, 95), title, fill=(109, 117, 133), font=font(13))


def draw_browser_mockup(state):
    img = make_background()

    # soft device/browser shadow
    mock_shadow = create_shadow((1100, 860), 24, 110)
    img.alpha_composite(mock_shadow, (210, 92))

    browser = Image.new('RGBA', (1100, 860), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(browser)
    rounded(bdraw, (0, 0, 1100, 860), 22, (229, 233, 241, 255))
    rounded(bdraw, (0, 44, 1100, 860), 0, (12, 18, 34, 255))

    # top browser chrome
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        x = 24 + i * 18
        bdraw.ellipse((x, 16, x + 10, 26), fill=c)
    rounded(bdraw, (98, 10, 1016, 34), 10, (248, 249, 252, 255), (215, 219, 228, 255), 1)
    bdraw.text((126, 13), state['url'], fill=(109, 117, 133), font=font(13))

    # app canvas inside browser
    app = Image.new('RGBA', (1036, 780), (10, 15, 29, 255))
    adraw = ImageDraw.Draw(app)

    # local app background blobs
    for x, y, r, color in [
        (120, 80, 180, (112, 84, 255, 95)),
        (910, 110, 160, (86, 218, 255, 60)),
        (770, 640, 220, (126, 117, 255, 55)),
    ]:
        blob = Image.new('RGBA', (1036, 780), (0, 0, 0, 0))
        b = ImageDraw.Draw(blob)
        b.ellipse((x-r, y-r, x+r, y+r), fill=color)
        blob = blob.filter(ImageFilter.GaussianBlur(36))
        app = Image.alpha_composite(app, blob)
        adraw = ImageDraw.Draw(app)

    panel = (22, 22, 1014, 250)
    rounded(adraw, panel, 28, (13, 20, 38, 224), (255, 255, 255, 18), 1)
    adraw.ellipse((46, 46, 56, 56), fill=(108, 226, 255))
    adraw.text((68, 43), state['brand'], fill=(151, 167, 203), font=font(12))
    adraw.multiline_text((44, 76), state['headline'], fill='white', font=font(34, bold=True), spacing=4)
    adraw.multiline_text((44, 152), state['body'], fill=(203, 214, 236), font=font(15), spacing=5)
    rounded(adraw, (44, 204, 186, 240), 18, state['cta_primary_fill'])
    adraw.text((69, 214), state['cta_primary'], fill=state['cta_primary_text'], font=font(14, bold=True))
    rounded(adraw, (198, 204, 396, 240), 18, (255, 255, 255, 15), (255, 255, 255, 30), 1)
    adraw.text((224, 214), state['cta_secondary'], fill=(237, 243, 255), font=font(14, bold=True))

    # orb card
    rounded(adraw, (740, 36, 980, 228), 24, (33, 36, 66, 236), (150, 185, 255, 30), 1)
    cx, cy = 860, 110
    for radius, fill in [(68, (255,255,255,24)), (52, (101, 170, 255, 255)), (38, (124, 103, 255, 255)), (18, (13, 20, 38, 255))]:
        adraw.ellipse((cx-radius, cy-radius, cx+radius, cy+radius), fill=fill)
    adraw.text((849, 101), '◎', fill='white', font=font(18, bold=True))
    adraw.text((770, 156), 'Companion state', fill=(151, 167, 203), font=font(12))
    adraw.text((770, 174), state['companion_state'], fill='white', font=font(19, bold=True))
    adraw.multiline_text((770, 198), state['companion_copy'], fill=(213, 222, 242), font=font(13), spacing=4)

    # middle row cards
    rounded(adraw, (22, 270, 506, 532), 24, (13, 20, 38, 224), (255,255,255,18), 1)
    rounded(adraw, (530, 270, 1014, 532), 24, (13, 20, 38, 224), (255,255,255,18), 1)

    adraw.text((42, 292), state['timer_label'], fill=(151, 167, 203), font=font(12))
    adraw.text((42, 314), state['timer_title'], fill='white', font=font(19, bold=True))
    rounded(adraw, (408, 300, 484, 330), 14, state['mode_fill'])
    adraw.text((428, 307), state['mode_text'], fill=(239, 245, 255), font=font(12))
    adraw.text((42, 356), state['timer_value'], fill='white', font=font(56, bold=True))
    rounded(adraw, (42, 430, 486, 444), 8, (255,255,255,20))
    rounded(adraw, (42, 430, 42 + int(444 * state['progress']), 444), 8, state['progress_fill'])

    stats_x = [42, 195, 348]
    for i, (k, v) in enumerate(state['stats']):
        box = (stats_x[i], 462, stats_x[i] + 128, 514)
        rounded(adraw, box, 16, (255,255,255,10), (255,255,255,18), 1)
        adraw.text((box[0] + 12, box[1] + 10), k, fill=(160, 176, 211), font=font(11))
        adraw.text((box[0] + 12, box[1] + 26), v, fill='white', font=font(13))

    adraw.text((550, 292), state['metrics_label'], fill=(151, 167, 203), font=font(12))
    adraw.text((550, 314), state['metrics_title'], fill='white', font=font(19, bold=True))
    y = 356
    for label, val in state['metrics']:
        rounded(adraw, (550, y, 978, y + 40), 14, (255,255,255,10), (255,255,255,18), 1)
        adraw.text((566, y + 12), label, fill=(160, 176, 211), font=font(13))
        adraw.text((850, y + 12), val, fill='white', font=font(13))
        y += 50
    rounded(adraw, (550, 498, 978, 522), 12, (255,255,255,10), (255,255,255,18), 1)
    adraw.text((566, 504), state['risk'], fill=(213, 222, 242), font=font(12))

    # bottom cards
    rounded(adraw, (22, 552, 482, 754), 24, (13, 20, 38, 224), (255,255,255,18), 1)
    rounded(adraw, (506, 552, 1014, 754), 24, (13, 20, 38, 224), (255,255,255,18), 1)
    adraw.text((42, 574), state['setup_label'], fill=(151, 167, 203), font=font(12))
    adraw.text((42, 596), state['setup_title'], fill='white', font=font(19, bold=True))

    pill_positions = [(42, 634), (252, 634), (42, 682), (252, 682)]
    for (text, active), (px, py) in zip(state['pills'], pill_positions):
        width = 190
        draw_chip(adraw, (px, py, px + width, py + 36), text, active)

    rounded(adraw, (42, 726, 458, 742), 8, (255,255,255,10))
    adraw.text((42, 706), state['note'], fill=(213, 222, 242), font=font(12))

    adraw.text((526, 574), state['challenge_label'], fill=(151, 167, 203), font=font(12))
    adraw.text((526, 596), state['challenge_title'], fill='white', font=font(19, bold=True))
    cy = 632
    for title, desc, reward, hi in state['challenges']:
        fill = (28, 57, 86, 255) if hi else (255,255,255,10)
        rounded(adraw, (526, cy, 986, cy + 44), 16, fill, (255,255,255,18), 1)
        adraw.text((542, cy + 8), title, fill='white', font=font(13, bold=True))
        adraw.text((870, cy + 8), reward, fill=(160, 176, 211), font=font(12))
        adraw.text((542, cy + 24), desc, fill=(213, 222, 242), font=font(11))
        cy += 56

    browser.alpha_composite(app, (32, 58))
    img.alpha_composite(browser, (250, 110))

    # subtle floor shadow / composition helpers
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    odraw.ellipse((360, 1005, 1230, 1130), fill=(0, 0, 0, 70))
    overlay = overlay.filter(ImageFilter.GaussianBlur(26))
    img.alpha_composite(overlay)

    # caption card small / natural framing
    cdraw = ImageDraw.Draw(img)
    rounded(cdraw, (250, 1002, 835, 1082), 20, (12, 18, 34, 200), (255,255,255,18), 1)
    cdraw.text((276, 1024), state['caption_title'], fill='white', font=font(18, bold=True))
    cdraw.text((276, 1050), state['caption_sub'], fill=(187, 199, 223), font=font(13))

    return img.convert('RGB')


states = [
    {
        'url': 'deepwork-companion.local / dashboard',
        'brand': 'Deepwork Companion',
        'headline': 'Turn work sessions into calm,\nadaptive AI-powered focus rituals.',
        'body': 'A virtual companion for deep work, lightweight challenges, and smarter recovery windows.\nBuilt with Xiaomi MiMo V2.5 Pro.',
        'cta_primary': 'Start session',
        'cta_secondary': 'Break mode',
        'cta_primary_fill': (124, 205, 255),
        'cta_primary_text': (11, 16, 32),
        'companion_state': 'Stable',
        'companion_copy': 'Momentum looks healthy.\nOne finished task will sharpen\nthe whole session.',
        'timer_label': 'Active timer',
        'timer_title': 'Deep focus block',
        'mode_fill': (35, 66, 88),
        'mode_text': 'focus',
        'timer_value': '45m',
        'progress': 0.86,
        'progress_fill': (108, 226, 255),
        'stats': [('Streak', '6 days'), ('Sessions', '14'), ('Intent', 'Landing')],
        'metrics_label': 'Focus intelligence',
        'metrics_title': 'Session diagnostics',
        'metrics': [('Focus score', '82%'), ('Energy', '64%'), ('Mood', '78% · Locked In')],
        'risk': 'Risk signal · Low drift risk · Keep the current lane.',
        'setup_label': 'Session setup',
        'setup_title': 'Pick today’s work lane',
        'pills': [('Landing page', True), ('Frontend polish', False), ('PR review', False), ('Study mode', False)],
        'note': 'Finalize hero copy and keep the next sprint free from context switching.',
        'challenge_label': 'AI challenge feed',
        'challenge_title': 'Adaptive micro-missions',
        'challenges': [('Single-tab sprint', 'Keep only one work tab open for the next block.', '+8 calm', True), ('Zero-scroll commit', 'Finish one concrete task before checking notifications.', '+1 streak', False)],
        'caption_title': 'Overview dashboard',
        'caption_sub': 'Clean hero shot for README or launch post.',
        'filename': 'deepwork-v2-01-overview.png',
    },
    {
        'url': 'deepwork-companion.local / focus-session',
        'brand': 'Deepwork Companion',
        'headline': 'Protect your best attention\nwith a living focus dashboard.',
        'body': 'The companion tracks momentum, energy, and drift signals while nudging you toward one clean win.\nBuilt with Xiaomi MiMo V2.5 Pro.',
        'cta_primary': 'Pause session',
        'cta_secondary': 'Challenge queue',
        'cta_primary_fill': (114, 244, 214),
        'cta_primary_text': (9, 24, 28),
        'companion_state': 'Locked-in',
        'companion_copy': 'High-quality focus detected.\nKeep scope narrow and finish\nbefore opening anything new.',
        'timer_label': 'Active timer',
        'timer_title': 'Deep focus block',
        'mode_fill': (28, 84, 86),
        'mode_text': 'focus',
        'timer_value': '28m',
        'progress': 0.55,
        'progress_fill': (84, 240, 206),
        'stats': [('Streak', '9 days'), ('Sessions', '23'), ('Intent', 'Onboarding')],
        'metrics_label': 'Focus intelligence',
        'metrics_title': 'Live focus diagnostics',
        'metrics': [('Focus score', '91%'), ('Energy', '79%'), ('Mood', '88% · Creative')],
        'risk': 'Risk signal · Low drift risk · Push one visible milestone before the block ends.',
        'setup_label': 'Current mission lane',
        'setup_title': 'Focus mission controls',
        'pills': [('Onboarding polish', True), ('Interaction audit', False), ('Copy trim', False), ('No distractions', True)],
        'note': 'Keep the polish pass narrow: onboarding hero, tooltip timing, and confirmation states only.',
        'challenge_label': 'AI challenge feed',
        'challenge_title': 'Momentum-preserving missions',
        'challenges': [('No-tab drift', 'Finish the active screen before opening docs or chat.', '+9 momentum', True), ('One clean ship', 'Close one polish task all the way to done.', '+1 boost', False)],
        'caption_title': 'Session in progress',
        'caption_sub': 'Best screenshot for a “working product” feel.',
        'filename': 'deepwork-v2-02-session-running.png',
    },
    {
        'url': 'deepwork-companion.local / break-mode',
        'brand': 'Deepwork Companion',
        'headline': 'Recovery windows that actually\nhelp the next block land better.',
        'body': 'Use short reset rituals to recover energy, reduce noise, and come back with cleaner execution.\nBuilt with Xiaomi MiMo V2.5 Pro.',
        'cta_primary': 'Resume focus',
        'cta_secondary': 'Reset routine',
        'cta_primary_fill': (175, 146, 255),
        'cta_primary_text': (19, 14, 35),
        'companion_state': 'Recovering',
        'companion_copy': 'Break mode is active.\nHydrate, stretch, and stay away\nfrom work chat for ten minutes.',
        'timer_label': 'Recovery timer',
        'timer_title': 'Break mode',
        'mode_fill': (74, 58, 118),
        'mode_text': 'break',
        'timer_value': '10m',
        'progress': 0.72,
        'progress_fill': (159, 132, 252),
        'stats': [('Recovery', '4 resets'), ('Sessions', '12'), ('Intent', 'Reset')],
        'metrics_label': 'Recovery intelligence',
        'metrics_title': 'Recovery diagnostics',
        'metrics': [('Focus score', '68%'), ('Energy', '52%'), ('Mood', '62% · Steady')],
        'risk': 'Risk signal · Moderate drift risk · Recovery should stay offline and short.',
        'setup_label': 'Reset routine',
        'setup_title': 'Short-form recovery cues',
        'pills': [('Hydrate', True), ('No chat', True), ('Avoid scroll', False), ('Walk 5 min', False)],
        'note': 'Keep the break restorative, not stimulating. No inbox, no random tabs, no fake multitasking.',
        'challenge_label': 'Reset prompts',
        'challenge_title': 'Quick recovery guidance',
        'challenges': [('Hydration cue', 'Drink water before touching your keyboard again.', '+6 energy', True), ('Visual reset', 'Look away from the screen for one full minute.', '+4 mood', False)],
        'caption_title': 'Break mode view',
        'caption_sub': 'Natural variation that makes the app feel complete.',
        'filename': 'deepwork-v2-03-break-mode.png',
    },
    {
        'url': 'deepwork-companion.local / challenge-board',
        'brand': 'Deepwork Companion',
        'headline': 'Small AI-generated missions\nthat make deep work feel alive.',
        'body': 'Challenge cards guide attention, reduce tab chaos, and turn vague effort into concrete rituals.\nBuilt with Xiaomi MiMo V2.5 Pro.',
        'cta_primary': 'Accept challenge',
        'cta_secondary': 'Shuffle missions',
        'cta_primary_fill': (124, 205, 255),
        'cta_primary_text': (11, 16, 32),
        'companion_state': 'Stable',
        'companion_copy': 'You do not need more tasks.\nYou need one strong sequence\nof focused execution.',
        'timer_label': 'Challenge timer',
        'timer_title': 'Mission sprint',
        'mode_fill': (35, 66, 88),
        'mode_text': 'focus',
        'timer_value': '18m',
        'progress': 0.38,
        'progress_fill': (108, 226, 255),
        'stats': [('Win rate', '84%'), ('Sessions', '31'), ('Intent', 'Ship')],
        'metrics_label': 'Mission intelligence',
        'metrics_title': 'Mission diagnostics',
        'metrics': [('Focus score', '76%'), ('Energy', '69%'), ('Mood', '74% · Locked In')],
        'risk': 'Risk signal · Low drift risk · Mission-based focus is outperforming passive timers.',
        'setup_label': 'Mission filters',
        'setup_title': 'Challenge focus settings',
        'pills': [('Single-task', True), ('No notifications', True), ('One visible win', False), ('No switching', False)],
        'note': 'Pick one challenge and commit to it for the entire block, even if the temptation to switch shows up.',
        'challenge_label': 'AI challenge feed',
        'challenge_title': 'Curated mission board',
        'challenges': [('Single-task fortress', 'Work on one deliverable with every secondary tool hidden.', '+11 focus', True), ('No-refresh sprint', 'Avoid reloading dashboards or analytics until the block ends.', '+7 calm', False)],
        'caption_title': 'Challenge-centric shot',
        'caption_sub': 'Useful when posting multiple screenshots in a carousel.',
        'filename': 'deepwork-v2-04-challenges.png',
    },
    {
        'url': 'deepwork-companion.local / night-mode',
        'brand': 'Deepwork Companion',
        'headline': 'A late-night focus layer for\nquiet shipping and steady momentum.',
        'body': 'Perfect for solo work sessions when you want soft guidance, less noise, and a calmer way to finish strong.\nBuilt with Xiaomi MiMo V2.5 Pro.',
        'cta_primary': 'Enter night mode',
        'cta_secondary': 'Queue next session',
        'cta_primary_fill': (150, 136, 255),
        'cta_primary_text': (19, 14, 35),
        'companion_state': 'Calm',
        'companion_copy': 'This is a good hour for quiet work.\nKeep the room still, ship one thing,\nand leave a clean next step.',
        'timer_label': 'Night session',
        'timer_title': 'Quiet deep work',
        'mode_fill': (56, 48, 99),
        'mode_text': 'night',
        'timer_value': '52m',
        'progress': 0.9,
        'progress_fill': (133, 119, 255),
        'stats': [('Night streak', '3'), ('Sessions', '19'), ('Intent', 'Final pass')],
        'metrics_label': 'Night intelligence',
        'metrics_title': 'Night focus diagnostics',
        'metrics': [('Focus score', '84%'), ('Energy', '58%'), ('Mood', '72% · Locked In')],
        'risk': 'Risk signal · Moderate fatigue risk · Ship one careful pass, then stop cleanly.',
        'setup_label': 'Night cues',
        'setup_title': 'Quiet-session controls',
        'pills': [('Low-noise', True), ('No social tabs', True), ('Final polish', False), ('Tomorrow note', False)],
        'note': 'Finish the final UI pass, write tomorrow’s first move, and leave before the work gets sloppy.',
        'challenge_label': 'Night guidance',
        'challenge_title': 'Quiet-session prompts',
        'challenges': [('Soft landing', 'Ship one clean improvement, then stop instead of overextending.', '+8 calm', True), ('Tomorrow anchor', 'Leave one precise note for the next session.', '+4 clarity', False)],
        'caption_title': 'Night session variation',
        'caption_sub': 'Good for showing product range without changing the brand feel.',
        'filename': 'deepwork-v2-05-night-mode.png',
    },
]

for state in states:
    img = draw_browser_mockup(state)
    out = OUTDIR / state['filename']
    img.save(out, quality=95)
    print(out)
