import os
import shutil
import subprocess
import jinja2


def delete_folder(directory):
    try:
        if os.path.exists(directory):
            shutil.rmtree(directory)
    except:
        print('Could not delete the temp directory' + directory)


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error creating directory ' + directory)


def setup(tempdir):
    # deleteFolder(tempdir)
    create_folder(tempdir)
    return True


def copy_and_overwrite(from_path, to_path):
    if os.path.exists(to_path):
        shutil.rmtree(to_path)
    shutil.copytree(from_path, to_path)


def execute_helm(namevalues, name, tempvaluesgeneric):
    try:
        subprocess.check_call(
            ["helm", "upgrade", "--install", "-f", tempvaluesgeneric + "/" + namevalues, name, tempvaluesgeneric])
    except Exception:
        exit()


def render(dir_template, tempdir):
    loader_dir, template = split_dir_from_template(dir_template)
    loader = jinja2.FileSystemLoader(loader_dir)
    env = jinja2.Environment(autoescape=True, loader=loader)

    def env_override(value, key):
        return os.getenv(key, value)

    env.filters['ENV'] = env_override

    values = env.get_template(template)
    write_values(template, values.render(), tempdir)


def write_values(file, template_content, tempdir):
    with open(tempdir + "/" + file, "w") as fh:
        fh.write(template_content)


def split_dir_from_template(dir):
    split = dir.split("/")
    return "/".join(split[:-1]).replace(" ", ""), split[-1]


def verify_chart(path):
    try:
        subprocess.check_call(["helm", "lint", path])
    except Exception:
        exit()


def download_dependencies(path):
    try:
        subprocess.check_call(["helm", "dependency", "update", path])
    except Exception:
        exit()
