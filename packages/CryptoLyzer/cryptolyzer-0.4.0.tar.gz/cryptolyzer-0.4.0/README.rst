CryptoLyzer
===========

What is it and what is it not?
------------------------------

As the project name CryptoLyzer implies, it is a cryptographic protocol analyzer. The main purpose of creating this
application is the fact, that cryptography protocol analysis differs in many aspect from establishing a connection
using a cryptographic protocol. Analysis is mostly testing where we trigger special and corner cases of the protocol
and we also trying to establish connection with hardly supported, experimental, obsoleted or even deprecated mechanisms
or algorithms which are may or may not supported by the latest or any version of an implementation of the cryptographic
protocol.

As follows, it is neither a comprehensive nor a secure client/server implementation of any cryptographic protocol. On
the one hand analyzer implements only the absolutely necessary parts of the protocol to interact with servers. On the
other it may use completely insecure algorithms and mechanisms. It is not designed and contraindicated to use these
client/server implementations establishing secure connections. If you are searching for proper cryptographic protocol
implementations, there are several existing wrappers and native implementations for Python (eg: M2Crypto, pyOpenSSL,
Paramiko, ...).

Quick start
-----------

CryptoLyzer can be installed directly via pip

.. code-block:: sh

    pip install cryptolyzer
    cryptolyze tls ciphers www.example.com

or via APT on Debian based systems

.. code-block:: sh

    apt update && apt install -y gnupg2 curl
    echo 'deb https://download.opensuse.org/repositories/home:/pfeiffersz:/cryptolyzer:/dev/Debian_10/ /' >/etc/apt/sources.list.d/cryptolyzer.list
    curl -s https://download.opensuse.org/repositories/home:/pfeiffersz:/cryptolyzer:/dev/Debian_10/Release.key | apt-key add -
    apt update && apt install -y python3-pkg-resources python3-cryptoparser python3-cryptolyzer
    cryptolyze tls ciphers www.example.com

or via DNF on Fedora based systems

.. code-block:: sh

    dnf install 'dnf-command(config-manager)'
    dnf config-manager --add-repo https://download.opensuse.org/repositories/home:/pfeiffersz:/cryptolyzer:/dev/Fedora_31/
    rpm --import http://download.opensuse.org/repositories/home:/pfeiffersz:/cryptolyzer:/dev/Fedora_31/repodata/repomd.xml.key
    dnf install python3-urllib3 python3-cryptography cryptoparser cryptolyzer

or can be used via Docker

.. code-block:: sh

    docker run --rm coroner/cryptolyzer tls ciphers www.example.com

.. code-block:: sh

    docker run -ti --rm -p 127.0.0.1:4433:4433 coroner/cryptolyzer ja3 generate 127.0.0.1:4433
    openssl s_client -connect 127.0.0.1:4433

Development environment
^^^^^^^^^^^^^^^^^^^^^^^

If you want to setup a development environment, you are in need of `pipenv <https://docs.pipenv.org/>`__.

.. code-block:: sh

    $ git clone https://gitlab.com/coroner/cryptolyzer
    $ cd cryptolyzer
    $ pipenv install --dev
    $ pipenv run python setup.py develop
    $ pipenv shell
    $ cryptolyze -h

Generic Features
----------------

Protocols
^^^^^^^^^

SSL/TLS
"""""""

* transport layer

  * Secure Socket Layer (SSL)

    * `SSL 2.0 <https://tools.ietf.org/html/draft-hickman-netscape-ssl-00>`_
    * `SSL 3.0 <https://tools.ietf.org/html/rfc6101>`_

  * Transport Layer Security (TLS)

    * `TLS 1.0 <https://tools.ietf.org/html/rfc2246>`_
    * `TLS 1.1 <https://tools.ietf.org/html/rfc4346>`_
    * `TLS 1.2 <https://tools.ietf.org/html/rfc5246>`_

* application layer

  * `opportunistic TLS <https://en.wikipedia.org/wiki/Opportunistic_TLS>`_ (STARTTLS)

    * `FTP <https://en.wikipedia.org/wiki/File_Transfer_Protocol>`_
    * `IMAP <https://en.wikipedia.org/wiki/Internet_Message_Access_Protocol>`_
    * `LDAP <https://en.wikipedia.org/wiki/Lightweight_Directory_Access_Protocol>`_
    * `POP3 <https://en.wikipedia.org/wiki/Post_Office_Protocol>`_
    * `RDP <https://en.wikipedia.org/wiki/Remote_Desktop_Protocol>`_
    * `SMTP <https://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol>`_
    * `XMPP (Jabber) <https://en.wikipedia.org/wiki/XMPP>`_

Analyzers
^^^^^^^^^

.. table:: Supported analyzers by cryptographic protocol versions

    +------------------------------------------+---------------------------------------+
    ||                                         | **Protocos**                          |
    ||                                         +---------------+-----------------------+
    ||                                         | *SSL*         | *TLS*                 |
    ||                                         +-------+-------+-------+-------+-------+
    || **Analyzers**                           |  2.0  |  3.0  |  1.0  |  1.1  |  1.2  |
    +==========================================+=======+=======+=======+=======+=======+
    | Cipher Suites (``ciphers``)              |   ✓   |   ✓   |   ✓   |   ✓   |   ✓   |
    +------------------------------------------+-------+-------+-------+-------+-------+
    | X.509 Public Keys (``pubkeys``)          |   ✓   |   ✓   |   ✓   |   ✓   |   ✓   |
    +------------------------------------------+-------+-------+-------+-------+-------+
    | X.509 Public Key Request (``pubkeyreq``) |  n/a  |   ✓   |   ✓   |   ✓   |   ✓   |
    +------------------------------------------+-------+-------+-------+-------+-------+
    | Elliptic Curves (``curves``)             |  n/a  |  n/a  |   ✓   |   ✓   |   ✓   |
    +------------------------------------------+-------+-------+-------+-------+-------+
    | Diffie-Hellman parameters (``dhparams``) |  n/a  |  n/a  |   ✓   |   ✓   |   ✓   |
    +------------------------------------------+-------+-------+-------+-------+-------+
    | Signature Algorithms (``sigalgos``)      |  n/a  |  n/a  |  n/a  |   ✓   |   ✓   |
    +------------------------------------------+-------+-------+-------+-------+-------+

Python implementation
^^^^^^^^^^^^^^^^^^^^^

* CPython (2.7, >=3.3)
* PyPy (2.7, 3.5)

Operating systems
^^^^^^^^^^^^^^^^^

* Linux
* macOS
* Windows

Protocol Specific Features
--------------------------

Transport Layer Security (TLS)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Only features that cannot be or difficultly implemented by the most popular SSL/TLS implementations (eg:
`GnuTls <https://www.gnutls.org/>`_, `LibreSSL <https://www.libressl.org/>`_, `OpenSSL <https://www.openssl.org/>`_,
`wolfSSL <https://www.wolfssl.com/>`_, ...) are listed.

Cipher Suites
"""""""""""""

#. supports each cipher suites discussed on `ciphersuite.info <https://ciphersuite.info>`_
#. supports `GOST <https://en.wikipedia.org/wiki/GOST>`_ (national standards of the Russian Federation and CIS
   countries) cipher suites

Fingerprinting
""""""""""""""

#. generates `JA3 tag <https://engineering.salesforce.com/tls-fingerprinting-with-ja3-and-ja3s-247362855967>`_ of any
   connecting TLS client independently from its type (graphical/cli, browser/email client/...)
#. decodes existing `JA3 tags <https://engineering.salesforce.com/tls-fingerprinting-with-ja3-and-ja3s-247362855967>`_
   by showing human-readable format of the TLS parameters represented by the tag

Social Media
------------

* `Twitter <https://twitter.com/CryptoLyzer>`_
* `Facebook <https://www.facebook.com/cryptolyzer>`_

Credits
-------

Icons made by `Freepik <https://www.flaticon.com/authors/freepik>`_ from `Flaticon <https://www.flaticon.com/>`_.

License
-------

The code is available under the terms of Mozilla Public License Version 2.0 (MPL 2.0).

A non-comprehensive, but straightforward description of MPL 2 can be found at `Choose an open source
license <https://choosealicense.com/licenses#mpl-2.0>`__ website.
