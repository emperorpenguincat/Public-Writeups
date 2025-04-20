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

When the 'Buy Tickets' button is clicked, an alert message 'Not your turn yet! Please Wait!' will appear as the user is not authorized to access the ticket purchasing site yet.

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

When decoding the JWT using an online tool such as [jwt.io](https://jwt.io/). We can see that the JWT uses RS256 algortihm to secure their token. It also contain the payload `{"purchasePerm" : false}` which most likely is the mechanism used to check the validility of the token from the backend server. Therefore, changing the boolean of the payload to `{"purchasePerm" : true}` should work right? Unfortunately for RS256 algorithm, modifying the payload without a valid private key will not work because the server will use the public key to decode the token and checks the payload. Modifying the token without private key will cause the token to be not recognizable by the server and result in invalid token.

<br>

![image](https://github.com/user-attachments/assets/e3985a60-d8de-43e7-b2d1-b683c4c95a48)

<br>

Thus, the website may have two potential vulnerabilities which are [JWT Algorithm "None"](https://medium.com/@phosmet/forging-jwt-exploiting-the-none-algorithm-a37d670af54f) or [JWT Algorithm Confusion](https://portswigger.net/web-security/jwt/algorithm-confusion). Let's first explore the algorithm "None" exploit and determine whether it works. We can use jwt.io to switch the algorithm to `none` and forged a token containing a header like `{"alg" : "none" , "type" : "JWT"}` and also change the payload to `{"purchasePerm" : true}`. The forged token will look something like this `eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJwdXJjaGFzZVBlcm0iOnRydWUsImV4cCI6MTc0NTE2ODg5OCwiaWF0IjoxNzQ1MTY1Mjk4fQ.`.

<br>

![image](https://github.com/user-attachments/assets/8a690b70-a261-44f6-860d-5eadd8209dff)

<br>

Then, we can replace the token in the localStorage with the forged token and attempt to access the `/buyTicket`. As a result, the algorithm "None" exploit does not work because the server will not accept token with "None" algorithm so it returns 'Token Authentication Failure'. Therefore, the JWT Algorithm "None" is not the solution ❎ and now we only have one possible vulnerability left which is JWT Algorithm Confusion.

<br>

![image](https://github.com/user-attachments/assets/efe7c9ab-7860-4031-bb1b-997b62e70bcc)

<br>

JWT Algorithm Confusion require us to retrieve the public key which will be used as the HMAC shared secret key after changing the algorithm to HS256 in the JWT header. Most of the time server will exposed their public keys in common path like `/jwks.json` , `/known-path/jwks.json`, & `/public.pem`. However, after several attempts on trying to retrieved the exposed public keys through known path has resulted in nothing. We can assume that the server was configured properly to ensure that the public key does not get exposed.

![image](https://github.com/user-attachments/assets/3d0a6bc1-faa1-493b-bbd4-203219c14021)

<br>

Fortunately, there is an interesting method that can be used to retrieved the public keys if they are not exposed. A great tool developed by nu11secur1ty called [rsa_sign2n](https://github.com/nu11secur1ty/rsa_sign2n/blob/main/README.md) can derived the public keys from existing tokens which we need to generated two tokens from the website for the tool to work.

First Token: `eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJwdXJjaGFzZVBlcm0iOmZhbHNlLCJleHAiOjE3NDUxNzc2MzgsImlhdCI6MTc0NTE3NDAzOH0.iTWhbTm90rdNtA10xmwiV0I7S-eD1veCkDgCqbBt5wer6ds1sHJDl5tNZQZcnwfBtYiaMhNG-DqTB7VfTbaYTWJRHNxr6n_UJmXB_XjWBtNkIpGwPHwkJBmebngg-VZuXOvo2NP8wv0TpdF3GRLQENonGFY37l5cYmATtKsNBUlTrvKwp0KLrLpIS8-uufXXkxha5SL6sDmj5z9Mmhwv-At7O0C4ZE8cijfhj48KXWcHk1fQFl1lYVPovqygh3tkJOW2avUO0HehDs6o5YX833aFhOox9kya7DbpPBcW9UEh62_EfFk2L1G1xgZg04vHcTzFYxrX62oaz804FyZHRQ`

After deleting the token and refresh the page will generate another new token.

Second Token: `eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJwdXJjaGFzZVBlcm0iOmZhbHNlLCJleHAiOjE3NDUxNzc2NTcsImlhdCI6MTc0NTE3NDA1N30.GMSDZvtmFlYGT8dcpk04rHWx6PDM-4DAuzzSXtuvRLfp9-IlVxuwe2MsjzjBGIFU9NLrBhxMkruqm2HcNrDHVkz-NUVDKWmLRED0_VJ9FGwIEARkkZqS-dHXA56x0QxGpUVWSq43_1u_qFi8ZczYAr_O9iXEDmTnBFl2Xu_zLZ0OYOlhKSEnCiGbWUlju2UH-nflysT_I7ENrUTFp_wixpPNYVxfZWLk16ixarISbOixvMdL5rYbYZmPEwos5Lz0-ix4gxmPcY1J2luLRhhQPdkaqKBwMzpSQjwex6N63gHt7kGk_kVfHr1B0L-CIYPazNBn9W5qQcUUVTbvVbzBlg`

Now we have two tokens ready and we can use the tool after successful installation. 

</details>
