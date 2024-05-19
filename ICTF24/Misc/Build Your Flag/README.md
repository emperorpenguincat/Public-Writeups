# Challenge: Build Your Flag

### Difficulty: Easy
## Category: Misc
### Description: Timmy is a very lazy person. Instead of hiding the flag as instructed, he insisted that we construct it ourselves using this text file. Don't be like Timmy.

The challenge provided a large text file and contains random characters that might seems confusing. 

![329581973-e6e97603-5b24-45b6-acb3-4dfb07c7d809](https://github.com/emperorpenguincat/Public-Writeups/assets/110463026/4750ef39-b54b-459a-8c08-ab675efc3296)

Firstly, we need to understand that the flag format is important which is `ICTF24{flag}`.Now we need to oberserve the text file and seek for the flag format.

![329583068-9e0937e6-3e05-4989-afe1-4be4ee095343](https://github.com/emperorpenguincat/Public-Writeups/assets/110463026/3a16ed6f-3492-411e-af6a-817e494ea228)

Based on the image above, we can see the characters of the flag format and they are being separated by spaces.

![329583121-505a26b0-517c-4561-bd03-32d0edc1186c](https://github.com/emperorpenguincat/Public-Writeups/assets/110463026/ae64a272-16a4-4163-8bdf-213434e91476)

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

