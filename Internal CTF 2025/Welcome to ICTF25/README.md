# Welcome to ICTF25

#### Category: Misc

#### Difficulty: Easy

#### Description: Welcome to Internal CTF 2025. We are glad to have you on board and we will offer you a flag as a welcome gift. However, before proceeding to the competition, we need to check your sanity by winning this game.

#### Preview:
![image](https://github.com/user-attachments/assets/277eb1e3-31b1-4cf6-974f-8818307021d4)

![image](https://github.com/user-attachments/assets/72b64831-abf4-4894-9181-055863a1b513)

![image](https://github.com/user-attachments/assets/5da7e339-c39b-49a6-9f66-e1582aefd7aa)

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
Access to `http://docker-ip-address:8080`

## Solution
<details>

Since this is just a sanity check and a welcome flag challenge, nothing crazy is required to solve the challenge. All we have to do is defeat the 7 bosses called `Alcyone, Asterope, Celaeno, Electra, Maia, Merope, and Taygete` which is needed to win the game. Completing the game will allow us to obtain the flag.

![image](https://github.com/user-attachments/assets/08b8f7d2-52cb-4e65-9d59-4ee1a2e88056)

### Flag
> ICTF25{w3lc0me_70_ICTF25_3527d3288d718eb52f97ab20cacba9cd}

Note: **I created this game because our theme is 8-bit space :P. I apologize to those who struggle to win the game. I have already attempted to reduce the difficulty and to those who won, I hope you had fun!**

</details>
