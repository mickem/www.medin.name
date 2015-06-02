Slides from my OSMC 2012 presentation
#####################################
:date: 2012-10-26 08:05
:author: Michael Medin
:category: Monitoring
:tags: book, conference, demo, nsclient++, OSMC, slides
:slug: slides-from-my-osmc-2012-presentation
:image: /images/SLIDES-NSClient-in-the-new-millenium-001_thumb.png
:social_image: /images/SLIDES-NSClient-in-the-new-millenium-001_thumb.png

On OSMC 2012
I presented NSClient++ 0.4.1 not really presenting new features as such
but more focusing on how to use the new version of NSClient++. In
addition to explain various parts of the new Agent I did some demos
which of course does not show very well in the slides so here I have
presented the demos in a bit more details. I have also, in the slides,
elaborated a bit more to at least give the commands I used. `Slides can
be found
here </images/NSClient++-in-the-new-millenium-WEBFRIENDLY.pptx>`__.

.. PELICAN_END_SUMMARY

Presentation Patterns
---------------------

|image1|\ This year I decided to make the slides a bit mode modern as I
read the `Pressentation Patterns <http://presentationpatterns.com/>`__
book by Neal Ford, Matthew McCullough, and Nate Schutta. It is truly an
impressive book and a must read by anyone who wants to make
presentations.

I describes a series of patterns on how to make good presentations or as
I would say modern presentations.

I was a bit scared as it is a big transition from my old routine so I
did a bit of a hybrid where I tried to minimize the number of bullets
and talk more. I normally essentially have a bullet for each sentence
which I have justified by saying it is my cheat sheet so I wont forget.
So for me taking the plunge to a presentation where I cant read my way
to what I shall say was scary but in the end it worked out so this is
definitely the future.

I also went the way of adding a bling by making nifty(?) animations and
having a lot of advanced hand animated transitions in PowerPoint which
means I almost had to re create my slides to be able to make them
available for paper.

So now I shall return to explain the demos a bit and then allow you to
sit back and read the slides to your hearts content.

Demo 1: Using NSClient++ 0.4.x
------------------------------

The essence of this section and demo was to introduce the command line
interface and convince people the settings generation stuff can really
help them.

So I first had a deck presenting the command line syntax and various
ways to get help. For that section I refer to the slides since it is
explained there.

Then removed the configuration file and showed you I was not cheating:

[sourcecode language="bash" padlinenumbers="true"]
 rm nsclient.ini
 ls nsclient.ini
 # ls: cannot access nsclient.ini: No such file or directory
 [/sourcecode]

Next up I added a module using the command line syntax:

[sourcecode language="bash" padlinenumbers="true"]
 ./nscp settings --activate-module NRPEServer --add-defaults
 [/sourcecode]

Which gives as a configuration that looks like this:

.. code-block:: text

     ; A list of modules.
     [/modules]
    
    .. raw:: html
    
       </p>
    
    ; NRPE server - A simple server that listens for incoming NRPE
      connection and handles them.
     NRPEServer = enabled
    
    ; Section for NRPE (NRPEServer.dll) (check\_nrpe) protocol options.
     [/settings/NRPE/server]
    
    ; COMMAND ARGUMENT PROCESSING - This option determines whether or not
      the we will allow clients to specify arguments to commands that are
      executed.
     allow arguments = false
    
    ; COMMAND ALLOW NASTY META CHARS - This option determines whether or
      not the we will allow clients to specify nasty (as in \|\`&><'"\\[]{})
      characters in arguments.
     allow nasty characters = false
    
    ; PORT NUMBER - Port to use for NRPE.
     port = 5666
    
    ; ... removed large chunk here ...
    
    [/settings/default]
    
    ; ALLOWED CIPHERS - A better value is:
      ALL:!ADH:!LOW:!EXP:!MD5:@STRENGTH
     allowed ciphers = ADH
    
    ; ALLOWED HOSTS - A comaseparated list of allowed hosts. You can use
      netmasks (/ syntax) or \* to create ranges.
     allowed hosts = 127.0.0.1
    
    ; CACHE ALLOWED HOSTS - If hostnames should be cached, improves speed
      and security somewhat but wont allow you to have dynamic IPs for your
      nagios server.
     cache allowed hosts = true
    
    ; SSL CERTIFICATE -
     certificate =
    
    ; TIMEOUT - Timeout when reading packets on incoming sockets. If the
      data has not arrived within this time we will bail out.
     timeout = 30
    
    ; ENABLE SSL ENCRYPTION - This option controls if SSL should be
      enabled.
     use ssl = true
    
    ; VERIFY MODE -
     verify mode = none
    >THE END<

If we now first change the port to 1234 and run the following command to
remove all our default values we end up with the following snippet which
is essentially the keys we have actually configured.

.. code-block:: text

     ; A list of modules.
     [/modules]
    
    .. raw:: html
    
       </p>
    
    ; NRPE server - A simple server that listens for incoming NRPE
      connection and handles them.
     NRPEServer = enabled
    
    ; Section for NRPE (NRPEServer.dll) (check\_nrpe) protocol options.
     [/settings/NRPE/server]
    
    ; PORT NUMBER - Port to use for NRPE.
     port = 1234
    >THE END<

Demo 2: Real-time monitoring
----------------------------

Next up was a crash course in real-time monitoring as well as
introducing several new modules.

-  CheckLogFile
   Listens for file system changes (events, not polling by the way) and
   performs pattern matching and sends events based on patterns
-  SimpleFileWriter
   Writes events to files (a bit like NSCA does when it sends events to
   `Nagios <http://www.nagios.org/>`__ via the command file).
-  NSCAClient
   Sends events to remote NSCA server.

I wont go through the command lines I used to create the configuration
(since that is not really useful apart from show casing it can be done).

.. code-block:: text

     [/modules]
     CheckLogFile = enabled
     SimpleFileWriter = enabled
    
    .. raw:: html
    
       </p>
    
    [/settings/logfile/real-time/checks/sample]
     file = ./test.txt
     filter = column1 like 'hello'
     destination = FILE
     warning = column2 like 'warn'
     critical = column2 like 'crit'
    
    [/settings/logfile/real-time]
     enabled = true
    >THE END<

What we do here is in essence enable the CheckLogFile module and the
SimpleFileWriter module as well as define a file we want to listen for
changes from.

The most interesting part is the …/sample section. Where we have:

-  file
   The file we want to listen to changes from. Here we assume it is a
   tab delimited file if it is we can reconfigure it to have other line
   and column separators. The file should (in some way) be a tabular
   file.
-  filter
   The lines we are interested in should have the first column contain
   “hello”.
-  destination
   To which target we want to send events.
-  warning
   Lines matching this will become a warning (think Nagios).
-  critical
   Lines matching this will become a critical (think Nagios).

To test this I first create the various files and then run tail on the
“output.txt” file (which is the default filename on the SimpleFileWriter
module.

Then I add data to the file using the echo command.

[sourcecode language="bash" padlinenumbers="true"]
 touch test.txt
 touch output.txt
 # In other window:
 tail -f output.txt
 # In yet another window:
 nscp test
 # In yet another window
 echo -e "hello\\tworld"
 echo -e "hello\\tcrit"
 [/sourcecode]

The result is two lines added to the output.txt file one “ok” and one
“critical” like so:

.. code-block:: text

     sample OK ./test.txt: 1 (hello, world, )
     sample CRITICAL ./test.txt: 1 (hello, crit, )
    >THE END<

Next up we extend this by first adding the NSCAClient module and then
changing destination to include ***both** FILE and NSCA* which gives us
the following configuration:

.. code-block:: text

     [/modules]
     CheckLogFile = enabled
     SimpleFileWriter = enabled
     NSCAClient = enabled
    
    .. raw:: html
    
       </p>
    
    [/settings/logfile/real-time/checks/sample]
     file = ./test.txt
     filter = column1 like 'hello'
     destination = FILE,NSCA
     warning = column2 like 'warn'
     critical = column2 like 'crit'
    
    [/settings/logfile/real-time]
     enabled = true
    
    [/settings/NSCA/client/targets/default]
     address = 127.0.0.1
     encryption = xor
     password = secret
    >THE END<

The result from repeating the above commands are now we in addition to
get lines in output.txt also gets events sent to our NSCA server.

Demo 3: Passive real-time checks via NRPE
-----------------------------------------

This module introduced yet another new module called SimpleCache which
stores events for checking via NRPE. This module requires very little
configuration (out of the box) so we merely enabled it but also changed
the destination to send to FILE, NSCA and no also CACHE:

.. code-block:: text

     [/modules]
     CheckLogFile = enabled
     SimpleFileWriter = enabled
     NSCAClient = enabled
     SimpleCache = enabled
    
    .. raw:: html
    
       </p>
    
    [/settings/logfile/real-time/checks/sample]
     file = ./test.txt
     filter = column1 like 'hello'
     destination = FILE,NSCA,CACHE
     warning = column2 like 'warn'
     critical = column2 like 'crit'
    
    [/settings/logfile/real-time]
     enabled = true
    
    [/settings/NSCA/client/targets/default]
     address = 127.0.0.1
     encryption = xor
     password = secret
    >THE END<

What we did now was again run the sample commands to add lines to our
file and NSCA. After which we did an active check from the command line
(in the NSClient++ window).

[sourcecode language="bash"]
 nscp test
 ...
 check_cache index=sample
 OK:./test.txt: 1 (hello, world, )
 [/sourcecode]

And that was pretty much it really… Now all that’s left, if you have not
done so already, is to browse through the
`slides </images/NSClient++-in-the-new-millenium-WEBFRIENDLY.pptx>`__
and hopefully you will then be ready to go with NSClient++ 0.4.1.

Attachments:
------------

.. |SLIDES - NSClient in the new millenium - 001| image:: /images/SLIDES-NSClient-in-the-new-millenium-001_thumb.png
   :target: /images/SLIDES-NSClient-in-the-new-millenium-001.png
.. |image1| image:: http://presentationpatterns.com/images/module/home/book-cover.jpg
