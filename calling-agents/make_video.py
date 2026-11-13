#!/usr/bin/env python3
"""Build a LinkedIn demo video (1080x1080, ~28s) for one calling-agent project.
Scenes: title card -> workflow diagram (slow zoom) -> simulated call transcript -> outcomes.
Usage: python3 make_video.py <project-dir-slug>  e.g. 01-banking-calling-agent
Output: <project-dir>/demo-video.mp4
"""
import json, os, subprocess, sys, textwrap
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.expanduser('~/workspace/calling-agents')
W = H = 1080
BG = (26, 26, 34)
CARD = (48, 48, 62)
TEXT = (235, 235, 240)
SUB = (165, 165, 180)
GREEN = (46, 204, 130)

PROJECTS = {
    '01-banking-calling-agent': dict(
        title='Banking Calling Agent', sub='EMI & Payment Reminders',
        agent='Sara  •  Demo Bank', accent=(46, 204, 130),
        lines=[('Agent', 'Assalam-o-Alaikum, main Demo Bank se Sara bol rahi hoon. Aapki EMI Rs 25,000 kal due hai.'),
               ('Customer', 'Ji, main kal subah pay kar dunga.'),
               ('Agent', 'Shukriya! Payment link aapko SMS par bhej diya hai.')],
        outcomes=['Call logged in Google Sheets', 'Payment link sent by email', 'Team notified on Slack']),
    '02-health-calling-agent': dict(
        title='Health Calling Agent', sub='Clinic Appointment Booking',
        agent='Ayesha  •  City Clinic', accent=(0, 200, 180),
        lines=[('Agent', 'Assalam-o-Alaikum, main City Clinic se bol rahi hoon. Aapki appointment kal 11 baje hai — confirm karni thi.'),
               ('Customer', 'Ji confirm hai, main aa jaunga.'),
               ('Agent', 'Shukriya! Reminder SMS bhej diya hai — 15 minute pehle aa jaiye ga.')],
        outcomes=['Appointment confirmed on call', 'Reminder SMS sent', 'Reschedule / cancel handled']),
    '03-ecommerce-calling-agent': dict(
        title='E-commerce Calling Agent', sub='Order Confirmation & COD Check',
        agent='Sara  •  Demo Store', accent=(255, 150, 60),
        lines=[('Agent', 'Aapka order #1234 — 2 items, total Rs 3,500, cash on delivery. Address confirm kar dein?'),
               ('Customer', 'Ji address theek hai, kal deliver kar dein.'),
               ('Agent', 'Shukriya! Aapka order confirm ho gaya hai.')],
        outcomes=['Order confirmed in sheet', 'COD address verified', 'Delivery slot booked']),
    '04-real-estate-calling-agent': dict(
        title='Real Estate Calling Agent', sub='Property Inquiry & Site Visits',
        agent='Ayesha  •  Demo Realty', accent=(90, 170, 255),
        lines=[('Agent', 'Aapne 1 crore budget mein 5 marla ghar ke liye inquiry ki thi — site visit Saturday 11 baje book kar dun?'),
               ('Customer', 'Ji, Saturday theek hai.'),
               ('Agent', 'Shukriya! Visit details WhatsApp par bhej diye hain.')],
        outcomes=['Lead qualified — budget + area', 'Site visit booked', 'Brochure sent to lead']),
    '05-restaurant-calling-agent': dict(
        title='Restaurant Calling Agent', sub='Food Order Confirmation',
        agent='Sara  •  Demo Kitchen', accent=(255, 90, 90),
        lines=[('Agent', 'Aapka order — 2 chicken burgers, total Rs 1,200. Gulberg address confirm hai?'),
               ('Customer', 'Ji, 30 minute mein deliver kar dein.'),
               ('Agent', 'Shukriya! Order kitchen ko bhej diya hai.')],
        outcomes=['Order confirmed in 30 seconds', 'Address verified', 'Kitchen notified instantly']),
    '06-education-calling-agent': dict(
        title='Education Calling Agent', sub='Admission Inquiry & Campus Visits',
        agent='Ayesha  •  Demo University', accent=(155, 120, 255),
        lines=[('Agent', 'Aapne BS Computer Science mein admission ke liye inquiry ki thi. Aap eligible hain — campus visit book kar dun?'),
               ('Customer', 'Ji, next week visit karna chahta hoon.'),
               ('Agent', 'Shukriya! Visit details email par bhej diye hain.')],
        outcomes=['Eligibility checked on call', 'Campus visit booked', 'Counsellor transfer ready']),
    '07-travel-calling-agent': dict(
        title='Travel Calling Agent', sub='Hotel & Flight Confirmations',
        agent='Sara  •  Demo Travels', accent=(120, 220, 255),
        lines=[('Agent', 'Aapki Lahore hotel booking 20 November se confirm hai — 2 nights, 2 guests.'),
               ('Customer', 'Ji confirm hai, shukriya.'),
               ('Agent', 'Shukriya! Itinerary email par bhej diya hai.')],
        outcomes=['Booking confirmed', 'Itinerary emailed', 'Date change / cancel handled']),
    '08-insurance-calling-agent': dict(
        title='Insurance Calling Agent', sub='Policy Renewal Reminders',
        agent='Ayesha  •  Demo Insurance', accent=(255, 200, 90),
        lines=[('Agent', 'Aapki car insurance policy 25 November ko renew ho rahi hai — premium Rs 18,000 due hai.'),
               ('Customer', 'Main is hafte pay kar dunga.'),
               ('Agent', 'Shukriya! Payment link email par bhej diya hai.')],
        outcomes=['Renewal intent recorded', 'Payment link sent', 'Claim questions routed to agent']),
}


def font(size, bold=False):
    p = f'/usr/share/fonts/truetype/dejavu/DejaVuSans{"-Bold" if bold else ""}.ttf'
    return ImageFont.truetype(p, size) if os.path.exists(p) else ImageFont.load_default()


def wrap(d, text, f, max_w):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def scene_title(p):
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    for gx in range(0, W, 36):
        for gy in range(0, H, 36):
            d.ellipse([gx - 1.5, gy - 1.5, gx + 1.5, gy + 1.5], fill=(58, 58, 70))
    d.rectangle([0, 500, 14, 620], fill=p['accent'])
    f_t, f_s = font(72, True), font(36)
    y = 470
    for ln in wrap(d, p['title'], f_t, 900):
        d.text((60, y), ln, font=f_t, fill=TEXT)
        y += 86
    d.text((60, y + 16), p['sub'], font=f_s, fill=SUB)
    f_chip = font(30, True)
    cx = 60
    for chip in ['AI Calling Agent', 'Vapi  +  n8n']:
        tw = d.textlength(chip, font=f_chip)
        d.rounded_rectangle([cx, y + 110, cx + tw + 44, y + 166], radius=28,
                            fill=CARD, outline=p['accent'], width=3)
        d.text((cx + 22, y + 122), chip, font=f_chip, fill=TEXT)
        cx += tw + 44 + 24
    return img


def scene_flow(proj_dir, p):
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    wf_png = os.path.join(proj_dir, 'workflow.png')
    wf = Image.open(wf_png).convert('RGB')
    wf.thumbnail((1020, 800))
    img.paste(wf, ((W - wf.width) // 2, 90))
    d.rounded_rectangle([40, 880, 1040, 990], radius=18, fill=CARD)
    f_c = font(28, True)
    txt = 'Schedule  →  Sheet  →  Filter  →  Vapi Call  →  Log'
    tw = d.textlength(txt, font=f_c)
    d.text(((W - tw) / 2, 914), txt, font=f_c, fill=TEXT)
    return img


def scene_call(p):
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    f_lab, f_b = font(28, True), font(32)
    d.text((60, 60), 'SIMULATED CALL  •  ' + p['agent'], font=f_lab, fill=p['accent'])
    y = 140
    for who, text in p['lines']:
        is_agent = who == 'Agent'
        lines = wrap(d, text, f_b, 800)
        bh = len(lines) * 44 + 36
        if is_agent:
            x0, col = 60, (30, 80, 55)
        else:
            x0, col = 220, (58, 58, 72)
        d.rounded_rectangle([x0, y, x0 + 860 if is_agent else 1020, y + bh],
                            radius=22, fill=col)
        d.text((x0 + 24, y + 6), who.upper(), font=font(22, True),
               fill=p['accent'] if is_agent else SUB)
        ty = y + 34
        for ln in lines:
            d.text((x0 + 24, ty), ln, font=f_b, fill=TEXT)
            ty += 44
        y += bh + 36
    return img


def scene_outcome(p):
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    for gx in range(0, W, 36):
        for gy in range(0, H, 36):
            d.ellipse([gx - 1.5, gy - 1.5, gx + 1.5, gy + 1.5], fill=(58, 58, 70))
    f_h, f_o = font(56, True), font(36)
    d.text((60, 300), 'What happens after the call', font=f_h, fill=TEXT)
    y = 430
    for o in p['outcomes']:
        d.ellipse([60, y + 8, 96, y + 44], fill=p['accent'])
        d.text((72, y + 8), '✓', font=font(28, True), fill=BG)
        d.text((120, y), o, font=f_o, fill=TEXT)
        y += 84
    d.text((60, 780), 'Full workflow on GitHub  •  Vapi + n8n', font=font(32), fill=SUB)
    return img


def main():
    slug = sys.argv[1]
    proj_dir = os.path.join(BASE, slug)
    p = PROJECTS[slug]
    tmp = os.path.join(proj_dir, '_video_frames')
    os.makedirs(tmp, exist_ok=True)
    scenes = [
        (scene_title(p), 5),
        (scene_flow(proj_dir, p), 10),
        (scene_call(p), 10),
        (scene_outcome(p), 5),
    ]
    paths = []
    for i, (im, dur) in enumerate(scenes):
        fp = os.path.join(tmp, f'scene{i}.png')
        im.save(fp)
        paths.append((fp, dur))
    out = os.path.join(proj_dir, 'demo-video.mp4')
    # xfade chain: A(5) B(10) C(10) D(5), fade 0.6s; B gets slow zoom
    fc = (
        "[0]fps=24,format=yuv420p[a];"
        "[1]zoompan=z='min(zoom+0.0009,1.09)':d=240:s=1080x1080:fps=24,format=yuv420p[bz];"
        "[2]fps=24,format=yuv420p[c];[3]fps=24,format=yuv420p[dd];"
        "[a][bz]xfade=transition=fade:duration=0.6:offset=4.4[x1];"
        "[x1][c]xfade=transition=fade:duration=0.6:offset=13.8[x2];"
        "[x2][dd]xfade=transition=fade:duration=0.6:offset=23.2[v]"
    )
    cmd = ['ffmpeg', '-y', '-loop', '1', '-t', '5', '-i', paths[0][0],
           '-loop', '1', '-t', '10', '-i', paths[1][0],
           '-loop', '1', '-t', '10', '-i', paths[2][0],
           '-loop', '1', '-t', '5', '-i', paths[3][0],
           '-filter_complex', fc, '-map', '[v]', '-c:v', 'libx264',
           '-pix_fmt', 'yuv420p', '-r', '24', '-crf', '26', '-movflags', '+faststart', out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print('FFMPEG FAILED'); print(r.stderr[-2000:]); sys.exit(1)
    print('OK', out, os.path.getsize(out), 'bytes')


if __name__ == '__main__':
    main()
