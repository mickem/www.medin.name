Securing NRPE with certificate based authentication
###################################################
:date: 2012-12-02 23:13
:author: Michael Medin
:category: Monitoring
:tags: icinga, nagios, nsclient++, security, ssl
:slug: securing-nrpe-with-certificate-based-authentication
:image: /images/image.png
:social_image: /images/image.png

NRPE is a common easy to use option for monitoring remote
machines from `Nagios <http://www.nagios.org/>`__ or
`Icinga <https://www.icinga.org/>`__. *Unfortunately NRPE, with **out of
the box setup,** is **not** what I would consider **secure.***

This tutorial looks at how you can secure your NRPE traffic by using
`NSClient++ <http://nsclient.org/>`__ both as a client and server (yes
it runs on Linux as well) in conjunction with SSL certificates to
provide certificate based authentication.

.. PELICAN_END_SUMMARY

Target design
=============

We are going to start by looking at what we want to achieve. What we
want is:

-  Encrypted SSL data transfer
-  Secure client authentication
-  Secure server authentication

The solution I present here will use SSL and certificate based
authentication to create a secure environment where we only allow
trusted clients to communication with trusted servers. Unfortunately the
solution requires a lot of infrastructure (configuration and
administration) so it is probably not for everyone.

We will be using NSClient++ on both *CLIENT* and *SERVER* and connect
the two over a secured SSL socket whilst using a central CA for
authentication both ways.

This means your client can be sure it is a trusted server it is
connecting to as well as the server can be assured it is a trusted
client connecting.

|image|

I am by no means a security expert but from what I can tell this is a
fairly secure model so hopefully it shall be safe enough for our
monitoring needs (it is surely more secure the the default method).

So how do we achieve this then?

Well, lets start by adding certificates to the NSClient server to make
sure the connection is encrypted.

Using certificates with NSClient++
==================================

|image|

The first goal on the agenda is to use certificates with NSClient++. In
this case we are not looking for authentication instead only encryption
so this will only help keep the data traffic hidden from prying eyes. to
do this we first need to create a certificate.

I tend to use `openssl <http://www.openssl.org>`__ for certificates not
because it is good but because it works. I tend to consider openssl to
be far to complicated for everyday use and always end up scripting
things around it to make it easier to work with.

To create a certificate with openssl we can use the bundles CA.pl perl
script. In my case I start from scratch so I need to generate the CA
using the following command (it will ask for CA password as well as some
meta information):

***/usr/lib/ssl/misc/CA.pl -newca***

Then we can request the first certificate and sign it:

***/usr/lib/ssl/misc/CA.pl -newreq /usr/lib/ssl/misc/CA.pl -sign***

All open ssl commands will ask for meta information as well as
passphrases and passwords and the only thing which is important is the
CA field (or common name) during the request. It has to match the
hostname of the server ideally (if you want to enable host name
validation) but lessens security down the line as you can steal
certificates from another node as well as various man in the middle
attacks. After running this we have three files in the folder:

.. code-block:: text

   -rwxrwxrwx 1 root root 3220 Dec  2 18:48 newcert.pem
   -rwxrwxrwx 1 root root  963 Dec  2 18:47 newkey.pem
   -rwxrwxrwx 1 root root  668 Dec  2 18:47 newreq.pem

The request (newreq) is not really useful anymore instead it is the
certificate (newcert) and key (newkey) we are interested in. Before we
copy these files over to our NSClient++ server we shall remove the
passphrase from the key (unless you want to manually type a password
whenever you start NSClient++).

.. code-block:: text

   openssl rsa -in newkey.pem -out newkey_open.pem

Then we rename and place these files under the under the security folder
of the NSClient++ installation.

Next up we will configure the *SERVER* NSClient++ to use this
certificate. Which is pretty straight forward first we enable the module
(loading in all default values) then we set the relevant keys and
finally we remove all defaults to keep the configuration clean and
relevant.

.. code-block:: text

     del nsclient.ini
     nscp settings --activate-module NRPEServer --add-defaults
     nscp settings --path /settings/default --key "allowed ciphers" --set
    "ALL:!ADH:!LOW:!EXP:!MD5:@STRENGTH"
     nscp settings --path /settings/default --key "certificate" --set
    security/server.pem
     nscp settings --path /settings/default --key "certificate key" --set
    security/server\_key.pem
     nscp settings --generate --remove-defaults
    >THE END<

-  First we enabled strong ciphers and disable the unsecure ADH option
   by settings the ***allowed ciphers*** list to
   ***"ALL:!ADH:!LOW:!EXP:!MD5:@STRENGTH"***
-  Then we set the ***certificate*** to ***security/server.pem***.
-  Finally we set the ***certificate key*** to
   ***security/server\_key.pem***.

To test this we start NSClient++ in test mode and open up a new console
where we will simulate a remote NRPE client connection.

.. code-block:: text

   nscp nrpe -- -H 127.0.0.1
   I (0,4,1,66 2012-11-18) seem to be doing fine...

Here we don’t really see much in regards to our secure option but
hopefully it is a bit less easy to eavesdrop on this connection since we
have a proper certificate and not using the hard-coded DH key.

Next up we want to sprinkle some trust by using the CA to validate the
certificates.

Enabling trust
==============

|image|

The simplest way to enable trust when using SSL is to use a central CA
when issuing the certificates. Since we already have the certificates in
place for the *SERVER* all we need to do is copy the CA certificate over
to the *CLIENT* and ask it to validate the remote server. The first
thing we need to do is to copy over the cacert.pem file from the demoCA
folder to the security folder of the *CLIENT* NSClient++ installation (I
use the same for the *SERVER* for simplicity). Also note that I rename
it to ca.pem for brevity. Next we start nscp in client mode again adding
a set of options:

.. code-block:: text

     nscp nrpe -H 127.0.0.1 --ca security/ca.pem --verify peer-cert
    --allowed-ciphers ALL:!ADH:!LOW:!EXP:!MD5:@STRENGTH
     I (0,4,2,1 2012-08-08) seem to be doing fine...
    >THE END<

The extra options are (in order):

-  **--ca** security/ca.pem
   The certificate authority to use (in our case the demoCA
   certificate)
-  **--verify** peer-cert
   What we want to verify (in this case that the peer is valid and has
   a valid certificate)
-  **--allowed-ciphers** ALL:!ADH:!LOW:!EXP:!MD5:@STRENGTH
   As before for legacy reasons the default cipher list includes only
   unsecure ciphers so we need to change that.

If we quickly reconfigure NSClient++ without the certificate and retry
we get the following result (which is not a very good error message,
since it only says something is wrong):

.. code-block:: text

     nscp nrpe -H 127.0.0.1 --ca security/ca.pem --verify peer-cert
    --allowed-ciphers ALL:!ADH:!LOW:!EXP:!MD5:@STRENGTH
     error nrpe SSL handshake failed: short read
     D:\\source\\nscp\\trunk\\include\\socket/client.hpp:194
     error nrpe Error: Failed to connect to: 127.0.0.1:5666 :short read
     ..\\..\\..\\..\\trunk\\modules\\NRPEClient\\NRPEClient.cpp:353
     Error: Failed to connect to: 127.0.0.1:5666 :short read
    >THE END<

Better trust?
=============

Now it might not make too much sense for us to validate that the server
we are calling has a valid certificate a better option would be to have
the server validating incoming connections. We presumably know who we
are calling so we can most likely trust the remote node after all. This
is easily achieved but requires a bit more configuration as well as a
bit more administration. This as we now are required to provide
certificates for BOTH the *CLIENT* and the *SERVER*. so we need an extra
set of certificates and we need to configure NSClient++ to use them.

|image|

So first off we need to go and generate some more certificates using the
CA.pl script again.

This time we copy the certificates over to the *CLIENT* side and rename
them to client.pem and client_key.pem. For details refer to the section
above also don’t forget to remove the passphrase from the key file.

Now we need to re-configure our *SERVER* to instead validate
certificates which we as before do using the command line syntax. And as
before we first add defaults to figure out what the key is inside the
NSClient++ configuration file.

.. code-block:: text

     nscp settings --generate --add-defaults
     nscp settings --path /settings/default --key ca --set security/ca.pem
     nscp settings --path /settings/default --key "verify mode" --set
    "verify peer"
     nscp settings --generate --remove-defaults
    >THE END<

Then we restart NSClient++ *SERVER* and retry the connection command we
issued before.

.. code-block:: text

     nscp nrpe -H 127.0.0.1 --ca security/ca.pem --verify peer-cert
    --allowed-ciphers ALL:!ADH
     :!LOW:!EXP:!MD5:@STRENGTH
     error nrpe SSL handshake failed: short read
     D:\\source\\nscp\\trunk\\include\\socket/client.hpp:194
     error nrpe Error: Failed to connect to: 127.0.0.1:5666 :short read
     ..\\..\\..\\..\\trunk\\modules\\NRPEClient\\NRPEClient.cpp:353
     Error: Failed to connect to: 127.0.0.1:5666 :short read
    >THE END<

This is actually expected as we have not loaded the client certificate.
Also since we are not interested (yet) in validating the client and thus
use the CA certificate ca.pem file we remove all options we had relating
to the CA before. Instead we add new ones for the *CLIENT* certificate
as well as key.

.. code-block:: text

     nscp nrpe -H 127.0.0.1 --allowed-ciphers
    ALL:!ADH:!LOW:!EXP:!MD5:@STRENGTH --certificate security/client.pem
    --certificate-key security/client\_key.pem
     I (0,4,2,1 2012-08-08) seem to be doing fine...
    >THE END<

Going over the options we have:

-  --allowed-ciphers
   We still need to enable to strong chipers.
-  --certificate
   Our client certificate
-  --certificate-key
   The key for our certificate.

Complete trust
==============

The last thing we are going to do is enable trust both ways. Client will
trust server and server will trust client. Since we have already had
trust both ways (just not at once) we only need to change the command to
include the verification we had before again:

|image|

.. code-block:: text

     nscp nrpe -H 127.0.0.1 --ca security/ca.pem --verify peer-cert
    --allowed-ciphers ALL:!ADH:!LOW:!EXP:!MD5:@STRENGTH --certificate
    security/client.pem --certificate-key security/client\_key.pem
     I (0,4,2,1 2012-08-08) seem to be doing fine...
    >THE END<

As you can see we end up with a rather long command we can get around
this by using some configuration but I will leave that for another day
especially since the command will be templated in Nagios/Icinga anyway
so the long command line wont be a problem. Lastly lets go over all the
command line options one last time.

-  **--ca** security/ca.pem
   Set the CA certificate to use when validating remote peers.
-  **--verify** peer-cert
   Enable verification of peer certificates.
-  **--allowed-ciphers** ALL:!ADH:!LOW:!EXP:!MD5:@STRENGTH
   Enabled strong ciphers (and disable weak ones)
-  **--certificate** security/client.pem
   Set the client certificate
-  **--certificate-key** security/client_key.pem
   Set the client certificate key file.

And the configuration as well:

.. code-block:: text

     [/modules]
     NRPEServer = enabled
    
    .. raw:: html
    
       </p>
    
    [/settings/default]
     allowed ciphers = ALL:!ADH:!LOW:!EXP:!MD5:@STRENGTH
     ca=security/ca.pem
     certificate = security/server.pem
     certificate key = security/server\_key.pem
     verify mode = peer-cert
    >THE END<

-  **ca** = security/ca.pem
   Set the CA certificate to use when validating remote peers.
-  **verify mode** = peer-cert
   Enable verification of peer certificates.
-  **allowed ciphers** = ALL:!ADH:!LOW:!EXP:!MD5:@STRENGTH
   Enabled strong ciphers (and disable weak ones)
-  **certificate** = security/server.pem
   Set the server certificate
-  **certificate key** security/server_key.pem
   Set the server certificate key file.

Conclusion
==========

So enabling security over NRPE is not that difficult using NSClient++.
If it can be done using plain vanilla NRPE I am unsure of it is possible
you can configure this using environment variables but I have never
tried I am skeptical though.

The biggest drawback to using certificates for security is that you
almost have to have infrastructure to manage it as manually generating
and copying and configuring certificates is a lot of work. If you push
your configuration out it could maybe be done using some publishing tool
but my guess is you will need to manage this on your own.

I have some plans to provide a way to do this centrally and
automatically using some NSClient++ scripting but haven't had time to do
so yet. If you are interested in coming with feedback and helping out
testing/developing such a solution please don’t hesitate to ask.

As always, feedback greatly appreciated (in all its forms)!

**UPDATE:** As Beaker pointed out the second command is **-newreq** not
**-newca** again :)

.. |image| image:: /images/image_thumb.png
   :target: /images/image.png
.. |image2| image:: /images/image_thumb1.png
   :target: /images/image1.png
.. |image3| image:: /images/image_thumb2.png
   :target: /images/image2.png
.. |image4| image:: /images/image_thumb3.png
   :target: /images/image3.png
.. |image5| image:: /images/image_thumb4.png
   :target: /images/image4.png
.. |image6| image:: /images/image_thumb5.png
   :target: /images/image5.png
