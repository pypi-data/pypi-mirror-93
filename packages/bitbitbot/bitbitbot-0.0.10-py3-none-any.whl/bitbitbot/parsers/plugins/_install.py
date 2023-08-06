import json
import subprocess
from pathlib import Path
from re import compile
from urllib import request

GITHUB_RE = compile(r'https://github.com/(\w+)/(\w+).*/(\w+)?$')


def download_files(api_url: str) -> None:
    response = request.urlopen(api_url)
    if response.status != 200:
        print(f'Received an invalid response status from the URL: {response.status}')

    root_path = Path('plugins')
    artifact_list = json.loads(response.read())
    for artifact in artifact_list:
        if artifact.get('type', '') == 'file':
            artifact_name = artifact.get('name', '')
            print(f'Downloading {artifact_name}...', end='')

            artifact_response = request.urlopen(artifact.get('download_url'))
            if artifact_response.status != 200:
                print('Failed')

            file_path = root_path / artifact.get('path', '')
            file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, 'w+') as f:
                f.write(artifact_response.read().decode())
            print('OK')

            if artifact_name == 'requirements.txt':
                print('Installing Plugin Requirements', end='')
                subprocess.run(["pip", "install", "-r", file_path])
                print('OK')

        elif artifact.get('type', '') == 'dir':
            download_files(artifact.get('url', ''))



def install_from_github(args):
    print('Installing From GitHub')

    github_url = args.path
    if not github_url.endswith('/'):
        github_url += '/'

    re_match = GITHUB_RE.match(args.path)
    if re_match is None:
        print('Invalid GitHub URL')
        return

    owner, repo, sub_path = re_match.groups()
    api_url = 'https://api.github.com/repos/{0}/{1}/contents/'.format(owner, repo)
    if sub_path is not None:
        api_url += sub_path

    download_files(api_url)
    print('Plugin installed successfully')


def install_from_zip(args):
    print('Not implemented yet')


def install(args):
    if args.path.startswith('https://github.com'):
        install_from_github(args)
    elif args.path.endswith('.zip'):
        install_from_zip(args)


def plugin_install_parser(plugins_subparsers):
    install_parser = plugins_subparsers.add_parser(
        'install',
        help='Manage your plugins for the bot',
    )

    install_parser.add_argument(
        'path',
        help='Path to the plugin you would like to install. Can be a local path to a zip, or a GitHub URL'
    )
    install_parser.set_defaults(func=install)
