import argparse
import sys
import os
from doxybook.runner import run

def parse_options():
    parser = argparse.ArgumentParser(description='Convert doxygen XML output into GitBook or Vuepress markdown output.')
    parser.add_argument('-t', '--target', 
        type=str, 
        help='Select the target: Gitbook (default) or Vuepress, for example: "-t vuepress" or "-t gitbook"',
        required=False,
        default='gitbook'
    )
    parser.add_argument('-i', '--input', 
        type=str, 
        help='Path to doxygen generated xml folder',
        required=True
    )
    parser.add_argument('-o', '--output', 
        type=str, 
        help='Path to the destination folder',
        required=True
    )
    parser.add_argument('-s', '--summary', 
        type=str, 
        help='Path to the summary file which contains a link to index.md in the folder pointed by --input (default: false)',
        required=False
    )
    parser.add_argument('-d', '--debug', 
        type=bool, 
        help='Debug the class hierarchy (default: false)',
        required=False,
        default=False
    )
    parser.add_argument('--hints', 
        type=bool, 
        help='(Vuepress only) If set to true, hints will be generated for the sections note, bug, and a warning (default: true)',
        required=False,
        default=True
    )
    parser.add_argument('--ignoreerrors', 
        type=bool, 
        help='If set to true, will continue to generate Markdown files even if an error has been detected (default: false)',
        required=False,
        default=False
    )
    parser.add_argument('-a', '--allgenerator', 
        type=str, 
        help='Is generator all *.md in Summary',
        required=False,
        default='yes'
    )
    parser.add_argument('-p', '--type',
            default='all',
            help='create ALL doc or PART doc')

    parser.add_argument('-l', '--link',
            default='',
            help='use for PART doc')

    args = parser.parse_args()

    if args.target != 'gitbook' and args.target != 'vuepress':
        raise Exception('Unknown target: ' + str(args.target))

    if args.target == 'gitbook' and args.summary and not os.path.exists(args.summary):
        raise Exception('The provided summary file does not exist!')

    if os.path.isfile(args.output):
        raise Exception('The target output directory is a file!')

    return args

def main():
    args = parse_options()
    os.makedirs(args.output, exist_ok=True)

    run(
        input=args.input,
        output=args.output,
        target=args.target,
        hints=args.hints,
        debug=args.debug,
        ignore_errors=args.ignoreerrors,
        summary=args.summary,
        allgenerator=args.allgenerator,
        doc_type = args.type,
        rel_path = args.link,
    )
