import sys
import xml.dom.minidom

x = "1. Suma de enteros base UNO\SU-MTDeterminista1C.jff"
doc = xml.dom.minidom.parse(x)

states = {}
initial = []
final = []

for st in doc.getElementsByTagName("state"):
    id = st.getAttribute("id")
    name = st.getAttribute("name")
    states[id] = name

    if st.getElementsByTagName("initial").length > 0:
        initial.append(name)
    if st.getElementsByTagName("final").length > 0:
        final.append(name)


print(f"name: {x}")
print(f"init: {','.join(initial)}")
print(f"accept: {','.join(final)}")


for tr in doc.getElementsByTagName("transition"):
    # <from>5</from>
    # <to>5</to>
    fr = tr.getElementsByTagName("from")[0].firstChild.nodeValue
    to = tr.getElementsByTagName("to")[0].firstChild.nodeValue

    read = {}
    write = {}
    move = {}

    # <read tape="1">1</read>
    for e in tr.getElementsByTagName("read"):
        tape = e.getAttribute("tape") or 0
        val = e.firstChild and e.firstChild.nodeValue
        read[int(tape)] = val
    # <write tape="1">1</write>
    for e in tr.getElementsByTagName("write"):
        tape = e.getAttribute("tape") or 0
        val = e.firstChild and e.firstChild.nodeValue
        write[int(tape)] = val
    # <move tape="1">R</move>
    for e in tr.getElementsByTagName("move"):
        tape = e.getAttribute("tape") or 0
        val = e.firstChild and e.firstChild.nodeValue
        move[int(tape)] = val

    mconv = {
        "L": "<",
        "R": ">",
        "S": "-"
    }
    rds = ",".join(str(v or "_") for k, v in sorted(read.items()))
    wrs = ",".join(str(v or "_") for k, v in sorted(write.items()))
    mvs = ",".join(mconv[v] for k, v in sorted(move.items()))
    print(f"{states[fr]},{rds}")
    print(f"{states[to]},{wrs},{mvs}")
