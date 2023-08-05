from textwrap import dedent

name = 'Julian Wachholz'
username = 'julianwachholz'

work = ['Quatico', 'Avectris', 'Polynorm', 'Unic']

website = 'https://julianwachholz.dev'
twitter = 'https://twitter.com/julianwachholz'
github = 'https://github.com/julianwachholz'

email = 'julian@wachholz.ch'
pgp = 'https://julianwachholz.dev/julian_wachholz_pub.asc'


def card():
    print(dedent(f'''
    {name} / @{username}

    Work:    {', '.join(work)}
    Website: {website}
    Twitter: {twitter}
    GitHub:  {github}

    Mail:    {email}
             (PGP: {pgp})

    Card:    pipx run jwa
    '''))


if __name__ == '__main__':
    card()
