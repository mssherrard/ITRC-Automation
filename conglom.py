import re

crsre = r"([A-Z] [A-Z][A-Z]?|[A-Z][A-Z] [A-Z]|[A-Z]{2,4})\s*" # department
        r"(\d{3,4}\w?)(?:\s*-\s*|\s+)"  # course number
        r"(\w{1,2})(?:\s+|:\s*)"        # section number
        r"(.*)\s*\((\d+)\),\s*"         # course title, crn
        r"([A-Z]+)\s+(\d{2,4})"         # term, year

def parse(courses):
    blah = []
    for crsln in courses:
        match = re.match(crsre, crsln, re.I)
        if match:
            dept = match.group(1).upper()
            cnum = match.group(2).upper()
            sect = match.group(3)
            desc = match.group(4)
            term = match.group(5)
            year = match.group(6)
            if len(cnum) == 3 or len(cnum) == 4 and not cnum.isdigit():
                cnum = cnum[0] + cnum
            if len(sect) == 1:
                sect = '0' + sect
        else:
            print "no match"
    return

def merge(clist, title, instr, term, year):
    ctree = {}
    term = term.capitalize()
    tcode = {'Fall':  (int(year)+1)*100 + 10,
             'Spring': int(year)*100 + 20,
             'Summer': int(year)*100 + 30}[term]
    for dept, cnum, sect in clist:
        ctree.setdefault(dept, {}).setdefault(cnum, set()).add(sect)
    if len(ctree) > 1:
        cname = ' / '.join(dept + ' ' + cnum + ' - ' + ', '.join(sorted(ctree[dept][cnum]))
                         for dept in sorted(ctree) for cnum in sorted(ctree[dept]))
    else:
        cname = ' / '.join(dept + ' ' + ' / '.join(cnum + ' - ' + ', '.join(sorted(ctree[dept][cnum]))
                         for cnum in sorted(ctree[dept])) for dept in sorted(ctree))
    lname = '%s: %s (%s), %s %s' % (cname, title, instr, term, year)
    foo = '-'.join(dept+cnum for dept in sorted(ctree) for cnum in sorted(ctree[dept]))
    sname = '%s-%s.%s' % (foo, instr, tcode)


def elide(course):
    sects = sorted(course)
    idx = 0
    beg = 0
    while idx <= len(sects):
        if idx < len(sects) and elen == int(sects[idx]) - int(sects[beg]):
            elen += 1
        else:
            if idx - beg > 2:
                sects[beg:idx] = [sects[beg] + ' ... ' + sects[idx-1]]
                idx = beg + 1
            beg = idx
        idx += 1
    return sects
##    for idx in range(len(sections)):
##        if int(sections[idx]) - int(sections[idx-1]) > 1:
#    last = ?
    for sect in sorted(course):
        if int(sect) - int(last) > 1:
            if int(last) - int(mark) > 1:
                res += ' ... ' + last + ', '
            else:
                res += ', ' + last
            res += sect
            mark = sect
        last = sect

def foo(courses):
    cd = {}
    for course in courses:
        cd.setdefault(course[0], {}).setdefault(course[1], {}).setdefault(course[2], course)
    if len(cd) > 1:
        res = ' / '.join(dept + ' ' + cnum + ' - ' + ', '.join(sorted(cd[dept][cnum]))
                         for dept in sorted(cd) for cnum in sorted(cd[dept]))
    else:
        res = ' / '.join(dept + ' ' + ' / '.join(cnum + ' - ' + ', '.join(sorted(cd[dept][cnum]))
                         for cnum in sorted(cd[dept])) for dept in sorted(cd))
    return res
