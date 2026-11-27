import hashlib,json,subprocess,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np

ROOT=Path.cwd().resolve()
QA=ROOT/'07_QA验收/P4-B'
FOLDERS={'rei-school':'03_校服绫波丽','rei-white':'04_白色战斗服','rei-black':'05_黑色战斗服'}

def read(p):
    return json.loads(p.read_text(encoding='utf-8'))

def write(p,x):
    with p.open('x',encoding='utf-8',newline='\n') as f:
        json.dump(x,f,ensure_ascii=False,indent=2);f.write('\n')

def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def rec(p):
    return {'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size}

def checked(f):
    p=ROOT/f['path']
    assert p.resolve().is_relative_to(ROOT) and sha(p)==f['sha256'],p
    return p

def open_frame(f):
    with Image.open(checked(f)) as im:
        assert im.size==(192,208) and im.mode=='RGBA'
        a=np.asarray(im)
        assert not np.any(a[[0,-1],:,3]) and not np.any(a[:,[0,-1],3])
        assert not np.any(a[a[:,:,3]==0,:3])
        return im.copy()

def png(im,path):
    with path.open('xb') as f:im.save(f,format='PNG')

def flat(im,bg='#f0f3f9'):
    cell=Image.new('RGBA',(192,208),bg)
    cell.alpha_composite(im)
    return cell.convert('RGB')

def gif_validate(path,frames,times,size):
    with Image.open(path) as im:
        assert im.n_frames==frames and im.size==size and im.info['loop']==0
        for i,ms in enumerate(times):
            im.seek(i)
            assert im.info['duration']==ms

def audit_input(row,times):
    checked(row['source'])
    for p in row['previews']:
        path=checked(p)
        if path.suffix=='.gif':gif_validate(path,len(times),times,(192,208))
    imgs=[open_frame(f) for f in row['frames']]
    assert len(imgs)==len(times) and len({x.tobytes() for x in imgs})==len(imgs)
    return imgs

def read_all(p4a,decisions):
    found={}
    for x in p4a['registered_rows']:
        key=(x['id'],x['state'])
        found[key]=x
    for x in decisions:
        if not x['candidate']:continue
        key=(x['id'],x['state'])
        assert key not in found
        p=ROOT/FOLDERS[x['id']]/'P4-B'
        status=read(p/'originals'/x['state']/x['attempt']/'attempt-qa.json')
        assert status['status']=='STRUCTURE_READY_FOR_VISUAL_REVIEW'
        found[key]=read(ROOT/status['row_path'])
    return found

def form_sheet(pid,rows,row_specs,out,imgs,font):
    width=1572
    tile_h=236
    board=Image.new('RGB',(width,tile_h*9+6),'#e5edf9')
    d=ImageDraw.Draw(board)
    for st,ix,count in row_specs:
        y=ix*tile_h+3
        key=pid,st
        state=f'{ix}  {st}  |  {count} frames'
        if key not in rows:
            d.text((9,y),state+'  |  MISSING / rejected',font=font,fill='#922d45')
            continue
        d.text((9,y),state,font=font,fill='#142845')
        for col,im in enumerate(imgs[key]):
            board.paste(flat(im),(6+196*col,y+20))
    png(board,out)
    return rec(out)

def assemble(pid,rows,row_specs,out,imgs,script):
    has_all=all((pid,st) in rows for st,ix,n in row_specs)
    if not has_all:return {'id':pid,'state':'INCOMPLETE','missing_rows':[st for st,i,n in row_specs if (pid,st) not in rows]}
    from compose_atlas import paste_centered,clear_transparent_rgb
    canvas=Image.new('RGBA',(1536,1872))
    for st,ix,n in row_specs:
        for c,im in enumerate(imgs[pid,st]):
            paste_centered(canvas,im,ix,c)
    p=out/'spritesheet-standard.png'
    png(clear_transparent_rgb(canvas),p)
    with Image.open(p) as im:
        assert im.size==(1536,1872) and im.mode=='RGBA'
        for st,ix,n in row_specs:
            for c in range(8):
                cell=im.crop((192*c,208*ix,192*(c+1),208*(ix+1)))
                if c<n:assert cell.tobytes()==imgs[pid,st][c].tobytes(),(pid,st,c)
                else:assert not any(cell.tobytes())
    validation=out/'spritesheet-standard-validation.json'
    assert not validation.exists()
    proc=subprocess.run([sys.executable,'-B',str(script/'validate_atlas.py'),str(p),'--json-out',str(validation)],capture_output=True,text=True,encoding='utf-8')
    result=read(validation)
    state='STRUCTURE_PASS' if proc.returncode==0 and result['ok'] else 'STRUCTURE_FAIL'
    return {'id':pid,'state':state,'atlas':rec(p),'validation':rec(validation),'validator_exit':proc.returncode,'errors':result.get('errors',[]),'warnings':result.get('warnings',[]),'cells':57,'blank_cells':15}

def synchronized(st,times,imgs,out,font):
    w,h=625,262
    frames=[]
    for j,ms in enumerate(times):
        panel=Image.new('RGB',(w,h),'#e5edf9')
        d=ImageDraw.Draw(panel)
        for i,pid in enumerate(FOLDERS):
            key=pid,st
            x=8+i*205
            d.text((x,6),pid,font=font,fill='#142845')
            if key in imgs:panel.paste(flat(imgs[key][j]),(x,26))
            else:d.text((x,103),'MISSING / rejected',font=font,fill='#922d45')
        d.text((8,244),f'{st} | {j+1}/{len(times)} | {ms} ms',font=font,fill='#142845')
        frames.append(panel)
    with out.open('xb') as f:
        frames[0].save(f,format='GIF',save_all=True,append_images=frames[1:],duration=times,loop=0,disposal=2,optimize=False)
    gif_validate(out,len(times),times,(w,h))
    return rec(out)

def main():
    script=Path(sys.argv[1])
    sys.path.insert(0,str(script))
    from compose_atlas import ROW_SPECS
    from render_animation_previews import ROW_DURATIONS
    assert [(s,i,n) for s,i,n in ROW_SPECS]==[(s,i,len(t)) for i,(s,t) in enumerate(ROW_DURATIONS.items())]
    base=ROOT/'07_QA验收/REI_P4A_ASSET_MANIFEST_FIX_BLACK.json'
    p4a=read(base)
    gate=read(QA/'gate.json')
    assert sha(base)==gate['p4a_manifest_sha256']
    decisions=read(QA/'visual-selection.json')
    rows=read_all(p4a,decisions)
    imgs={k:audit_input(x,ROW_DURATIONS[k[1]]) for k,x in rows.items()}
    sheets=[]
    atlases=[]
    font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
    for pid,folder in FOLDERS.items():
        out=ROOT/folder/'P4-B/delivery'
        assert out.resolve()==out
        out.mkdir(parents=True,exist_ok=False)
        sheets.append({'id':pid,**form_sheet(pid,rows,ROW_SPECS,out/'standard-contact-sheet.png',imgs,font)})
        atlases.append(assemble(pid,rows,ROW_SPECS,out,imgs,script))
    compare=QA/'comparison-gifs'
    compare.mkdir(exist_ok=False)
    gifs=[{'state':st,**synchronized(st,t,imgs,compare/f'{st}-three-form-light.gif',font)} for st,t in ROW_DURATIONS.items() if any((pid,st) in imgs for pid in FOLDERS)]
    attempts=[rec(f) for folder in FOLDERS.values() for f in sorted((ROOT/folder/'P4-B/originals').rglob('attempt-qa.json'))]
    sources=[rec(f) for folder in FOLDERS.values() for f in sorted((ROOT/folder/'P4-B/originals').rglob('source.png'))]
    manifest={'stage':'REI-PET-P4-B','status':'PARTIAL_PENDING_ART_REVIEW' if all(x['state']=='STRUCTURE_PASS' for x in atlases) else 'PARTIAL_MISSING_OR_FAILED_ROWS',
              'p4a_manifest':rec(base),'gate':rec(QA/'gate.json'),'visual_selection':rec(QA/'visual-selection.json'),
              'contract_rows':ROW_SPECS,'candidate_frames':sum(len(x) for x in imgs.values()),
              'per_form_frame_totals':{p:sum(len(v) for k,v in imgs.items() if k[0]==p) for p in FOLDERS},
              'locked_old_black_right':p4a['rejected_rows'][0]['source'],'locked_old_black_right_status':'REJECTED; excluded',
              'registered_rows':list(rows.values()),'attempt_records':attempts,'preserved_source_files':sources,'atlases':atlases,
              'contact_sheets':sheets,'comparison_gifs':gifs,
              'hatch_pet_script_sha256':{x:sha(script/x) for x in ['extract_strip_frames.py','inspect_frames.py','compose_atlas.py','validate_atlas.py','render_animation_previews.py']}}
    p=ROOT/'07_QA验收/REI_P4B_ASSET_MANIFEST.json'
    write(p,manifest)
    print(json.dumps({k:manifest[k] for k in ('status','candidate_frames','per_form_frame_totals','atlases','contact_sheets','comparison_gifs')},ensure_ascii=False))

if __name__=='__main__':main()
