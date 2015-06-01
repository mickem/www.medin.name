Experiences with puppet: "Perfect mail server"
##############################################
:date: 2014-10-02 21:22
:author: mickem
:category: Development
:tags: automation, mail, puppet, review
:slug: experiences-with-puppet-perfect-mail-server
:social_image: /images/thumbnails/400x-/lego-puppet.jpg
:image: /images/thumbnails/400x-/lego-puppet.jpg

I have for a year now been playing around with puppet on and off but have never done anything serious.
Instead I have dabbled a bit here and there in small example projects
so I am **a real puppet beginner**.
Since it was getting time to re-install my mail server I figured it
was an excellent thing to use as a real project.

.. PELICAN_END_SUMMARY

Last time I installed my mail server I did it fully automatic but with shell scripts. This was quite nice and worked pretty well. But due to
**the nature of shell scripting it was a very fragile** solution. I really hoped to **improve on this when I did it with puppet**.
This will not be a puppet tutorial (there are plenty of those around) instead it is some thoughts I had on puppet after using it for "real".

That said the puppet scripts are pretty basic and should hopefully (with the guide side-by-side be pretty easy to understand and use as a
basis for learning.
Again please note that I am a puppet beginner so some choices are probably bad (feel free to point them out) but others in my situation
might benefit from a "not so perfect puppet recipe".

Background
==========

.. image:: /images/thumbnails/200x_/lego-puppet.jpg
   :width: 200 px
   :alt: alternate text
   :align: left

Setting up email servers by hand is a tradition that goes way back for me.
First time I did it was on `slackware <http://www.slackware.com/>` with sendmail and wu-imap
and I barely understood what I was doing. As I got my hands on some sun spark-5 machines next up 
was qmail and courier on Solaris. A few years later it was time again and this time I went with debian,
postfix and cyrus. This combo was used again a while later when I switched to rackspace but extended with 
amavis spamassasin and clamav.  This time I decided to swap out cyrus for dovecot.

So while my installation experience has gone from build **everything
from source** to **fully automated installation with puppet** it
has also been a journey in terms of tools and technologies. And not
only the installation means have become much easier the tools
themselves has also become much simpler to manage. That said I would
say that email server is probably one of the most difficult things to
setup and manage. Why that is I do not know as the email protocols are
among the simplest and stupidest still in use so one would think that
something simple would be available. I mean setting up a full
middleware stack is today something done in a snap.

But I would say that postfix is pretty ok and dovecot was much much
simpler than cyrus (much thanks to sasl "just working").

But this is not a review of email servers instead it is all about
puppet so lets' get to it.

Getting started
===============

The very first thing to solve is installing puppet: This can
(obviously) not be automated with puppet so you end up with some
"boot-strapper" to get it all setup.

In my case I have a **shell script which installs puppet and then
kicks off puppet** with the manifest. In a large origination you
probably want to mitigate this using preloaded images as well as
puppet master to orchestrate things. Since my experience is a bit
different I am a user of infrastructure not a deployer of it **I am
hesitant to the concept of puppet master**. I don't want my
production systems "changed by mistake" because I managed to click the
wrong button.

So I kind of like the idea of puppet stand alone. But perhaps this is
just me?

    So how do you get start with a puppet project?

Well first off you need to know what you want done it is a **good idea
to rough out what you have planned** and start thinking about how to
structure things. In my case I started out from a guide
(https://www.exratione.com/2014/05/a-mailserver-on-ubuntu-1404-postfix-dovecot-mysql/)
so that part was covered.

| When it comes to puppet it is a good idea to start off using multiple
  manifests at least one for config and one for installation tasks but I
  would probably split things up a bit where I to redo this. Having a
  massive 1000 line long script makes it difficult to find things so I
  ended up spending a lot of time looking for things.
|  Having config separately is another must as it is easy to slip in
  some passwords or what not in the git repository by mistake if you
  have configuration in the same file as source code.
|  Speaking of git I haven't mentioned it but **version control is
  probably the best benefit from using puppet**.
|  Using puppet is straight forward and you can start hacking away
  pretty much from the start. One thing I would like to say is to start
  off grouping your tasks into logical "classes" such as "postfix"
  "dovecot" "packages" etc etc.
|  Something which is **really painful in puppet is dependency
  management** and a good structure can greatly help since you can
  order classes as well as things.
|  For instance instead of declaring massive amount of dependencies
  between mail database, mail-admin and mail data I can simply place
  them in separate classes and order the classes.
|  And while this can seem like a solution to all problems unfortunately
  it is not.
|  Once you start ordering everything manually you quickly run into
  "strange loops" since puppet have its own idea about things so one has
  to practice restraint.

Benefits
========

The main benefit of using puppet is repetability and incremental change.
If I reload a machine from scratch I know the outcome and I can trust
the outcome. If I do the same by hand I might miss something and thus
end up with a broken config. With this setup I can at any time reload
the entire machine and have a working email server... Without worrying
about loosing email. This is something wondrous to experience. When I
need to change something I can boot up a new VM and apply the current
config to that and then make changes and test them knowing the config is
exactly right.
If I want to swap hosting provider: dito
Now all this could be achieved using shell scripting or various other
frameworks so puppet is not unique here but puppet is popular and used
by many people so there is plenty of information out there for it and
there are plenty of modules as well. Now I dont use any modules in my
recepie and this is by choice as I wanted "my email server" (Ever heard
of "Nor invented here") but more importantly most third party modules
are a bit to general and you end up writing ten lines of code instead of
one when using them.

Also I wanted to learn puppet not a bunch of strange modules.

Puppet pain
===========

.. image:: http://puppetlabs.com/wp-content/uploads/2010/12/PL_logo_horizontal_RGB_lg.png
   :width: 200 px
   :alt: alternate text
   :align: left

While puppet is nice to automate things there are a lot of snags and issues you will run into.
The prime one is **dependencies** which I already mentioned.
Yet another one is that puppet has very **little support for modifying
files**. I don't know about everyone else but I don't want to use "my
configuration file" I want to modify the default configuration file. If
someone fixes the default configuration file I don't want to miss those
fixes. This is extremely difficult to do in puppet. The closest thing
they have is file_line in the standard library but it is sorely lacking
and usually a pain to work with.


It is **impossible to fetch information from the target system**.
One might think that generating a password and persist that between runs in a file on the target system would be simple?

Not so! It requires creating **functions and some ruby coding** to
do. And while I can understand the rationale behind it (which is that
puppet master executes the "logic") I think it is yet another reason
they should ditch the puppet master concept. Having a "stupid"
framework is pretty silly now puppet is extensible so you can overcome
much of this with some code but again: Why should you have to?

There is **no easy way to say "run this once"** or even "run this if
that" which means that some tasks I have are always executing just
because it is too painful to make a check for them. There are workaround
such as creating random "flag files" and/or use the event subsystem but
it is a pain a flag "do this once" could easily have been provided and
persisted by puppet framework.

The puppet syntax is horrible... It is **difficult to write and even
worse to refactor** someone should really change this into something
usable. Now I spend half the time fixing syntax issues (a missing coma
being the prime example). Another option here would be some sort of
intelligent editor perhaps?

All in all writing the actual script in puppet is pretty simple and
quick.  Instead I would say that the biggest time killer is not the
writing of installation scripts it is debugging and fixing them.

I had the rough version of my scripts after maybe 4-5 hours then I
spent another day and some fixing it. Mainly ordering and dependencies
but also "checks" are difficult to validate. This is not helped by
puppets inability to be helpful.

Debugging puppet is pretty difficult as well as time-consuming as
there is no debugging framework instead you have to rely on
"recreating the image" and running from start with some messages. From
what I know you can't even make a dry run asking puppet to "show" what
it will do which I think would be the first feature I implemented
myself…

Other pains
===========

But it is not only puppet which causes headaches when you do something
like this. One thing which hit me several times was **getting
packages I had not asked for**.

The first time I discovered this I got a failure starting nginx and
after digging around I noticed apache was running! And I don't install
apache but apparently if you install php without a webserver installed
it will install apache for you.

The same was true for a few other packages such as maria-db as well.

Another silly snag is that if you replace content in files it is very
very important that you get the right filename. I managed to mix-up
two similarly named files causing a long stretch of debugging before I
realized that it was the broken file which was the culprit. This was
not really helped much by dovecot being not very helpful as it exited
with some funky error level without any message.

Was it worth it?
================

.. image:: /images/thumbnails/200x_/DO_Logo_Vertical_Blue-75e0d68b.png
   :width: 200 px
   :alt: alternate text
   :align: left

**That's a defined resound yes!**

If I compare the scripts from last time these always work (now when
they work).
It is much easier to fix and edit changes and best of all it is much
much easier to understand.
I would estimate this (which I think is is a fairly complicated
setup) to around 16 hours from scratch (4 of it writing script and 12
debugging them).
It is also vitally important to get version control and virtulizaion
in so you can test that scripts actually WORK!
Once you have the script finished you can use them on any machine but
it would have been impossible to develop without resetting the virtual
machine some 100 times.

 

Next up is adding some IM server as well as a wordpress blog and perhaps
spending some time refactoring the manifest into multiple files.

* The code can be found here: https://github.com/mickem/mail-server-puppet/
* The guide which I based this off can be fund here: https://www.exratione.com/2014/05/a-mailserver-on-ubuntu-1404-postfix-dovecot-mysql/
