"""Общая вёрстка пакетов «Готово к заливу» 30.09 (P60-*) целиком в Pillow (ключ OpenAI истёк 29.09).

Координаты — в единицах 1080×1080, холст рисуется в K раз крупнее и уменьшается при сохранении
(сглаживание фигур). Итог — PNG 1080×1080, ≤ 400 КБ. Основа — psy_lib 30.09 + сжатый шрифт для
«плашек» в стиле рабочих кредитных крео владельца (AT 0819-GE02, LT paskolos).
"""
import math
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = "/home/user/alextest/creatives/ready/2026-09-30_packs"
W = 1080

F = {
    "sb": "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "s": "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "si": "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf",
    "db": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "d": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "serb": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "ser": "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "lserb": "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    "lser": "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    "lseri": "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
}


def rgba(c, a=255):
    return tuple(c[:3]) + ((c[3],) if len(c) == 4 else (a,))


def mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def rotpts(pts, cx, cy, ang):
    """Поворот точек вокруг (cx, cy) на ang градусов (по часовой на экране)."""
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * ca - (y - cy) * sa, cy + (x - cx) * sa + (y - cy) * ca) for x, y in pts]


class C:
    def __init__(self, bg=(255, 255, 255), K=2):
        self.K = K
        self.im = Image.new("RGBA", (W * K, W * K), rgba(bg))
        self._fonts = {}

    # --- базовое
    def s(self, v):
        return int(round(v * self.K))

    def sb(self, box):
        return tuple(self.s(v) for v in box)

    def sp(self, pts):
        return [(self.s(x), self.s(y)) for x, y in pts]

    @property
    def d(self):
        return ImageDraw.Draw(self.im)

    def font(self, name, size):
        key = (name, self.s(size))
        if key not in self._fonts:
            self._fonts[key] = ImageFont.truetype(F[name], self.s(size))
        return self._fonts[key]

    def layer(self):
        return Image.new("RGBA", self.im.size, (0, 0, 0, 0))

    def put(self, lay, blur=0):
        if blur:
            lay = lay.filter(ImageFilter.GaussianBlur(self.s(blur)))
        self.im.alpha_composite(lay)

    def _draw(self, alpha):
        """Непрозрачное — прямо на холст (быстро), полупрозрачное — через слой."""
        if alpha >= 255:
            return self.d, None
        lay = self.layer()
        return ImageDraw.Draw(lay), lay

    # --- фигуры
    def rect(self, box, fill=None, r=0, outline=None, width=0, alpha=255):
        dd, lay = self._draw(alpha)
        f = rgba(fill, alpha) if fill is not None else None
        o = rgba(outline, alpha) if outline is not None else None
        wdt = max(1, self.s(width)) if width else 0
        if r:
            dd.rounded_rectangle(self.sb(box), self.s(r), fill=f, outline=o, width=wdt)
        else:
            dd.rectangle(self.sb(box), fill=f, outline=o, width=wdt)
        if lay:
            self.put(lay)

    def ellipse(self, box, fill=None, outline=None, width=0, alpha=255):
        dd, lay = self._draw(alpha)
        dd.ellipse(self.sb(box), fill=rgba(fill, alpha) if fill else None,
                   outline=rgba(outline, alpha) if outline else None, width=max(1, self.s(width)) if width else 0)
        if lay:
            self.put(lay)

    def circle(self, cx, cy, r, **kw):
        self.ellipse((cx - r, cy - r, cx + r, cy + r), **kw)

    def poly(self, pts, fill, alpha=255, outline=None, width=0):
        dd, lay = self._draw(alpha)
        dd.polygon(self.sp(pts), fill=rgba(fill, alpha) if fill else None)
        if lay:
            self.put(lay)
        if outline:
            self.line(list(pts) + [pts[0]], outline, width, alpha)

    def line(self, pts, fill, width=2, alpha=255, joint="curve"):
        dd, lay = self._draw(alpha)
        dd.line(self.sp(pts), fill=rgba(fill, alpha), width=max(1, self.s(width)), joint=joint)
        if lay:
            self.put(lay)

    def arc(self, box, start, end, fill, width=2, alpha=255):
        dd, lay = self._draw(alpha)
        dd.arc(self.sb(box), start, end, fill=rgba(fill, alpha), width=max(1, self.s(width)))
        if lay:
            self.put(lay)

    def pie(self, box, start, end, fill, alpha=255):
        dd, lay = self._draw(alpha)
        dd.pieslice(self.sb(box), start, end, fill=rgba(fill, alpha))
        if lay:
            self.put(lay)

    def shadow(self, box, r=24, alpha=90, blur=16, off=(0, 8), color=(0, 0, 0)):
        lay = self.layer()
        x0, y0, x1, y1 = box
        ImageDraw.Draw(lay).rounded_rectangle(self.sb((x0 + off[0], y0 + off[1], x1 + off[0], y1 + off[1])), self.s(r), fill=rgba(color, alpha))
        self.put(lay, blur=blur)

    def card(self, box, fill=(255, 255, 255), r=28, sh_alpha=90, blur=18, off=(0, 10), outline=None, width=0):
        self.shadow(box, r=r, alpha=sh_alpha, blur=blur, off=off)
        self.rect(box, fill=fill, r=r, outline=outline, width=width)

    def glow(self, box, color, alpha=200, blur=40, ellipse=True, r=0):
        lay = Image.new("RGBA", self.im.size, tuple(color[:3]) + (0,))
        dd = ImageDraw.Draw(lay)
        if ellipse:
            dd.ellipse(self.sb(box), fill=rgba(color, alpha))
        else:
            dd.rounded_rectangle(self.sb(box), self.s(r), fill=rgba(color, alpha))
        self.put(lay, blur=blur)

    def vgrad(self, box, c0, c1):
        x0, y0, x1, y1 = self.sb(box)
        dd = self.d
        for y in range(y0, y1):
            t = (y - y0) / max(1, y1 - y0 - 1)
            dd.line([(x0, y), (x1 - 1, y)], fill=mix(c0, c1, t) + (255,))

    def hgrad(self, box, c0, c1):
        x0, y0, x1, y1 = self.sb(box)
        dd = self.d
        for x in range(x0, x1):
            t = (x - x0) / max(1, x1 - x0 - 1)
            dd.line([(x, y0), (x, y1 - 1)], fill=mix(c0, c1, t) + (255,))

    def dots(self, box, step, r, col, alpha=40):
        lay = self.layer()
        dd = ImageDraw.Draw(lay)
        x0, y0, x1, y1 = box
        y = y0
        k = 0
        while y < y1:
            x = x0 + (step / 2 if k % 2 else 0)
            while x < x1:
                dd.ellipse(self.sb((x - r, y - r, x + r, y + r)), fill=rgba(col, alpha))
                x += step
            y += step * 0.866
            k += 1
        self.put(lay)

    # --- текст
    def tw(self, text, fnt):
        b = self.d.textbbox((0, 0), text, font=fnt)
        return (b[2] - b[0]) / self.K, (b[3] - b[1]) / self.K

    def lh(self, name, size, gap=1.16):
        asc, desc = self.font(name, size).getmetrics()
        return (asc + desc) / self.K * gap

    def wrap(self, text, fnt, max_w, cond=1.0):
        lines = []
        for para in text.split("\n"):
            cur = ""
            for w_ in para.split(" "):
                t = (cur + " " + w_).strip()
                if self.tw(t, fnt)[0] * cond <= max_w:
                    cur = t
                else:
                    if cur:
                        lines.append(cur)
                    cur = w_
            lines.append(cur)
        return lines

    def fit(self, text, name, max_w, max_lines, start, min_size=16, cond=1.0):
        size = start
        while size > min_size:
            fnt = self.font(name, size)
            ls = self.wrap(text, fnt, max_w, cond)
            if len(ls) <= max_lines and all(self.tw(l, fnt)[0] * cond <= max_w for l in ls):
                return size
            size -= 1
        return min_size

    def text(self, xy, text, name, size, fill, anchor="la", stroke=0, stroke_fill=None, alpha=255):
        dd, lay = self._draw(alpha)
        dd.text(self.sp([xy])[0], text, font=self.font(name, size), fill=rgba(fill, alpha), anchor=anchor,
                stroke_width=self.s(stroke), stroke_fill=rgba(stroke_fill) if stroke_fill else None)
        if lay:
            self.put(lay)

    def ctext(self, xy, text, name, size, fill, cond=0.84, anchor="la"):
        """Сжатый по горизонтали текст (имитация condensed-шрифта с рабочих крео владельца).
        anchor: 'la' / 'ma' / 'ra' (верх строки) или 'lm' / 'mm' / 'rm' (середина)."""
        fnt = self.font(name, size)
        b = fnt.getbbox(text)
        asc, desc = fnt.getmetrics()
        tw_, th_ = b[2], asc + desc
        lay = Image.new("RGBA", (tw_ + 4, th_ + 4), (0, 0, 0, 0))
        ImageDraw.Draw(lay).text((2, 2), text, font=fnt, fill=rgba(fill))
        nw = max(1, int(lay.width * cond))
        lay = lay.resize((nw, lay.height), Image.LANCZOS)
        x, y = self.sp([xy])[0]
        h, v = anchor[0], anchor[1]
        if h == "m":
            x -= nw // 2
        elif h == "r":
            x -= nw
        if v == "m":
            y -= lay.height // 2
        self.im.alpha_composite(lay, (x, y))
        return nw / self.K

    def cwidth(self, text, name, size, cond=0.84):
        return self.tw(text, self.font(name, size))[0] * cond

    def block(self, text, name, size, y, max_w, fill, cx=W / 2, align="center", x=None, gap=1.16, max_lines=None,
              highlight=None, hl_pad=8, min_size=16):
        """Текст с переносом; возвращает нижний y (в единицах 1080)."""
        if max_lines:
            size = self.fit(text, name, max_w, max_lines, size, min_size=min_size)
        fnt = self.font(name, size)
        lines = self.wrap(text, fnt, max_w)
        asc, desc = fnt.getmetrics()
        lh = (asc + desc) / self.K * gap
        for ln in lines:
            w_, _ = self.tw(ln, fnt)
            if align == "center":
                xx = cx - w_ / 2
            elif align == "right":
                xx = x - w_
            else:
                xx = x
            if highlight:
                bb = self.d.textbbox(self.sp([(xx, y)])[0], ln, font=fnt)
                self.rect((bb[0] / self.K - hl_pad, bb[1] / self.K - hl_pad * 0.6, bb[2] / self.K + hl_pad, bb[3] / self.K + hl_pad * 0.8), fill=highlight, r=6)
            self.text((xx, y), ln, name, size, fill)
            y += lh
        return y

    def bars(self, lines, y, name="sb", size=92, cond=0.82, fill=(255, 255, 255), bar=(200, 30, 36), cx=W / 2,
             padx=18, pady=6, gap=10, max_w=980, align="center", x=None, bar_alpha=255, skew=0):
        """Строки-плашки: каждая строка — отдельная цветная плашка, текст сжат по ширине.
        lines — список (text, fill, bar) или str. Возвращает нижний y."""
        for ln in lines:
            if isinstance(ln, str):
                t, fc, bc, sz = ln, fill, bar, size
            else:
                t, fc, bc = ln[0], ln[1], ln[2]
                sz = ln[3] if len(ln) > 3 else size
            k = cond
            while self.cwidth(t, name, sz, k) > max_w - 2 * padx and k > 0.62:
                k -= 0.01
            while self.cwidth(t, name, sz, k) > max_w - 2 * padx:
                sz -= 1
            fnt = self.font(name, sz)
            b = fnt.getbbox(t.upper() if False else t)
            cap_top = b[1] / self.K
            cap_h = (b[3] - b[1]) / self.K
            wdt = self.cwidth(t, name, sz, k)
            if align == "center":
                x0 = cx - wdt / 2
            else:
                x0 = x
            if bc is not None:
                box = (x0 - padx, y, x0 + wdt + padx, y + cap_h + 2 * pady + 12)
                if skew:
                    self.poly([(box[0] + skew, box[1]), (box[2] + skew, box[1]), (box[2] - skew, box[3]), (box[0] - skew, box[3])], bc, alpha=bar_alpha)
                else:
                    self.rect(box, fill=bc, alpha=bar_alpha)
            self.ctext((x0, y + pady + 6 - cap_top), t, name, sz, fc, cond=k)
            y += cap_h + 2 * pady + 12 + gap
        return y

    def button(self, label, cx, cy, name="sb", size=40, fill=(229, 57, 53), color=(255, 255, 255), padx=56, pady=22, r=None,
               arrow=True, shadow=True, outline=None, grad=None, min_w=0):
        t = label + ("  →" if arrow else "")
        fnt = self.font(name, size)
        w_, _ = self.tw(t, fnt)
        asc, desc = fnt.getmetrics()
        h_ = (asc + desc) / self.K
        bw, bh = max(min_w, w_ + 2 * padx), h_ + 2 * pady
        box = (cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2)
        rr = bh / 2 if r is None else r
        if shadow:
            self.shadow(box, r=rr, alpha=110, blur=8, off=(0, 6))
        if grad:
            # глянцевая кнопка: верх светлее
            self.rect(box, fill=grad[1], r=rr, outline=outline, width=4 if outline else 0)
            self.rect((box[0] + 5, box[1] + 5, box[2] - 5, cy), fill=grad[0], r=max(1, rr - 5), alpha=150)
        else:
            self.rect(box, fill=fill, r=rr, outline=outline, width=3 if outline else 0)
        self.text((cx, cy), t, name, size, color, anchor="mm")
        return box

    def pill(self, label, cx, cy, size=22, fill=(229, 57, 53), color=(255, 255, 255), padx=20, pady=10, arrow=True, name="sb", min_w=0):
        return self.button(label, cx, cy, name=name, size=size, fill=fill, color=color, padx=padx, pady=pady, arrow=arrow, shadow=False, min_w=min_w)

    def check(self, x, y, size, color, width=6):
        self.line([(x, y + size * 0.5), (x + size * 0.38, y + size * 0.88), (x + size, y + size * 0.1)], color, width)

    # --- сохранение
    def save(self, rel):
        path = os.path.join(OUT, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        img = self.im.convert("RGB").resize((W, W), Image.LANCZOS)
        img.save(path, optimize=True)
        mode = "truecolor"
        if os.path.getsize(path) > 400 * 1024:
            for colors in (256, 224, 192, 160, 128, 96):
                q = img.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG)
                q.save(path, optimize=True)
                mode = f"{colors} colors"
                if os.path.getsize(path) <= 400 * 1024:
                    break
        print(rel, os.path.getsize(path) // 1024, "KB", mode)
        return path
