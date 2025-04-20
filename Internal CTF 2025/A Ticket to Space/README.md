# A Ticket to Space

#### Category: Web Exploitation

#### Difficulty: Medium

#### Type: Black Box

#### Description: I have always wanted to go to space. Now they offer a program that will allow me to fulfill my dream! But the queue is a little long, and I'm not sure if I'll still be here when my turn arrives...  I wonder if there is a way to bypass the queuing system.

![image](https://github.com/user-attachments/assets/8c2f4250-53d8-463c-be5c-3828a186b3ab)


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
Access to `http://docker-ip-address:3000`

## Solution
<details>

Since the web exploitation is a black box challenge, source code are not provided and it is required for the players to perform analysis themself and figure out the possible vulnerability. Accessing to the website, a webpage will be displayed like this and it should simulate like a ticket queuing system.

<br>

![image](https://github.com/user-attachments/assets/1fd26ac1-3aa4-4dcb-b933-962368016e73)

<br>

When the 'Buy Ticket' button is clicked, an alert message 'Not your turn yet! Please Wait!' will appear as the user is not authorized to access the ticket purchasing site yet.

<br>

![image](https://github.com/user-attachments/assets/f7519d5c-1ae0-45f6-8703-a56137ebbc71)

<br>

To further understand on how does the website checks the user's authorization, inspecting the frontend side should provide some valuable information.

### Frontend Source Code (Javascript)
```javascript
 window.onload = function() {
    if (!localStorage.getItem("jwt")) {
    fetch("/genToken", {
        method: "GET",
        headers: {
        "Content-Type": "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {
        localStorage.setItem("jwt", data.token);
    })
    .catch(err => console.error("Error getting token:", err));
    }
    };
    
    function BuyTicket() {
    const token = localStorage.getItem("jwt");
    if (!token) {
        alert("No token found.");
        return;
    }
    fetch("/buyTicket", {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    })
    .then(async (response) => {
        if (!response.ok) {
            const data = await response.json();
            alert(data.message || "Access denied");
            return;
        }
        const html = await response.text();
        document.open();
        document.write(html);
        document.close();
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Something went wrong.");
    });
}
```
<br>

It seems that the website will fetch the `/genToken` to generate a unique Json Web Token (JWT) for each of the user and stored in the localStorage which will be retrieved later on to check the validity of the token in the `/buyTicket`. If the token validity returns invalid, it will deny the user access to the site. Now let's obtain the JWT from the localStorage for further analysis.

<br>

![image](https://github.com/user-attachments/assets/84c96782-0c5c-445b-95a5-6406a12eccb9)

<br>

When decoding the JWT using an online tool such as [jwt.io](https://jwt.io/). We can see that the JWT uses RS256 algortihm to secure their token. It also contain the payload `{"purchasePerm" : false}` which most likely is the mechanism used to check the validility of the token from the backend server. Therefore, changing the boolean of the payload to `{"purchasePerm" : true}` should work right? Unfortunately for RS256 algorithm, modifying the payload without a valid private key will not work because the server will use the public key to decode the token and checks the payload. Modifying the token without private key will cause the token to be not recognizable by the server and result invalid token.

<br>

![image](https://github.com/user-attachments/assets/e3985a60-d8de-43e7-b2d1-b683c4c95a48)


</details>
