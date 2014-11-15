import argparse
import os
import glob
import re
import subprocess

file_re = re.compile(r'(?:senior|intermediate)_contest[1-4]_(.*)_python([23])\.py', re.IGNORECASE)

def run_one(directory, filename, version):
    cmd = 'python{} {} < {}'.format(version, filename, os.path.join(directory, 'in.txt'))
    try:
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return proc.communicate()
    except:
        print 'stopped on file', filename
        raise

def run_all(directory):
    results = {}
    for f in glob.glob('{}/*.py'.format(directory)):
        version = file_re.search(f).group(2)
        results[f] = run_one(directory, f, version)
    return results

def score_output(this, correct):
    score = 0
    res = []
    for t, c in zip(this, correct):
        if c in t:
            score += 1
            res.append((t, True))
        else:
            res.append((t, False))
    return score, res

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', help='Directory to use to check', type=str)
    parser.add_argument('-r', '--html', help='Create html report', action='store_true')
    args = parser.parse_args()

    with open(os.path.join(args.directory, 'out.txt')) as f:
        correct_out = f.read().split('\n')
    max_score = len(correct_out)

    results = run_all(args.directory)

    for i in results:
        out = results[i][0].strip().split('\n')
        score, out = score_output(out, correct_out)
        results[i] = {'out': out,
                      'err': results[i][1],
                      'score': score,
                      'name': file_re.search(i).group(1)}

    names = sorted(results.keys())
    for i in names:
        print '{}: {}'.format(results[i]['name'], results[i]['score'])

    if args.html:
        import jinja2
        with open('template.html') as f:
            template = jinja2.Template(f.read().decode('utf-8'))
        with open(os.path.join(args.directory, 'in.txt')) as f:
            inp = f.read()
        with open(os.path.join(args.directory, 'report.html'), 'w') as f:
            f.write(template.render({
                'results': results,
                'names': names,
                'max_score': max_score,
                'directory': args.directory,
                'input': inp,
                'correct_output': '\n'.join(correct_out)
            }).encode('utf-8'))

        import webbrowser
        webbrowser.open(os.path.join(args.directory, 'report.html'))
