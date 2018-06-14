#!/usr/bin/python3
import argparse
import pathlib
import rosdistro
import subprocess
import yaml


def main():
    parser = argparse.ArgumentParser(description='Pull the contents of a ROS distribution to disk.')
    parser.add_argument('--src-dir', type=pathlib.Path, required=True)
    parser.add_argument('--github-key', type=str)
    parser.add_argument('--repositories-file', type=pathlib.Path, default='catkin.repos')
    args = parser.parse_args()

    index = rosdistro.get_index(rosdistro.get_index_url())
    distro = rosdistro.get_distribution(index, 'locus')

    repositories = {}
    for repo in distro.repositories.items():
        repositories[repo[0]] = {
            'type': repo[1].source_repository.type,
            'url': repo[1].source_repository.url,  # TODO(pbovbel) insert github key into URL
            'version': repo[1].source_repository.version
        }

    args.src_dir.mkdir(parents=True, exist_ok=True)

    args.repositories_file.write_text(yaml.dump({'repositories': repositories}))

    subprocess.run(["vcs", "import", str(args.src_dir), "--input", str(args.repositories_file)], check=True)
    subprocess.run(["vcs", "pull", str(args.src_dir)], check=True)


if __name__ == '__main__':
    main()
