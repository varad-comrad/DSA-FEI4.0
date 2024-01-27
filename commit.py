import subprocess, argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--message', type=str, required=True)
    parser.add_argument('-sm', '--submodule-message', type=list[str], nargs='*', required=False)
    parser.add_argument('-b', '--branch', type=str, default='main')
    return parser.parse_args()

def run_command(command, cwd='.'):
    output = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=cwd).stdout
    return output

def get_submodules():
    command = 'git submodule status'
    output = str(run_command(command))
    submodules = []
    for line in output.splitlines():
        if line:
            submodules.append(line.split()[1])
    return submodules

def main():
    args = parse_args()
    add_command = 'git add .'
    commit_command_template = 'git commit -m "{}"'
    push_command_template = 'git push -u origin {}'
    merge_submodules = 'git submodule update --remote --merge'
    print(run_command(merge_submodules), flush=True)
    if not args.submodule_message:
        args.submodule_message = [args.message] * len(get_submodules())
    for submodule, message in zip(get_submodules(), args.submodule_message):
        command = '&& '.join(
            (add_command, commit_command_template.format(message), push_command_template.format(args.branch)))
        print(run_command(command, cwd=submodule), flush=True)
    command = '&& '.join(
        (add_command, commit_command_template.format(args.message), push_command_template.format(args.branch)))
    print(run_command(command), flush=True)

if __name__ == '__main__':
    main()