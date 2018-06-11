#!/usr/bin/python3
import pathlib
import rosdistro
import subprocess
import yaml


def main():
    # TODO(pbovbel) make args
    rosdistro_index = pathlib.Path("tailor-distro/rosdistro/index.yaml").resolve().as_uri()

    index = rosdistro.get_index(rosdistro_index)
    distro = rosdistro.get_distribution(index, "locus")

    repositories = {}
    for repo in distro.repositories.items():
        repositories[repo[0]] = {
            'type': repo[1].source_repository.type,
            'url': repo[1].source_repository.url,
            'version': repo[1].source_repository.version
        }

    repositories_file = pathlib.Path('catkin.repos')
    repositories_file.write_text(yaml.dump({'repositories': repositories}))

    workspace_dir = pathlib.Path("workspace/src")
    try:
        workspace_dir.mkdir(parents=True)
    except FileExistsError:
        pass

    subprocess.check_call(["vcs", "import", str(workspace_dir), "--input", str(repositories_file)])


if __name__ == '__main__':
    main()
