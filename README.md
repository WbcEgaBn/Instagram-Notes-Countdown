
## Run Locally

Clone the project

```bash
  git clone https://github.com/WbcEgaBn/Instagram-Notes-Countdown.git
```

Go to the project directory

```bash
  cd Instagram-Notes_Countdown
```

Install dependencies

```bash
  pip install instagrapi
```

Before running the program, add your username, password, and 2FA code to the variables located at the top of `main.py`. Once successfully logged in, the script will create a `session.json` which holds your information for easier sign in.  

Run the program
```
  python main.py {countdown type} {date dd/mm/yy} {24h time hh:mm} {message}
```
There are two types of countdown:
- `c` countdown
- `ds` days since

Messages can include placeholders for:
- minutes (m)
- hours (d)
- days (d)
- weeks (w)
- months (mo)
To include a placeholder in a countown, simply add the variable as if it were an f-string. Placeholders will be replaced with their actual value at runtime. Below is an example.
```
  python main.py c 11/9/2001 08:46 "{d} days since 9/11"
```
