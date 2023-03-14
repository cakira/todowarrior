# todowarrior
_Synchronize [Toodledo](https://www.toodledo.com/) and
[Taskwarrior](https://taskwarrior.org/)_

## Why?
I've been using [Toodledo](https://www.toodledo.com/) for some years
(decades?) as my task list/to-do list manager, and I like it. I use it on
both my desktop, through the web interface, and on my smartphone, through
a third-party app.

However, as a software/firmware developer, I also like the quickness of
using the terminal to add and list my tasks/to-do list. Consequently,
[Taskwarrior](https://taskwarrior.org/) is quite convenient, and I use it
to record some tasks.

The problem arises when I'm not at my computer and want to see the tasks
in Taskwarrior. I've already tried using the site
[Inthe.AM](https://inthe.am/) for that, but it seems I can't get used to
it.

So, I want to use Toodledo to see my Taskwarrior's tasks.

## Current status
Currently, you can log in Toodledo and print your task list as a prof of
concept. To accomplish this, you will need a Client ID and a Secret.

I already have my own Client ID and Secret, but its not wise to share
secrets on a public website. However, you can obtain yours by registering
a new application on this site:
https://api.toodledo.com/3/account/doc_register.php.

In the registration form, fill the "Website" field with any valid website
of your choice. For the "Redirect URI" field, I suggest using the same as
mine:
`https://github.com/cakira/todowarrior/wiki/Authentication-accepted`

After completing the registration, the Toodledo API page will show your
Client ID and Secret.

Next, execute the following commands:

For the first time only:

  1. Create a virtual environment for Python: `python -m env venv`
  2. Activate the virtual environment: `source venv/bin/activate`
  3. Install the required dependencies: `pip install -r requirements.txt`

Then:

  * Replace the 'todowarrior' and 'api123...' bellow with your Client ID
    and Secret
  * Run the command:
    `TOODLEDO_CLIENT=todowarrior:api1234567890abc python todowarrior/main.py`
  * Follow the instructions provided by the program

After use, deactivate the virtual environment with the command
`deactivate`

This project is in its very beginning. Check the
[issue list](https://github.com/cakira/todowarrior/issues?q=is%3Aissue) to
see the features I am currently working on.

## License
This code is released under the MIT license. For details, check the
[LICENSE](LICENSE) file.

## Related projects
* [toodledo-to-taskwarrior](https://github.com/dennistang/toodledo-to-taskwarrior):
  This project downloads data from Toodledo to Taskwarrior. I'm rather
  interested in the other way around. The project's singular and last
  commit was in 2016.
* [syncwarrior](https://github.com/roylez/syncwarrior): This project does
  not have a README page. Its last commit was in 2013.
