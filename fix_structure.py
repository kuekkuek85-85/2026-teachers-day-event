import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

fp = r'C:\claude_code_project\2026_스승의날_이벤트\docs\1-1.html'
with open(fp, encoding='utf-8') as f:
    src = f.read()

TAGS = ['div','span','p','sc-if','svg','g','text','h1','h2','h3','section','a','button','textarea','tspan','defs','style','b','strong','small','em','li','ul']
tag_alt = '|'.join(TAGS)

# Find every '/TAG>' whose preceding char is not '<'
pat = re.compile(r'(.)/(?:' + tag_alt + r')>')
fixes = []
def show(m):
    return m.group(0)

count = 0
out = []
i = 0
# Use finditer to insert '<' where the char before '/tag>' is not '<'
def repl(m):
    global count
    prev = m.group(1)
    if prev == '<':
        return m.group(0)  # already valid
    count += 1
    # insert '<' between prev char and '/tag>'
    return prev + '<' + m.group(0)[1:]

# Exclude the dc-script JS region from modification
js_start = src.index('<script type="text/x-dc"')
js_end = src.index('</script>', js_start)
head, js_block, tail = src[:js_start], src[js_start:js_end], src[js_end:]
new_head = pat.sub(repl, head)
new_tail = pat.sub(repl, tail)
new_src = new_head + js_block + new_tail
print(f'Closing tags missing "<" that were fixed: {count}')

# Verify div balance now via simple count
od = len(re.findall(r'<div\b', new_src))
cd = len(re.findall(r'</div>', new_src))
print(f'After fix: <div> {od}  </div> {cd}  diff {od-cd:+d}')

with open(fp, 'w', encoding='utf-8') as f:
    f.write(new_src)
print('Saved.')
