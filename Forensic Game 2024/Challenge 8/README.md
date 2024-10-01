# Title: Challenge 8

## Location: Cyber Range @APU

### Description: We intercepted the culprits' packets as they communicated about where they were hiding the money. The message appears to be encrypted, can you find a way to see what they are talking about and where they are hiding the money?

#### File: capturedpacket.pcapng

#### File in Cyber Range's PC: chat.txt


## Solution

Firstly, the challenge provided one pcap file called `capturedpacket.pcapng` so players should know that this challenge involve with network analysis. Tools like Wireshark is very useful for network analysis and they are pre-installed in Kali Linux. This challenge also requires the player to travel to another location which is CyberRange@APU and there's a file called `chat.txt` that contains a chat log of the three masterminds which stored inside the PCs. When the players open the pcap file, it seems that the traffic is encrypted so we need to find a way to decrypt the messages.

![image](https://github.com/user-attachments/assets/c6c23616-ba16-46b3-88b9-608fa8efed28)

When players analyze the chat log, they will eventually encounter a suspicious URL link that may lead to the culprits stash.

![image](https://github.com/user-attachments/assets/110cf199-eb67-498c-9014-9598ee690b94)

When they enter the link, they should see that it is a dropbox that contains multiple different files such as images and text file.

![image](https://github.com/user-attachments/assets/e2f4d40c-4993-464a-b437-a961e9209ef8)

However, the file that should attracts the most attention is the `SSLKEYLOG` file. This file is very important to decrypt a TLS traffic because it logged the information about the secrets used in a TLS connection. Then, players should download the file into their PC for next step.

![image](https://github.com/user-attachments/assets/e71bcc0a-6af1-4ac4-b4b0-65a53edd2482)

Now that the players have the `SSLKEYLOG` file, they can decrypt the packet using `Wireshark`. For more info you can read: https://wiki.wireshark.org/TLS. When opened the Wireshark, the players should first go to `preferences`.

![image](https://github.com/user-attachments/assets/a5b04716-35c7-4531-839a-f36ccd588c08)

Then, locate to `protocols` and expand it.

![image](https://github.com/user-attachments/assets/10eeff51-45fa-4382-82de-b4b2296397a9)

After that, scroll all the way down until `TLS` is found.

![image](https://github.com/user-attachments/assets/d285144c-0cfc-4077-a297-9d1ae2deabd8)

In the `(Pre)-Master-Secret Log`, the players can simply browse and use the `SSLKEYLOG` file that they downloaded earlier. After completing the steps, just click OK.

![image](https://github.com/user-attachments/assets/5d16424e-34ad-4397-96c3-f00d33b8e7d3)

The packet now should be decrypted and the HTTP protocols can be read in plaintext.

![image](https://github.com/user-attachments/assets/10bfb963-44de-4685-b444-1c29fa4c6815)

Now the players can filter the protocols by just using `HTTP` in Wireshark and find any relevant information from the packets.

![image](https://github.com/user-attachments/assets/e83adcfe-0783-44b7-8d96-89481550c831)

Players should eventually found a suspicious image that called `location.png` from one of the HTTP stream as that is the objective of the challenge.

![image](https://github.com/user-attachments/assets/3573dca5-eb90-410f-94e2-e2bf31c59dbb)

Now, they can try to download the image using one of the Wireshark function which is `Export Objects`.

![image](https://github.com/user-attachments/assets/747aa991-5467-4427-b625-c2c128acb628)

After that, the players can download the image by simply going to the HTTP stream and export the `image/png`. 

![image](https://github.com/user-attachments/assets/a39cdbef-d460-409a-9d5f-912d083a6934)

To download the image, just save the image into any of your designated folder.

![image](https://github.com/user-attachments/assets/f82a9efd-d264-43ab-ac3c-04a528586525)

Finally, the players should open up the image from the folder that they downloaded and they should be able to see the location of the place which is the flag.

![image](https://github.com/user-attachments/assets/182cb031-df9c-47c3-94e4-9f448cc8cb11)

### Flag:FG24{Southern_Riverbank}
