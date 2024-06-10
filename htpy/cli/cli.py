import argparse
from dataclasses import dataclass

from htpy.utils import html_to_htpy


@dataclass
class ConvertArgs:
    shorthand: bool
    format: bool
    files: list[str]
    output: list[str | None]


def main():
    global_parser = argparse.ArgumentParser(prog="htpy")
    subparsers = global_parser.add_subparsers(title="commands", help="commands")

    convert_parser = subparsers.add_parser(
        "convert", help="convert html to python (htpy)"
    )
    convert_parser.add_argument(
        "-s",
        "--shorthand",
        help="Use shorthand syntax for class and id attributes",
        action="store_true",
    )
    convert_parser.add_argument(
        "-f",
        "--format",
        help="Format output code (requires black installed)",
        action="store_true",
    )
    convert_parser.add_argument(
        "files",
        nargs="*",
        help="Optionally supply a files to parse (Requires -o)",
    )

    convert_parser.add_argument(
        "-o",
        "--output",
        nargs=1,
        help="Existing output directory to store parsed files",
    )

    def _convert_html(args: ConvertArgs):
        if args.files and not len(args.output) == 1:
            print("\nError: Output is required when files are provided.")
        else:
            convert_html_cli(args.shorthand, args.format, args.files, args.output[0])

    convert_parser.set_defaults(func=_convert_html)

    args = global_parser.parse_args()

    args.func(args)


if __name__ == "__main__":
    main()


def convert_html_cli(
    shorthand_id_class: bool, format: bool, files: list[str], output: str | None
):
    import time

    print("")
    print(f"HTML to HTPY converter")
    print(f"selected options: ")
    print(f"              format: {format}")
    print(f"  shorthand id class: {shorthand_id_class}")
    print(f"              output: {output}")
    print(f"               files: {files}")

    if files and output:

        failed_files: list[str] = []
        succeeded_files: list[str] = []
        for f in files:
            try:
                with open(f, "r") as r:
                    content = r.read()
                    htpy = html_to_htpy(content, shorthand_id_class, format)

                    new_filename = f"{output}/{f.split('.')[0]}.py"
                    with open(new_filename, "w") as w:
                        w.write(htpy)

                    succeeded_files.append(new_filename)
            except:
                failed_files.append(f)
                raise

        print(f"\nFiles written: {succeeded_files}")

        if failed_files:
            print(f"Failed files: {failed_files}")

    else:
        print("\nNo files selected. Paste html?")
        print(">>>>>>>>>>>>>>>>>>")
        print(">>> paste html >>>")
        print(">>>>>>>>>>>>>>>>>>\n")
        collected_text = ""
        input_starttime = None
        try:
            while True:
                user_input = input()
                if not input_starttime:
                    input_starttime = time.time()

                collected_text += user_input

                if input_starttime + 0.1 < time.time():
                    break

            print("\n##############################################")
            print("### serialized and formatted python (htpy) ###")
            print("##############################################\n")
            print(html_to_htpy(collected_text, shorthand_id_class, format))
        except KeyboardInterrupt:
            print("\nInterrupted")
