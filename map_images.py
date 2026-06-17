import sys, io, os, re, shutil, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import openpyxl

wb = openpyxl.load_workbook('data/1-2.xlsx', read_only=True, data_only=True)
ws = wb.active
rows = list(ws.iter_rows(values_only=True))
students = []
for r in rows[1:]:
    if not r or not r[1]: continue
    students.append({'id': int(r[0]), 'name_full': str(r[1]).strip()})

SRC = 'images/1-2'
all_files = [f for f in os.listdir(SRC) if not f.startswith('.') and os.path.isfile(os.path.join(SRC,f))]

def base_name(full):
    m = re.match(r'([가-힣A-Za-z]+)\s*\d{5}', full)
    return m.group(1) if m else full
stu_by_name = {base_name(s['name_full']): s for s in students}

def korean_name(s):
    m = re.search(r'([가-힣]{2,4})\s*\d{5}', s)
    return m.group(1) if m else None

named = {}      # student_id -> filename (files that map to a student)
unnamed = []    # files without a student match (e.g. student-01.png)
for f in all_files:
    nm = korean_name(f); sid = None
    if nm and nm in stu_by_name:
        sid = stu_by_name[nm]['id']
    else:
        for bn, s in stu_by_name.items():
            if bn in f:
                sid = s['id']; break
    if sid and sid not in named:
        named[sid] = f
    else:
        unnamed.append(f)

# build ordered gallery list: named by student id, then unnamed (sorted for stability)
ordered = [(sid, named[sid]) for sid in sorted(named.keys())]
for f in sorted(unnamed):
    ordered.append((None, f))

print(f'Total images: {len(all_files)} | named->student: {len(named)} | unnamed: {len(unnamed)}')

# clear old dest student files
dest_dir = 'docs/images/1-2'
os.makedirs(dest_dir, exist_ok=True)
for f in os.listdir(dest_dir):
    if f.startswith('student-'):
        os.remove(os.path.join(dest_dir, f))

mapping = []
for gi, (sid, src_f) in enumerate(ordered, 1):
    ext = os.path.splitext(src_f)[1].lower().lstrip('.')
    if ext == 'jpeg': ext = 'jpg'
    dest = f'student-{gi:02d}.{ext}'
    shutil.copy(os.path.join(SRC, src_f), os.path.join(dest_dir, dest))
    nm = next((s['name_full'] for s in students if s['id']==sid), '(이름미상)') if sid else '(이름미상)'
    mapping.append({'gi':gi,'sid':sid,'name':nm,'ext':ext})
    print(f'  student-{gi:02d}.{ext}  <- {nm}  ({src_f[:38]})')

json.dump(mapping, open('_img_map_1-2.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'\nTotal gallery images: {len(mapping)}  -> _img_map_1-2.json')
