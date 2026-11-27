import argparse,contextlib,hashlib,io,json,runpy,shutil,sys
from pathlib import Path
from types import SimpleNamespace
from PIL import Image

ROOT=Path.cwd().resolve()
QA=ROOT/'07_QA验收/P4-B'
FOLDERS={'rei-school':'03_校服绫波丽','rei-white':'04_白色战斗服','rei-black':'05_黑色战斗服'}

def write(path,obj):
    with path.open('x',encoding='utf-8',newline='\n') as f:json.dump(obj,f,ensure_ascii=False,indent=2);f.write('\n')

def sha(p):
    with p.open('rb') as a:return hashlib.file_digest(a,'sha256').hexdigest()

def copy_native(j,scripts):
    from extract_strip_frames import load_native_alpha_image
    pid,st,attempt=j['id'],j['state'],j.get('attempt','attempt-01')
    work=ROOT/FOLDERS[pid]/'P4-B'
    assert work.resolve()==work
    dest=work/'originals'/st/attempt
    dest.mkdir(parents=True,exist_ok=False)
    original=dest/'source.png'
    with Path(j['path']).open('rb') as a,original.open('xb') as b:shutil.copyfileobj(a,b)
    assert sha(Path(j['path']))==sha(original)
    status={'id':pid,'state':st,'attempt':attempt,'source_path':original.relative_to(ROOT).as_posix(),'sha256':sha(original),
            'native_alpha_pass':False,'status':'ORIGINAL_SAVED'}
    if j.get('prompt'):status['prompt']=j['prompt']
    try:
        with Image.open(original) as raw:
            status.update(size=raw.size,mode=raw.mode)
            if 'A' in raw.getbands():
                a=raw.getchannel('A')
                status.update(alpha_zero=a.histogram()[0],alpha_range=a.getextrema(),corners=[a.getpixel(p) for p in [(0,0),(raw.width-1,0),(0,raw.height-1),(raw.width-1,raw.height-1)]])
            load_native_alpha_image(raw, original)
        status['native_alpha_pass']=True
        origin=work/'candidates'/attempt/st
        args=SimpleNamespace(source=str(original),destination=str(origin),state=st,pet=pid,matte_floor=0)
        with contextlib.redirect_stdout(io.StringIO()):make_row(args)
        row=json.loads((origin/'row-evidence.json').read_text(encoding='utf-8'))
        times=ROW_DURATIONS[st]
        assert len(row['frames'])==len(times)
        assert len({f['sha256'] for f in row['frames']})==len(times)
        for fr in row['frames']:
            with Image.open(ROOT/fr['path']) as im:
                assert im.size==(192,208) and im.mode=='RGBA'
                alpha=im.getchannel('A')
                l,t,r,b=alpha.getbbox()
                assert min(l,t,192-r,208-b)>0
        status.update(row_path=(origin/'row-evidence.json').relative_to(ROOT).as_posix(),contact_path=(origin/'contact-sheet.png').relative_to(ROOT).as_posix(),
                      min_top_margin=min(x['transparent_margins_ltrb'][1] for x in row['frames']),
                      solid_heights=[x['solid_bbox'][3]-x['solid_bbox'][1] for x in row['frames']],
                      solid_bottoms=[x['solid_bbox'][3] for x in row['frames']])
        status['status']='STRUCTURE_READY_FOR_VISUAL_REVIEW'
        if st=='jumping':
            bottoms=status['solid_bottoms']
            if min(bottoms[1:4])>max(bottoms[0],bottoms[4])-2 or bottoms[2]>min(bottoms[1],bottoms[3])+1 or status['solid_heights'][-1]<182:
                status['status']='REJECTED_JUMP_GEOMETRY'
                status['reason']='Airborne peak is missing/misordered or the recovery scale is too short at the locked ground anchor.'
    except (Exception,SystemExit) as e:
        status['status']='REJECTED_NATIVE_ALPHA' if not status['native_alpha_pass'] else 'REJECTED_STRUCTURE'
        status['reason']=str(e)
    write(dest/'attempt-qa.json',status)
    return status

if __name__=='__main__':
    sys.path.insert(0,sys.argv[1])
    from render_animation_previews import ROW_DURATIONS
    make_row=runpy.run_path(str(ROOT/'07_QA验收/P4-A/build_preview_row.py'))['make_row']
    g=make_row.__globals__
    g['PERIODS'].update(ROW_DURATIONS)
    anchor=g['body_anchor']
    def state_anchor(im,box,state):
        return anchor(im,box,state if state.startswith('running-') or state=='jumping' else 'idle')
    g['body_anchor']=state_anchor
    jobs=json.loads(sys.stdin.read())
    print(json.dumps([copy_native(j,sys.argv[1]) for j in jobs],ensure_ascii=False))
