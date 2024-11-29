import sys
from jinja2 import Environment, FileSystemLoader


def main(template_file, year, day):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(template_file)
    print(template.render(year=year, day=day))


if __name__ == "__main__":
    template_file, year, day = sys.argv[1:]
    main(template_file, year, day)
