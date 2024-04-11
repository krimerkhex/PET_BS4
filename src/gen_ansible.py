import logging
import yaml


class IndentDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(IndentDumper, self).increase_indent(flow, False)


def import_yaml():
    yml = None
    with open('../materials/todo.yml', 'r') as file:
        stream = file.read()
        logging.info(f"Reading todo.yml")
        yml = yaml.load(stream, Loader=yaml.loader.SafeLoader)
    return yml


def create_module(yml):
    ansable = [
        {"name": "package installation",
         "ansible.builtin.package": {"name": yml["server"]["install_packages"],
                                     "state": "present"}},
        {"name": "file copying",
         "ansible.builtin.copy": {"src": ["../src/" + yml["server"]["exploit_files"][0],
                                          "../src/ex01" + yml["server"]["exploit_files"][1]],
                                  "dest": ["/etc/" + yml["server"]["exploit_files"][0],
                                           "/etc/" + yml["server"]["exploit_files"][1]]}},
        {"name": "script launch",
         "ansible.builtin.command": ["python /etc/" + yml["server"]["exploit_files"][1] + " " +
                                     yml["bad_guys"][0] + ',' + yml["bad_guys"][1],
                                     "python /etc/" + yml["server"]["exploit_files"][0]]}
    ]
    return ansable


def export_yaml(ansible):
    try:
        with open("../materials/deploy.yml", 'w') as file:
            file.write(yaml.dump(ansible, Dumper=IndentDumper,
                                 default_flow_style=False, sort_keys=False))
    except Exception as ex:
        logging.exception("File doensn't opened", exc_info=True, sep='\n')


def main():
    yml = import_yaml()
    if yml is not None:
        logging.info("[SUCCESS] YML file wasn't empty, generation ansible module started")
        ansible = create_module(yml)
        export_yaml(ansible)
    else:
        logging.error("YML file was empty")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    main()
