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
Extract passwords from a csv file:

``sh
ppcheck --extract path/to/passwords.csv
``

At this moment in time it expects, and can only work with csv's with 4 columns containing account_name, url, username, password, in that order. So export the csv from your password manager, put the columns in that order. Extract it with ppcheck and don't forget to delete the csv from your device again. 
Extracting it will save hashes of your passwords (not the passwords themselves!) to your home directory. 

``sh
ppcheck --check
``

Will checks if any of the hashes of the extracted passwords are in the haveibeenpwned database. 

``sh
ppcheck --uninstall
``

Removes all local files. But doesn't remove the python package itself. Run `pip uninstall ppcheck` if you want to do that.

## Contribute
Honestly, not sure if I'll ever look at pull requests. I have a day job and other hobbies. Feel free to fork and do what you want with it (see [LICENSE](https://github.com/cburik/ppcheck/blob/main/LICENSE)).

# Security
There's not that much code, so you can check for yourself how it works. 

ppcheck saves a hash of your passwords in your home directory, if that doesn't feel good to you, don't use the tool.

ppcheck sends the first 5 characters of your hashed passwords to the [haveibeenpwned API](https://haveibeenpwned.com/API/v2). If you're not comfortable with that, don't use the tool.

Also, see [LICENSE](https://github.com/cburik/ppcheck/blob/main/LICENSE).
