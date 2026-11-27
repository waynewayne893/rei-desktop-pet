import hashlib
import json
from io import BytesIO
import platform
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from scipy import ndimage as ndi
root=Path.cwd().resolve()
out=Path(__file__).resolve().parent
assert out.resolve()==out and not out.is_junction() and not out.is_symlink()
source=root/'00_原始美术母版'
manifest=json.loads((source/'REI_ART_FREEZE_MANIFEST.json').read_text(encoding='utf-8'))
items=sorted(manifest['assets'],key=lambda a: ('rei-school','rei-white','rei-black').index(a['id']))
def sha(f):
    with f.open('rb') as src: return hashlib.file_digest(src,'sha256').hexdigest()
def write_img(im,p):
    with p.open('xb') as f: im.save(f,format='PNG')
def approximate_bg(rgb):
    sides=rgb[:,np.r_[16:180,844:1008],:]
    left=ndi.median_filter(np.median(sides[:,:164],axis=1),size=(31,1))
    right=ndi.median_filter(np.median(sides[:,164:],axis=1),size=(31,1))
    x=np.clip((np.arange(1024)-97.5)/828,0,1)[None,:,None]
    return (1-x)*left[:,None,:]+x*right[:,None,:]
EDGE_MIN=6.0
COLOR_MIN=10.0
SOLE_EDGE_START=1400
CONTOUR_INSET=1.5
FEATHER_WIDTH=2.8
NEGATIVE_SPACE_SEEDS={
    'rei-school':[(496,1280)],
    'rei-white':[(537,853),(530,1044),(518,1260),(471,691)],
    'rei-black':[(535,1033),(522,1280)],
}
def largest(binary):
    labels,n=ndi.label(binary,structure=np.ones((3,3)))
    if not n: raise ValueError('no foreground')
    sizes=np.bincount(labels.ravel());sizes[0]=0
    return labels==sizes.argmax()
def make_mask(rgb,pet_id):
    bg=approximate_bg(rgb)
    diff=np.abs(rgb-bg).max(axis=-1)
    softened=ndi.gaussian_filter(rgb,sigma=(1.1,1.1,0))
    dx=np.gradient(softened,axis=1)
    dy=np.gradient(softened,axis=0)
    grad=np.sqrt(dx*dx+dy*dy).max(axis=-1)
    gradient_seed=grad>=EDGE_MIN
    candidate=(diff>=COLOR_MIN)|gradient_seed
    candidate[SOLE_EDGE_START:]=gradient_seed[SOLE_EDGE_START:]
    candidate=largest(ndi.binary_closing(candidate,iterations=2))
    full=ndi.binary_fill_holes(candidate)
    holes,_=ndi.label(full&~candidate)
    used=[]
    for x,y in NEGATIVE_SPACE_SEEDS[pet_id]:
        tag=holes[y,x]
        if tag:
            gap=holes==tag
            full[gap]=False
            used.append([x,y,int(gap.sum())])
        else:
            raise ValueError(f'{pet_id}: negative-space seed {(x,y)} did not match template')
    # Two previously enclosed leg openings contain thin sections where edge
    # seeds meet. Clear background-colored pixels only in their local corridors.
    yy,xx=np.ogrid[:rgb.shape[0],:rgb.shape[1]]
    if pet_id=='rei-black':
        leg_corridor=(yy>=866)&(yy<1444)&(xx>=499)&(xx<=551)
        full[leg_corridor&(diff<51)]=False
        between_boots=(yy>=1430)&(yy<=1500)&(xx>=509)&(xx<=540)
        shadow=(rgb[:,:,2]>148)&((rgb[:,:,0]-rgb[:,:,2])<=25)
        full[between_boots&shadow]=False
    if pet_id=='rei-white':
        center=np.interp(np.arange(rgb.shape[0]),[845,879,954,1000,1040,1085,1125],[535,536,536,533,530,530,525])
        leg_corridor=(yy>=845)&(yy<1135)&(np.abs(xx-center[:,None])<=5)
        full[leg_corridor&(diff<5.5)]=False
        for y in range(845,1135):
            mid=int(round(center[y]))
            blue=rgb[y,:,2]
            left=mid-8+int(np.argmin(blue[mid-8:mid]))
            right=mid+1+int(np.argmin(blue[mid+1:mid+9]))
            start,stop=left+1,right
            segment=blue[start:stop]
            if blue[left]<170 and blue[right]<170 and segment.size and segment.max()>226:
                # The two dark ink rails bound a real narrow negative space.
                full[y,start:stop] &= segment<214
    # Where the original floor shadow meets the edge, use the pigment of the
    # outsole as a per-column lower bound. Bright toe interiors stay intact.
    shoe_start={'rei-school':1445,'rei-white':1450,'rei-black':1443}[pet_id]
    sole_pigment=(rgb[:,:,2]<150)|((rgb[:,:,0]-rgb[:,:,2])>25)
    below=np.where(sole_pigment & (yy>=1425),yy,0).max(axis=0)
    limit=np.maximum(shoe_start-1,ndi.maximum_filter1d(below,size=3)+2)
    full[yy>limit[None,:]]=False
    inside=ndi.distance_transform_edt(full)
    outside=ndi.distance_transform_edt(~full)
    sdf=inside-outside
    coverage=np.clip((sdf-CONTOUR_INSET+FEATHER_WIDTH/2)/FEATHER_WIDTH,0,1)
    rgba=np.dstack([rgb,np.rint(coverage*255)])
    # Keep RGB inside the final binary core. On the transition, use local
    # nearest-foreground color to avoid baking the light matte into the edge.
    opaque=(sdf>=CONTOUR_INSET+FEATHER_WIDTH/2+0.5)
    iy,ix=ndi.distance_transform_edt(~opaque,return_distances=False,return_indices=True)
    transition=(rgba[:,:,3]>0)&(rgba[:,:,3]<255)
    foreground=rgb[iy[transition],ix[transition],:]
    # Local palette is authoritative only at the faint side of the feather.
    weights=coverage[transition,None]
    rgba[transition,:3]=foreground*(1-weights)+rgb[transition]*weights
    output=np.uint8(np.rint(rgba))
    keep=largest(output[:,:,3]>0)
    removed=int(np.count_nonzero((output[:,:,3]>0)&~keep))
    output[~keep]=0
    return Image.fromarray(output),used,removed

SIZE=(192,208)
HEIGHT=180
ANCHOR=(96,195)
DARK='#263242'
LIGHT='#f0f3f9'
FONT=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16)
HEAD=ImageFont.truetype('C:/Windows/Fonts/consolab.ttf',21)

def bbox(im,threshold=128):
    alpha=im.getchannel('A')
    return alpha.point(lambda a:255 if a>=threshold else 0).getbbox()

def sample(im):
    l,t,r,b=bbox(im)
    values=np.asarray(im.getchannel('A'))[b-min(26,b-t):b,:]
    _,cols=np.nonzero(values>=128)
    foot=(int(cols.min())+int(cols.max())+1)/2
    scale=HEIGHT/(b-t)
    pad=max(im.size)
    padded=Image.new('RGBA',(im.width+2*pad,im.height+2*pad))
    padded.paste(im,(pad,pad))
    x0=pad+foot-ANCHOR[0]/scale
    y0=pad+b-ANCHOR[1]/scale
    bounds=(x0,y0,x0+SIZE[0]/scale,y0+SIZE[1]/scale)
    native=padded.resize(SIZE,Image.Resampling.LANCZOS,box=bounds)
    raw=np.array(native)
    raw[raw[:,:,3]<8]=0
    native=Image.fromarray(raw)
    return native,{
        'source_alpha128_bbox':[l,t,r,b],'source_foot_axis_x':foot,
        'scale_xy':[scale,scale],'foot_anchor_cell_boundary_xy':list(ANCHOR),
        'nominal_visible_height_px':HEIGHT,'cell_size_px':list(SIZE),
        'filter':'Pillow RGBA Lanczos with uniform floating-point source box, alpha below 8 cleared',
        'output_alpha128_bbox':bbox(native),'output_nonzero_alpha_bbox':native.getbbox(),
    }

def composite(im,color):
    bg=Image.new('RGBA',im.size,color)
    bg.alpha_composite(im)
    return bg.convert('RGB')

def record(p):
    return {'path':p.relative_to(out).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size}

def pixel_qa(im):
    arr=np.asarray(im)
    alpha=arr[:,:,3]
    values=np.bincount(alpha.ravel(),minlength=256)
    return {'size_px':list(im.size),'mode':im.mode,'alpha_zero':int(values[0]),
            'alpha_partial':int(values[1:255].sum()),'alpha_full':int(values[255]),
            'alpha_nonzero_bbox':im.getbbox(),'alpha128_bbox':bbox(im),
            'detached_visible_components_8connected':int(ndi.label(alpha>=128,structure=np.ones((3,3)))[1])-1,
            'nonzero_rgb_at_alpha_zero':int(np.count_nonzero(np.any(arr[:,:,:3]!=0,axis=2)&(alpha==0)))}

AREAS={
    'rei-school': [('Hair and clips',(280,18,752,465)),('Hands and skirt',(380,595,659,947)),('Leg gap and soles',(405,1108,575,1521))],
    'rei-white': [('Hair and clips',(280,18,752,465)),('00, arms and gloves',(345,466,712,991)),('Leg gap and soles',(424,1055,611,1520))],
    'rei-black': [('Hair and clips',(280,18,752,465)),('09 and right hand on left arm',(406,452,686,1000)),('Leg gap and soles',(421,1030,634,1520))],
}

def edge_sheet(pet_id,rgba):
    board=Image.new('RGB',(1050,1044),LIGHT)
    d=ImageDraw.Draw(board)
    d.text((14,11),f'{pet_id} | Original-resolution edge crops',fill='#222940',font=HEAD)
    d.text((14,44),'Dark composite',fill='#222940',font=FONT)
    d.text((539,44),'Light composite',fill='#222940',font=FONT)
    for i,(label,region) in enumerate(AREAS[pet_id]):
        top=65+322*i
        d.text((14,top),label,fill='#222940',font=FONT)
        crop=rgba.crop(region)
        crop.thumbnail((514,296),Image.Resampling.LANCZOS)
        for col,bg in enumerate((DARK,LIGHT)):
            tile=Image.new('RGB',(519,296),bg)
            view=composite(crop,bg)
            tile.paste(view,((519-view.width)//2,(296-view.height)//2))
            board.paste(tile,(3+525*col,top+21))
    return board

def reference():
    evidence=json.loads((root/'07_QA验收/ASUKA_P2_READONLY_EVIDENCE.json').read_text(encoding='utf-8'))
    folder=Path(evidence['installed_root'])
    refs={}
    for key in ('asuka-school','asuka-work'):
        p=folder/key/'spritesheet.webp'
        digest=sha(p)
        assert digest==evidence['artifacts'][f'installed/{key}/spritesheet.webp']['sha256']
        with Image.open(p) as im:
            assert im.size==(1536,2288) and im.mode=='RGBA'
            native=im.crop((0,0,192,208))
        refs[key]=(native,{'path':str(p),'sha256':digest,'source_cell_row_col':[0,0],
                           'native_image_bbox_alpha128':bbox(native)})
    return refs

def comparison(tiles):
    board=Image.new('RGB',(1090,536),'#e2e8f2')
    d=ImageDraw.Draw(board)
    d.text((16,12),'Native 192 x 208 | 1 image pixel = 1 board pixel',fill='#172039',font=HEAD)
    for i,(name,native) in enumerate(tiles):
        x=16+i*214
        d.text((x,42),name,fill='#172039',font=FONT)
        for y,color in ((65,DARK),(285,LIGHT)):
            board.paste(composite(native,color),(x,y))
    d.text((16,503),'Asuka: installed V2, idle (0,0), unchanged. Rei: shared foot anchor, 180 px target height.',fill='#172039',font=FONT)
    return board

def equal_height_comparison(tiles):
    board=Image.new('RGB',(1090,318),'#e2e8f2')
    d=ImageDraw.Draw(board)
    d.text((16,12),'Silhouette comparison | shared 180 px height / same foot anchor',fill='#172039',font=HEAD)
    for i,(name,image) in enumerate(tiles):
        x=16+i*214
        d.text((x,42),name,fill='#172039',font=FONT)
        board.paste(composite(image,LIGHT),(x,65))
    d.text((16,282),'Comparison only. Asuka references rescaled proportionally; native comparison is separate.',fill='#172039',font=FONT)
    return board

def main():
    refs=reference()
    results=[]
    natives=[]
    for it in items:
        pet_id=it['id']
        f=source/it['filename']
        b=root/it['backup_path']
        input_sha=sha(f)
        backup_sha=sha(b)
        if input_sha!=it['sha256'] or backup_sha!=it['backup_sha256'] or input_sha!=backup_sha:
            print(f'{pet_id}: STOP — source or backup SHA-256 differs from the freeze manifest.')
            continue
        with Image.open(f) as im:
            assert im.mode=='RGB' and im.size==(1024,1536)
            rgb=np.asarray(im).astype('float32')
        rgba,used,removed=make_mask(rgb,pet_id)
        native,geometry=sample(rgba)
        final=out/pet_id
        final.mkdir()
        output_images={
            'alpha-mask.png':rgba.getchannel('A'),
            'master-rgba.png':rgba,
            'sample-192x208.png':native,
            'preview-dark.png':composite(rgba,DARK),
            'preview-light.png':composite(rgba,LIGHT),
            'edge-details.png':edge_sheet(pet_id,rgba),
        }
        outputs={}
        for name,img in output_images.items():
            p=final/name
            write_img(img,p)
            outputs[name]=record(p)
        raw=np.asarray(rgba)
        opaque=raw[:,:,3]==255
        arrays_equal=np.array_equal(raw[opaque,:3],rgb[opaque])
        results.append({'id':pet_id,'name':it['label'],'frozen_pose':it['pose'],
                        'source':{'path':str(f),'sha256':input_sha,'bytes':f.stat().st_size,
                                  'size_px':[1024,1536],'mode':'RGB'},
                        'backup':{'path':str(b),'sha256':backup_sha},
                        'workspace_baseline_status':'hash-verified P2 frozen candidate, pending user final visual identity confirmation',
                        'prior_download_source':None,
                        'confirmed_negative_space_seeds_x_y_with_area':used,
                        'tiny_detached_mask_pixels_removed':removed,
                        'master_opaque_rgb_pixel_identical_to_input':bool(arrays_equal),
                        'master_pixel_qa':pixel_qa(rgba),'sample_geometry':geometry,'sample_pixel_qa':pixel_qa(native),
                        'outputs':outputs})
        assert arrays_equal
        natives.append((pet_id,native))
    if len(natives)!=3:
        raise SystemExit('At least one freeze digest did not match. Full comparison not emitted.')
    native_path=out/'native-size-comparison.png'
    equal_path=out/'equal-height-comparison.png'
    comparison_tiles=[*natives,*[(name,entry[0]) for name,entry in refs.items()]]
    write_img(comparison(comparison_tiles),native_path)
    write_img(equal_height_comparison([*natives,*[(name,sample(entry[0])[0]) for name,entry in refs.items()]]),equal_path)
    params={
        'background_estimation':'Pixelwise linear interpolation across side strip medians x=16:180 and 844:1008, 31-row median filter',
        'candidate_color_max_channel_residual':COLOR_MIN,'candidate_max_channel_gradient':EDGE_MIN,
        'gradient_gaussian_sigma_px':1.1,'sole_gradient_only_from_row':SOLE_EDGE_START,
        'candidate_binary_closing_iterations':2,'candidate_hole_policy':'fill, then restore per-character visually identified negative spaces and local leg corridors',
        'contour_inset_px':CONTOUR_INSET,'alpha_feather_transition_px':FEATHER_WIDTH,
        'sole_start_y':{'rei-school':1445,'rei-white':1450,'rei-black':1443},
        'sole_cap':'bottom blue < 150 or red minus blue > 25 from y=1425, max-filtered by 3 columns, plus 2 px',
        'edge_rgb':'Inside alpha=255 keep source pixels; transition blends toward nearest opaque interior in proportion to 1-alpha; zero RGB at alpha=0',
        'no_person_redraw':True,'no_nonuniform_scaling':True,
        'preview_backgrounds':[DARK,LIGHT],
        'python':platform.python_version(),
    }
    result={'assets':results,'processing_parameters':params,
            'comparison_references':{name:entry[1] for name,entry in refs.items()},
            'shared_previews':[record(out/'frozen-masters-preview.png'),record(native_path),record(equal_path)],
            'recipe':record(Path(__file__))}
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':
    main()

