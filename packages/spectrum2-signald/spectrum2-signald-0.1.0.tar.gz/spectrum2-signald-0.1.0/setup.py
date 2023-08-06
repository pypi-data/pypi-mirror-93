# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spectrum2_signald']

package_data = \
{'': ['*']}

install_requires = \
['pysignald-async>=0.1.0,<0.2.0', 'pyspectrum2>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'spectrum2-signald',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Signald spectrum2 backend\n\n## What is this?\n\nThis is a way to connect to the [signal](https://www.signal.org/) instant\nmessaging network using other messaging networks such as\n[XMPP](https://www.xmpp.org/).\n\nIt can act as a linked device to your main signal device (your phone), or\nas a standalone replacement for official signal clients. The latter is my\npersonal use case so this is what is most tested.\n\nAlternatively, you might be interested in the signald python interface in\n`spectrum2_signald/signald.py`.\n\n## What do I need?\n\n- [signald](https://gitlab.com/signald/signald)\n- [spectrum2](https://spectrum.im/)\n- [pyspectrum2](https://pypi.org/project/pyspectrum2/)\n- qrencode to link an existing signal device\n\n### Could you be a little more specific?\n\n#### Python stuff\n\nSomeday I might package this more properly but for now, just clone this\nrepository, and use either `pip install --user` or a virtualenv of some\nsort to install pyspectrum2.\n\n#### XMPP Server\n\nConfigure a specific component in your XMPP server, for instance with\nprosody, add something like this to `/etc/prosody/prosody.cfg.lua`:\n\n```lua\nmodules_enabled = {\n  -- [...]\n  "privilege";\n}\n\n -- [...]\n\nComponent "signal.example.com"\n    component_secret = "something-random"\n    modules_enabled = {"privilege"}\n\n-- [...]\n\nVirtualHost "example.com"\n    privileged_entities = {\n        ["signal.example.com"] = {\n            roster = "both";\n            message = "outgoing";\n        }\n    }\n\n```\n\nThe privilege thing is not mandatory, but will allow carbons for messages\nsent from official signal clients to be sent to XMPP clients.\n\nFrom my experience, reloading configuration and components while prosody\nis running is not enough to get the privilege thing working, so you might\nneed to `systemctl restart prosody` at this point.\n\n#### Signald\n\nHave the `/var/lib/signald/attachments` directory readable for the user\nthat runs spectrum2 if you want attachments to work.\n\n#### Spectrum2\n\nModify the `signal.cfg` file to match the component secret, path to the\nright python interpreter and __main__.py script, and http upload stuff for\nattachments.\nCopy it to `/etc/spectrum2/transports`.\nYou should now be able to use `spectrum2_manager signal.example.com start`.\n\n#### XMPP client\n\n- Discover services on your server.\n- Subscribe to the gateway signal.example.com, using your phone number as a\n  username.\n- If you already used signald with this phone number, your roster should\n  populate with your signal contacts and you should be able to send\n  receive/contacts.\n- If you did not configure signald for this phone number, you should receive\n  a message from a signal@signal.example.com prompting you with instructions\n  to either register your phone number or to link signald to the official\n  signal app.\n- To see which groups are available send a message with "groups" as body to\n  this user to get a link of XMPP URIs to join your groups.\n\n## How secure is this?\n\nNot as secure as using the official signal client, especially since this is\npre-alpha software. You can read more about it [in this gitlab issue](https://gitlab.com/signald/signald/-/issues/101).\nAs a rule of thumb, if your main concern is privacy and security, you should\nuse the official signal clients.\nHowever, if you are running your own XMPP server, this shouldn\'t be a lot\nless "secure" than anything else on your XMPP server.\n\n### Multi-user considerations\n\nRight now, it is not safe at all to allow public registrations, because of [spectrum](https://github.com/SpectrumIM/spectrum2/issues/234) and [signald](https://gitlab.com/signald/signald/-/issues/119).\nThis should be improved some day. Right now, my advice is to only use it on your own server,\nand disable public registrations as soon as you register your user.\n\n## What works?\n\n- Send/receive private messages.\n- Join and send/receive messages from groups.\n- Attachments if the the script has access to a dir that is publicly available\n  via http.\n- Carbons for self messages sent from official signal clients.\n\n## What doesn\'t work?\n\n- It crashes quite often, especially [this issue](https://gitlab.com/signald/signald/-/issues/111)\n  seems to be really annoying.\n- Groups need to be manually joined via the XMPP client.\n- Unsubscribing via XMPP does not delete the signald user.\n\n## What is the license?\n\nSomething free (libre), yet to be determined. I am no expert in this stuff.\n',
    'author': 'Nicolas Cedilnik',
    'author_email': 'nicoco@nicoco.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
