# ppcheck
ppcheck is a tool to check your passwords against the pwnedpasswords database ([haveibeenpwned.com](https://haveibeenpwned.com/)).

# How-to

## Install
If you have Python and git installed on your pc. Run this:

```sh
git clone https://github.com/cburik/ppcheck.git
cd ppcheck
pip install .
ppcheck --install
```

Maybe I'll upload this to pypi at some point, so you can pip install it directly.

## Run
TODO: ADD ME!

## Contribute
Honestly, not sure if I'll ever look at pull requests. I have a day job and other hobbies. Feel free to fork and do what you want with it (see [LICENSE](https://github.com/cburik/ppcheck/blob/main/LICENSE)).

# Security
ppcheck sends the first 5 characters of your hashed passwords to the [haveibeenpwned API](https://haveibeenpwned.com/API/v2). If you're not comfortable with that, don't use the tool.

ppcheck saves a hash of your passwords in your home directory, if that doesn't feel good to you, don't use the tool.

Also, see [LICENSE](https://github.com/cburik/ppcheck/blob/main/LICENSE).
