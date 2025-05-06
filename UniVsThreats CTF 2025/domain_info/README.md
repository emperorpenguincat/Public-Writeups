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

![image](https://github.com/user-attachments/assets/7a2594fa-fe26-4256-9c65-0fc537586de7)

![image](https://github.com/user-attachments/assets/4003346f-4e69-40c1-afbf-4b83d0678f85)

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

#### Set up a ngrok TCP tunnel

*Note: To create TCP tunneling using ngrok, it is required to fill credit card info into your account but don't worry. It is still free.*

`ngrok tcp 1337`

#### Set up a nc listener

`nc -lvnp 1337`

#### Fill up the host and port provided by ngrok

![image](https://github.com/user-attachments/assets/965a1089-0260-4c5d-b0c5-08125f58bb59)

![image](https://github.com/user-attachments/assets/231f603d-5fb5-4bbb-8fa6-a1b2c6e1341d)

![image](https://github.com/user-attachments/assets/42a50d9d-df3e-4a2b-8ed9-cca4358eb3a0)

![image](https://github.com/user-attachments/assets/7d7d94fc-3833-4aec-a8c4-c692e2a4a324)

![image](https://github.com/user-attachments/assets/d31e6ea9-1e77-40e4-878a-14a1b37dbbb1)

![image](https://github.com/user-attachments/assets/a08d6ed9-c5e4-4217-8a89-6f9b90c4068f)

![image](https://github.com/user-attachments/assets/bcf6fbc3-7431-45d7-a3c1-dca89b564344)

#### Flag
> UVT{M4l1c10us_Wh0_1s_C0mmand_4nd_upl0ad}

</details>
