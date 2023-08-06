#!/usr/bin/python3

# imports

from .__init__ import __doc__ as description, __version__ as version
from argparse import ArgumentParser as Parser, RawDescriptionHelpFormatter as Formatter
from os import popen
from os.path import join as joinpath, split as splitpath, expanduser, abspath, isfile, split as splitpath
from sys import argv, exit
from time import localtime
from warnings import simplefilter
from libfunx import no_tag, find_not_in

# globals

class args:
    "container for arguments"
    pass 

# functions

def package_file(file):
    "return abspath of package local file"
    return joinpath(splitpath(__file__)[0], file)

def count_hash(line):
    """return number (0..6) of leading '#' chars in line
>>> for n in range(8): line = n * "#" + " xyz"; print((n, line, count_hash(line)))
(0, ' xyz', 0)
(1, '# xyz', 1)
(2, '## xyz', 2)
(3, '### xyz', 3)
(4, '#### xyz', 4)
(5, '##### xyz', 5)
(6, '###### xyz', 6)
(7, '####### xyz', 6)
"""
    for nhash, prefix in enumerate(["#","##","###","####","#####","######"]):
        if not line.startswith(prefix):
            return nhash
    else:
        return 6

def get_title(line):
    """extract title from line (removing '#' chars, HTML tags '<...>', and chapter numbering)
>>> get_title('### <a name="1.2.">1.2. On and Off</a>')
'On and Off'
"""
    result = no_tag(line)
    j = find_not_in(result, "# 0123456789.")
    return "" if j < 0 else result[j:].rstrip()

# main

def toc2md(argv):
    "Insert or update nested chapter numbering and linked Table Of Contents into a MarkDown file"

    # get arguments
    parser = Parser(prog="toc2md", formatter_class=Formatter, description=description)
    parser.add_argument('-H', '--user-guide', action='store_true', help="open User Guide in PDF format and exit")
    parser.add_argument("-V", "--version", action="version", version="toc2md " + version)
    parser.add_argument("-v", "--verbose", action="store_true", help="show what happens")
    parser.add_argument("file", nargs="?", help="markdown file to be backed up, read, processed and rewritten")
    parser.parse_args(argv[1:], args)
    if args.user_guide:
        toc2md_pdf = package_file("docs/toc2md.pdf")
        popen(f"xdg-open {toc2md_pdf} &")
        exit()
    
    # check arguments
    if not args.file:
        exit("ERROR: no file\n")
    args.file = abspath(expanduser(args.file))
    if not args.file.endswith(".md"):
        exit(f"ERROR: file {args.file!r} has no '.md' extension\n")
    if not isfile(args.file):
        exit(f"ERROR: file {args.file!r} not found\n")
        
    # copy file into backup
    backup = args.file[:-3] + "-%04d.%02d.%02d-%02d.%02d.%02d.md" % localtime()[:6]
    open(backup, "w").write(open(args.file).read())
    if args.verbose:
        print(f"file {args.file!r} has been backed up...\n...into {backup!r}")
    
    # read lines and chapters from file
    next_status = {(0, 1): 1, 
                   (1, 2): 2,
                   (2, 2): 3,
                   (3, 2): 3, (3, 3): 4,
                   (4, 2): 3, (4, 3): 4, (4, 4): 5,
                   (5, 2): 3, (5, 3): 4, (5, 4): 5, (5, 5): 6,
                   (6, 2): 3, (6, 3): 4, (6, 4): 5, (6, 5): 6, (6, 6): 7,
                   (7, 2): 3, (7, 3): 4, (7, 4): 5, (7, 5): 6, (7, 6): 7}
    lines = []; chapters = []; numbers = [0]; status = 0; jline_toc = -1
    for jline, line in enumerate(open(args.file)):
        line = line.rstrip()
        nhash = count_hash(line)
        if nhash:
            try:
                status = next_status[(status, nhash)]
            except KeyError:
                exit(f"ERROR: heading sequence error in line {jline+1} {line!r}\n")
            if status == 2:
                jline_toc = jline
            elif status > 2:
                nest = status - 2
                indent = (nest - 1) * 4 * " "
                numbers = numbers[:nest-1] + [numbers[nest-1] + 1] if nest <= len(numbers) else numbers + [1]
                label = "".join(f"{n}." for n in numbers)
                title = get_title(line)
                hashes = nhash * "#"
                chapters.append(f"{indent}- [{label} {title}](#{label})")
                line = f'{hashes} <a name="{label}">{label} {title}</a>'
            lines.append(line)
        elif status != 2:
            lines.append(line)
            
    # rewrite back lines and chapters into file
    with open(args.file, "w") as output: 
        for jline, line in enumerate(lines):
            print(line, file=output)
            if jline == jline_toc:
                print(file=output)
                for chapter in chapters:
                    print(chapter, file=output)
                print(file=output)
    if args.verbose:
        print(f"file {args.file!r} has been updated")
            
def main():
    try:
        simplefilter("ignore")
        toc2md(argv)
    except KeyboardInterrupt:
        print()

if __name__ == "__main__":
    main()
