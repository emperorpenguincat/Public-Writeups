# A Ticket to Space

#### Category: Web Exploitation

#### Difficulty: Medium

#### Description: I have always wanted to go to space. Now they offer a program that will allow me to fulfill my dream! But the queue is a little long, and I'm not sure if I'll still be here when my turn arrives...  I wonder if there is a way to bypass the queuing system.

![image](https://github.com/user-attachments/assets/8c2f4250-53d8-463c-be5c-3828a186b3ab)


## Set Up

Ensure that docker is installed in your virtual machine before the set up.

#### [1] Build challenge Docker image 
`sudo docker build -t chall .`

#### [2] Run the image inside a container
`sudo docker run -d chall`

#### [3] Get Docker container IP address
`sudo docker inspect <container-id> | grep 'IP'`

#### [4] Access challenge website
Access to `http://docker-ip-address:3000`

## Solution
<details>

  
</details>
