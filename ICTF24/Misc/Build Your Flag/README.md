# Challenge: Build Your Flag

### Difficulty: Easy
## Category: Misc
### Description: Timmy is a very lazy person. Instead of hiding the flag as instructed, he insisted that we construct it ourselves using this text file. Don't be like Timmy.

The challenge provided a large text file and contains random characters that might seems confusing. 

![image](https://github.com/emperorpenguincat/CTF-Writeups/assets/110463026/e6e97603-5b24-45b6-acb3-4dfb07c7d809)

Firstly, we need to understand that the flag format is important which is `ICTF24{flag}`.Now we need to oberserve the text file and seek for the flag format.

![Screenshot 2024-05-10 204857](https://github.com/emperorpenguincat/CTF-Writeups/assets/110463026/9e0937e6-3e05-4989-afe1-4be4ee095343)

Based on the image above, we can see the characters of the flag format and they are being separated by spaces.

![Screenshot 2024-05-10 204858](https://github.com/emperorpenguincat/CTF-Writeups/assets/110463026/505a26b0-517c-4561-bd03-32d0edc1186c)

Upon figuring out the flag format, we can see the recurring pattern of the spaces from the character `ICTF` and they are being separated by 2^n where n=1 and n is getting increment. It is almost impossible to try to retrieved each of the characters manually so creating a simple python script will be much easier.

Now, we should create a python script where it will read the index of the characters and read characters after the spacing of 2^n, n=1, n++.

## Solve Script (.py)
```python
def get_chars(file):
    with open(file, 'r') as file:
        x = file.read()
        y = ''
        i = 0
        n = 1
        while i < len(x):
            y += x[i]
            i += (2 ** n) + 1 
            n += 1
        return y


file = "build-flag.txt" 
flag = get_chars(file)
print(flag)
```

Using the example script above will allows us to get the flag.

### Flag: ICTF24{h3rE_Y0u_g0}

