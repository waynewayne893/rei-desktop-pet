import argparse
import hashlib
import json
import statistics
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

SIZE = (192, 208)
ANCHOR = (96, 195)
TARGET_HEIGHT = 188
DARK = '#263242'
LIGHT = '#f0f3f9'
PERIODS = {
    'idle': [280, 110, 110, 140, 140, 320],
    'running-right': [120] * 7 + [220],
}
EIGHT_CONNECTED = np.ones((3, 3), dtype=np.uint8)

def write_json(path, payload):
    with path.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write('\n')

def save_png(image, path):
    with path.open('xb') as f:
        image.save(f, format='PNG')

def artifact(path, root):
    with path.open('rb') as f:
        checksum = hashlib.file_digest(f, 'sha256').hexdigest()
    return {'path': path.relative_to(root).as_posix(), 'sha256': checksum,
            'bytes': path.stat().st_size}

def rgb_background(frame, color):
    panel = Image.new('RGBA', SIZE, color)
    panel.alpha_composite(frame)
    return panel.convert('RGB')

def solid_box(alpha):
    return alpha.point(lambda a: 255 if a >= 128 else 0).getbbox()

def source_components(strip, count, matte_floor):
    data = np.asarray(strip)
    alpha = data[:, :, 3]
    bright = alpha >= max(64, matte_floor + 10)
    labels, _ = ndimage.label(bright, structure=EIGHT_CONNECTED)
    sizes = np.bincount(labels.ravel())
    if len(sizes) == 1:
        raise ValueError('no encoded foreground')
    cutoff = max(120, max(sizes[1:]) * 0.20)
    groups = np.flatnonzero(sizes[1:] >= cutoff) + 1
    if len(groups) != count:
        raise ValueError(f'expected {count} comparable disconnected poses, found {len(groups)}')
    objects = ndimage.find_objects(labels)
    groups = sorted(groups, key=lambda v: objects[v - 1][1].start)
    output = []
    for label in groups:
        y, x = objects[label - 1]
        x0, y0 = max(x.start - 4, 0), max(y.start - 4, 0)
        x1, y1 = min(x.stop + 4, strip.width), min(y.stop + 4, strip.height)
        box = (x0, y0, x1, y1)
        if x.start <= 0 or y.start <= 0 or x.stop >= strip.width or y.stop >= strip.height:
            raise ValueError(f'source figure reaches source image edge: {box}')
        region = data[y0:y1, x0:x1].copy()
        keep = ndimage.binary_dilation(labels[y0:y1, x0:x1] == label,
                                       structure=EIGHT_CONNECTED, iterations=2)
        region[~keep] = 0
        if matte_floor:
            a = region[:, :, 3].astype(np.float32)
            a = np.rint(np.clip((a - matte_floor) * 255 / (255 - matte_floor), 0, 255))
            region[:, :, 3] = a.astype(np.uint8)
        region[region[:, :, 3] == 0] = 0
        im = Image.fromarray(region)
        a = im.getchannel('A')
        l, t, r, b = solid_box(a)
        output.append((im, box, (l, t, r, b)))
    return output

def body_anchor(frame, box, state):
    l, t, r, b = box
    rgba = np.asarray(frame)
    if state == 'idle':
        rows = rgba[b - max(8, round((b - t) * 0.025)):b, :, 3]
        _, xs = np.nonzero(rows >= 128)
        return (int(xs.min()) + int(xs.max()) + 1) / 2
    sample = rgba[t + int((b - t) * 0.50):t + int((b - t) * 0.70), :, 3] >= 128
    centers = []
    for row in sample:
        xs = np.flatnonzero(row)
        if xs.size:
            centers.append((int(xs.min()) + int(xs.max()) + 1) / 2)
    return statistics.median(centers)

def register(groups, state):
    baseline = max(origin[1] + box[3] for _, origin, box in groups)
    centers = [body_anchor(frame, box, state) for frame, _, box in groups]
    heights = [box[3] - box[1] for _, _, box in groups]
    tops = [origin[1] + box[1] for _, origin, box in groups]
    widths = [max(center - box[0], box[2] - center) for center, (_, _, box) in zip(centers, groups)]
    scale = min(TARGET_HEIGHT / statistics.median(heights),
                (ANCHOR[1] - 5) / (baseline - min(tops)),
                (ANCHOR[0] - 5) / max(widths))
    outputs = []
    for (img, origin, box), center in zip(groups, centers):
        padded = Image.new('RGBA', (img.width + 1400, img.height + 1200))
        padded.paste(img, (700, 600))
        x0 = 700 + center - ANCHOR[0] / scale
        y0 = 600 + (baseline - origin[1]) - ANCHOR[1] / scale
        viewport = (x0, y0, x0 + SIZE[0] / scale, y0 + SIZE[1] / scale)
        frame = padded.resize(SIZE, Image.Resampling.LANCZOS, box=viewport)
        out = np.array(frame)
        out[out[:, :, 3] < 8] = 0
        frame = Image.fromarray(out)
        alpha = frame.getchannel('A')
        left, top, right, bottom = alpha.getbbox()
        if min(left, top, SIZE[0] - right, SIZE[1] - bottom) <= 0:
            raise ValueError('registered figure reaches cell border')
        n = ndimage.label(np.asarray(alpha) >= 128, structure=EIGHT_CONNECTED)[1]
        if n != 1:
            raise ValueError(f'registered frame contains {n} distinct opaque components')
        outputs.append((frame, {
            'source_origin_box': origin, 'source_local_solid_bbox': box,
            'source_horizontal_anchor': center, 'solid_bbox': solid_box(alpha),
            'nonzero_bbox': alpha.getbbox(), 'transparent_margins_ltrb': [
                left, top, SIZE[0] - right, SIZE[1] - bottom],
        }))
    return outputs, scale, baseline

def draw_sheet(state, frames, destin, label):
    cols = len(frames)
    width = 12 + cols * 196
    sheet = Image.new('RGB', (width, 482), '#e5edf9')
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 15)
    draw.text((8, 5), label, fill='#142745', font=font)
    for k, frame in enumerate(frames):
        x = 6 + k * 196
        for dy, color in ((32, DARK), (248,LIGHT)):
            sheet.paste(rgb_background(frame, color), (x, dy))
        draw.text((x, 461), f'{k+1} | {PERIODS[state][k]} ms', fill='#142745', font=font)
    save_png(sheet, destin)

def make_row(args):
    workspace = Path.cwd().resolve()
    out = Path(args.destination).resolve()
    assert out.is_relative_to(workspace) and out.name == args.state
    source = Path(args.source).resolve()
    from extract_strip_frames import load_native_alpha_image
    with Image.open(source) as raw:
        strip = load_native_alpha_image(raw, source)
        src_alpha = strip.getchannel('A')
        src_metrics = {'size': strip.size, 'mode': strip.mode, 'alpha_range': src_alpha.getextrema(),
                       'fully_transparent_pixels': src_alpha.histogram()[0]}
    periods = PERIODS[args.state]
    groups = source_components(strip, len(periods), args.matte_floor)
    prepared, factor, ground = register(groups, args.state)
    out.mkdir(parents=True, exist_ok=False)
    frames_dir = out / 'frames'
    frames_dir.mkdir()
    files = []
    frame_records = []
    for idx, (frame, measured) in enumerate(prepared):
        path = frames_dir / f'{idx:02}.png'
        save_png(frame, path)
        files.append(path)
        frame_records.append({**artifact(path, workspace), **measured})
    native = out / 'native-first-frame.png'
    save_png(prepared[0][0], native)
    frames = [pair[0] for pair in prepared]
    for name, bg in (('dark', DARK), ('light', LIGHT)):
        composited = [rgb_background(frame, bg) for frame in frames]
        gif = out / f'{args.state}-{name}.gif'
        with gif.open('xb') as stream:
            composited[0].save(stream, format='GIF', save_all=True, append_images=composited[1:],
                               duration=periods, loop=0, disposal=2, optimize=False)
        with Image.open(gif) as check:
            assert check.n_frames == len(periods)
            assert check.size == SIZE
            actual = []
            for index in range(check.n_frames):
                check.seek(index)
                actual.append(check.info.get('duration'))
            assert actual == periods,(gif,actual)
    sheet = out / 'contact-sheet.png'
    draw_sheet(args.state, frames, sheet, f'{args.pet} | {args.state} | native 192 x 208 | candidate for review')
    result = {
        'id': args.pet, 'state': args.state, 'source': {**artifact(source, workspace), **src_metrics},
        'registered_row_scale_xy': [factor, factor], 'source_ground_y': ground,
        'boundary_anchor_xy': ANCHOR, 'matte_alpha_floor': args.matte_floor,
        'method': 'native-alpha major connected poses, shared isotropic row registration',
        'frame_duration_ms': periods, 'frames': frame_records,
        'previews': [artifact(p, workspace) for p in [native, sheet, *sorted(out.glob('*.gif'))]],
    }
    write_json(out / 'row-evidence.json', result)
    print(json.dumps(result, ensure_ascii=False))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--hatch-scripts', required=True)
    parser.add_argument('--source', required=True)
    parser.add_argument('--destination', required=True)
    parser.add_argument('--pet', required=True)
    parser.add_argument('--state', required=True, choices=PERIODS)
    parser.add_argument('--matte-floor', type=int, default=0)
    args = parser.parse_args()
    sys.path.insert(0, args.hatch_scripts)
    make_row(args)

if __name__ == '__main__':
    main()

