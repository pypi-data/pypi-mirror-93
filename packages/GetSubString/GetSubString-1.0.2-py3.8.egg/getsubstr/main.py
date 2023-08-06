import sys
import re
from argparse import ArgumentParser
from .setuptools import get_file_content


def get_substring(regexp_pattern: str, line: str, output_format: str = None, join_with: str = None) -> str:
    def _join_matches_into_list(_matches: list, _append_list: list = None) -> list:
        if _append_list is None:
            _append_str = list()
        for item in _matches:
            if type(item) == tuple:
                _join_matches_into_list(item, _append_list)
            else:
                _append_list.append(str(item))
        return _append_list

    if not join_with:
        join_with = "\t"
    matches = re.findall(regexp_pattern, line)
    if matches:
        if output_format:
            return output_format.format(*_join_matches_into_list(matches))
        return join_with.join(matches)
    return ""


def postprocess(result: str, strip: bool, lcut: int, rcut: int, lwrap: str, rwrap: str, find_replace: str) -> str:
    if strip:
        result = result.strip()
    if lcut:
        result = result[lcut:]
    if rcut:
        result = result[:rcut]
    if lwrap:
        result = "{}{}".format(lwrap, result)
    if rwrap:
        result = "{}{}".format(result, rwrap)
    if find_replace:
        find, replace = find_replace.split("::")
        result = result.replace(find, replace)
    return result


def _handle_args() -> tuple:
    version = get_file_content("./VERSION")
    parser = ArgumentParser(description=f"GetSubStr v{version} \nGet substring of each stdout line based on regexp.")
    parser.add_argument("regexp_pattern", type=str, help="Regexp pattern")
    parser.add_argument("-l", "--left-cut", dest="cut_left", type=int, help="Cut N chars from left side of result")
    parser.add_argument("-r", "--right-cut", dest="cut_right", type=int, help="Cut N chars from right side of result")
    parser.add_argument("--lwrap", dest="l_wrap", type=str, help="Wrap results from left side by specified char(s)")
    parser.add_argument("--rwrap", dest="r_wrap", type=str, help="Wrap results from left side by specified char(s)")
    parser.add_argument("-s", "--strip", dest="strip", default=False, action="store_true", help="Strip spaces from left and right side of result")
    parser.add_argument("-j", "--join-results", dest="join_results", type=str, help="Join all results with specified char(s)")
    parser.add_argument("--join-matches", dest="join_matches", type=str, help="Join more regexp matches with specified char(s). Default is TAB \\t")
    parser.add_argument("-f", "--find-replace", dest="find_replace", type=str, help="Find string and replace it with another string. It have to be defined in following format \"find::replace\"")
    parser.add_argument("-o", "--output-format", dest="output_format", type=str, help="Output format for matches (Best if you are using regexp groups). ex: \"myId:{1} yourId:{2}\"")
    parser.add_argument("-i", "--ignore-errors", dest="ignore_errors", default=False, action="store_true", help="Ignore errors caused regexp.")
    args = parser.parse_args()
    return args


def main():
    args = _handle_args()
    result_list = []
    for line in sys.stdin:
        try:
            result = get_substring(args.regexp_pattern, line, output_format=args.output_format, join_with=args.join_matches)
            result = postprocess(result, args.strip, args.cut_left, args.cut_right, args.l_wrap, args.r_wrap, args.find_replace)
            if args.join_results:
                result_list.append(result)
            else:
                sys.stdout.write("{}\n".format(result))
        except Exception as ex:
            if not args.ignore_errors:
                sys.stderr.write("\33[31mError\33[0m: {}\n".format(ex))
    if result_list:
        sys.stdout.write("{}\n".format(args.join_results.join(result_list)))


if __name__ == '__main__':
    main()
