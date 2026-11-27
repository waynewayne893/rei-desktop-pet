import json,hashlib
from scipy import ndimage as ndi
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
r=Path.cwd().resolve()
d=r/'02_标准化母版'
out=d/'P3-FIX'
assert d.resolve()==d and not d.is_junction() and not d.is_symlink()
m=json.loads((d/'REI_P3_ASSET_MANIFEST.json').read_text(encoding='utf-8'))
a=next(a for a in m['assets'] if a['id']=='rei-white')
def shi(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
src=Path(a['source']['path'])
base=d/a['outputs']['master-rgba.png']['path']
assert shi(src)==a['source']['sha256'] and shi(base)==a['outputs']['master-rgba.png']['sha256']
with Image.open(src) as im: origin=im.convert('RGB')
with Image.open(base) as im: before=im.copy()
ROI=(528,910,542,970)
TRACK_Y=[910,920,930,945,955,969]
LEFT_RAIL_X=[534,534,533,532,531,530]
RIGHT_RAIL_X=[537,536,536,536,536,536]
DARK_RAIL_CEILING=170
FADE_LOW=211
FADE_HIGH=231

def local_repair(base,source):
    old=np.array(base)
    rgb=np.asarray(source)
    new=old.copy()
    x0,y0,x1,y1=ROI
    stats={'processed_rail_pairs':0,'skipped_rows':[]}
    for y in range(y0,y1):
        blue=rgb[y,:,2].astype(np.int16)
        targets=[int(round(np.interp(y,TRACK_Y,xs))) for xs in (LEFT_RAIL_X,RIGHT_RAIL_X)]
        candidates=[np.arange(max(x0,mid-1),min(x1,mid+2)) for mid in targets]
        left,right=(min(xs,key=lambda x:(blue[x],abs(x-t))) for t,xs in zip(targets,candidates))
        if not (2<=right-left<=8 and blue[left]<=DARK_RAIL_CEILING and blue[right]<=DARK_RAIL_CEILING):
            stats['skipped_rows'].append(y)
            continue
        stats['processed_rail_pairs']+=1
        interior=np.arange(left+1,right)
        confidence=blue[interior]
        # Both ink rails stay intact. Inside the gap, remove strong backdrop
        # samples and feather the lower-confidence, mixed light pixels.
        remaining=np.clip((FADE_HIGH-confidence)/(FADE_HIGH-FADE_LOW),0,1)
        new_alpha=np.rint(old[y,interior,3]*remaining).astype(np.uint8)
        new[y,interior,3]=new_alpha
        clear=interior[(old[y,interior,3]>0)&(new_alpha==0)]
        new[y,clear,:3]=0
    delta=(old!=new).any(axis=2)
    scope=np.zeros(delta.shape,dtype=bool)
    scope[y0:y1,x0:x1]=True
    assert not np.any(delta&~scope)
    assert np.all(new[:,:,3]<=old[:,:,3])
    assert not np.any(delta & (rgb[:,:,2]<=DARK_RAIL_CEILING))
    y,x=np.nonzero(delta)
    assert x.size
    stats.update(changed_pixel_count=int(x.size),observed_changed_bbox=[int(x.min()),int(y.min()),int(x.max())+1,int(y.max())+1],
                 outside_roi_changed_pixels=0,protected_dark_edge_changed_pixels=0,
                 row_changes=[{'y':int(row),'x':list(map(int,np.flatnonzero(delta[row])))} for row in np.flatnonzero(delta.any(axis=1))])
    return Image.fromarray(new),stats

def zoom_comparison(before,after,source):
    dark='#263242'; light='#f0f3f9'; ink='#142343'
    board=Image.new('RGB',(930,560),'#e5eaf5')
    draw=ImageDraw.Draw(board)
    main=ImageFont.truetype('C:/Windows/Fonts/consolab.ttf',22)
    small=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
    draw.text((12,10),'rei-white | Inner-thigh gap, 5x nearest-neighbor',font=main,fill=ink)
    l,t,r,b=(516,897,548,986)
    for i,(label,im,bg) in enumerate([('Frozen RGB',source,light),('Before / dark',before,dark),('After / dark',after,dark),
                                      ('Before / light',before,light),('After / light',after,light)]):
        x=12+i*183
        draw.text((x,43),label,font=small,fill=ink)
        crop=im.crop((l,t,r,b)).resize(((r-l)*5,(b-t)*5),Image.Resampling.NEAREST)
        layer=Image.new('RGBA',crop.size,bg)
        if crop.mode=='RGB': layer.paste(crop)
        else: layer.alpha_composite(crop)
        board.paste(layer.convert('RGB'),(x,68))
    draw.text((12,528),'Area x=516..547, y=897..985 in the 1024 x 1536 source. Treatment restricted to the gap.',font=small,fill=ink)
    return board

FOOT = (96,195)
SIZE = (192,208)
HEIGHTS = (180,188,194)
DARK = '#263242'
LIGHT = '#f0f3f9'
ORDER = ('rei-school','rei-white','rei-black')

def save(im, file):
    assert file.resolve().is_relative_to(out)
    with file.open('xb') as stream:
        im.save(stream,format='PNG')
    return file

def record(p):
    return {'path':p.relative_to(out).as_posix(),'sha256':shi(p),'bytes':p.stat().st_size}

def alpha_data(im):
    alpha=im.getchannel('A')
    box=alpha.getbbox()
    solid=alpha.point(lambda a:255 if a>=128 else 0).getbbox()
    hist=alpha.histogram()
    l,t,r,b=box
    return {
        'dimensions':list(im.size),'mode':im.mode,'nonzero_alpha_bbox':box,
        'alpha128_bbox':solid,'alpha128_height':solid[3]-solid[1],
        'alpha_zero':hist[0],'alpha_partial':sum(hist[1:255]),'alpha_full':hist[255],
        'transparent_margins_LTRB':[l,t,im.width-r,im.height-b],
        'opaque_component_count_alpha128':int(ndi.label(np.asarray(alpha)>=128,structure=np.ones((3,3)))[1]),
        'hidden_nonzero_rgb_pixels':int(np.count_nonzero((np.asarray(alpha)==0)&np.any(np.asarray(im)[:,:,:3]!=0,axis=2))),
    }

def derive(im,height):
    alpha=im.getchannel('A')
    l,t,r,b=alpha_data(im)['alpha128_bbox']
    bottom=np.asarray(alpha)[b-26:b,:]
    _,xs=np.where(bottom>=128)
    axis=(int(xs.min())+int(xs.max())+1)/2
    factor=height/(b-t)
    pad=max(im.size)
    frame=Image.new('RGBA',(im.width+2*pad,im.height+2*pad))
    frame.paste(im,(pad,pad))
    ox=pad+axis-FOOT[0]/factor
    oy=pad+b-FOOT[1]/factor
    box=(ox,oy,ox+SIZE[0]/factor,oy+SIZE[1]/factor)
    native=np.array(frame.resize(SIZE,Image.Resampling.LANCZOS,box=box))
    native[native[:,:,3]<8]=0
    return Image.fromarray(native),{'scale_xy':[factor,factor],'source_foot_x':axis,'source_alpha128_bottom':b,
                                   'source_box_in_padded_input':box}

def alpha_composite(image, bg):
    color=Image.new('RGBA',image.size,bg)
    color.alpha_composite(image)
    return color.convert('RGB')

def make_scale_board(rows, refs, bg):
    panel=Image.new('RGB',(888,833),'#e4ebf7')
    draw=ImageDraw.Draw(panel)
    title=ImageFont.truetype('C:/Windows/Fonts/consolab.ttf',22)
    small=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
    case=ImageFont.truetype('C:/Windows/Fonts/consolab.ttf',17)
    ink='#162743'
    draw.text((13,8),'Rei 180 / 188 / 194 px | native 192 x 208 cells',font=title,fill=ink)
    draw.text((13,36),'Top / bottom transparent rows are measured at A > 0. Asuka frames stay at native size.',font=small,fill=ink)
    for row,(name,variants) in enumerate(rows.items()):
        y=66+245*row
        ref=refs['asuka-school' if name=='rei-school' else 'asuka-work']
        tiles=[(f'{name} {height}',im,info) for height,(im,info) in variants.items()]
        tiles.append((f'{ref[0]} {ref[2]["alpha128_height"]}',ref[1],ref[2]))
        for i,(label,im,info) in enumerate(tiles):
            x=14+i*219
            draw.text((x,y),label,font=case,fill=ink)
            draw.rounded_rectangle((x-1,y+19,x+192,y+228),radius=1,outline='#8392ab')
            panel.paste(alpha_composite(im,bg),(x,y+20))
            top,bottom=[info['transparent_margins_LTRB'][i] for i in (1,3)]
            draw.text((x,y+229),f'Top {top:02} px | Bottom {bottom:02} px',font=small,fill=('#9b2441' if top<=1 else ink))
    return panel

after,repair=local_repair(before,origin)
before_data=alpha_data(before)
after_data=alpha_data(after)
assert before_data['alpha128_bbox']==after_data['alpha128_bbox']
assert before_data['nonzero_alpha_bbox']==after_data['nonzero_alpha_bbox']
assert after_data['opaque_component_count_alpha128']==1 and after_data['hidden_nonzero_rgb_pixels']==0
fixed_path=save(after,out/'rei-white-master-rgba-p3-fix.png')
mask_path=save(after.getchannel('A'),out/'rei-white-alpha-mask-p3-fix.png')
board_path=save(zoom_comparison(before,after,origin),out/'rei-white-edge-before-after.png')

rows={}
scale_info=[]
input_info={}
for name in ORDER:
    asset=next(a for a in m['assets'] if a['id']==name)
    source_file=Path(asset['source']['path'])
    backup=Path(asset['backup']['path'])
    entry=asset['outputs']['master-rgba.png']
    master=d/entry['path']
    a180=asset['outputs']['sample-192x208.png']
    assert shi(source_file)==shi(backup)==asset['source']['sha256']==asset['backup']['sha256']
    assert shi(master)==entry['sha256']
    assert shi(d/a180['path'])==a180['sha256']
    input_info[name]={
        'original_source':asset['source'],'source_backup':asset['backup'],
        'p3_master_before':entry,'p3_sample_180_before':a180,
        'scale_source':record(fixed_path) if name=='rei-white' else entry,
    }
    im=after if name=='rei-white' else Image.open(master)
    rows[name]={}
    sub=out/'scale-candidates'/name
    sub.mkdir(parents=True)
    for h in HEIGHTS:
        native,transform=derive(im,h)
        info=alpha_data(native)
        assert info['alpha128_height']==h and info['alpha128_bbox'][3]==FOOT[1]
        assert info['opaque_component_count_alpha128']==1
        assert info['alpha_zero']>0 and info['hidden_nonzero_rgb_pixels']==0
        p=save(native,sub/f'{name}-{h}px.png')
        orig180=None
        if h==180:
            with Image.open(d/a180['path']) as old:
                orig180=int(np.count_nonzero(np.any(np.asarray(old)!=np.asarray(native),axis=2)))
            assert name=='rei-white' or orig180==0
        margins=info['transparent_margins_LTRB']
        scale_info.append({'id':name,'target_height':h,'file':record(p),'transform':transform,
                           'alpha':info,'same_scale_p3_changed_rgba_pixels':orig180,
                           'frame_edge_nonzero_alpha':any(m==0 for m in margins)})
        rows[name][h]=(native,info)
    if name!='rei-white':
        im.close()
refs={}
refs_info={}
for name,entry in m['comparison_references'].items():
    p=Path(entry['path'])
    assert shi(p)==entry['sha256']
    with Image.open(p) as im:
        tile=im.crop((0,0,192,208))
    info=alpha_data(tile)
    refs[name]=(name,tile,info)
    refs_info[name]={**entry,'observed_native':info}
scale_dark=save(make_scale_board(rows,refs,DARK),out/'scale-comparison-dark.png')
scale_light=save(make_scale_board(rows,refs,LIGHT),out/'scale-comparison-light.png')

result={
    'assets_unchanged_source_and_p3':input_info,
    'white_local_repair':{
        'declared_roi_half_open':ROI,
        'method':'Modify alpha only between paired source ink rails in the specified ROI. Keep RGB except zeroing hidden RGB at newly transparent pixels.',
        'track_y':TRACK_Y,'left_track_x':LEFT_RAIL_X,'right_track_x':RIGHT_RAIL_X,
        'rail_search_radius_px':1,'paired_rail_separation_px_inclusive':[2,8],
        'source_blue_max_for_protected_ink':DARK_RAIL_CEILING,'source_blue_fade_from_to':[FADE_LOW,FADE_HIGH],
        'stats':repair,'before_alpha':before_data,'after_alpha':after_data,'fixed_master':record(fixed_path),'fixed_mask':record(mask_path),
        'comparison':record(board_path)},
    'scale_candidates':scale_info,
    'scale_policy':{'foot_anchor_cell_boundary_xy':FOOT,'frame_size':SIZE,'resampling':'Pillow RGBA Lanczos, same exact x/y scale via floating point source box, α below 8 cleared','heights':HEIGHTS,'selected_height':None,
                    'white_basis':'P3-FIX RGBA', 'school_black_basis':'existing P3 RGBA',
                    'safety_note':'Margins measured in static cells. Any full-frame contact at 194 px is reported. Motion clearance requires future row-level verification.'},
    'installed_asuka_native_comparison':refs_info,
    'new_scale_previews':[record(scale_dark),record(scale_light)],
    'inherited_previews':m['shared_previews'],
}
print(json.dumps(result,ensure_ascii=False))

