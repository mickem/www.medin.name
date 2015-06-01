Book review: Developing Web Applications with Oracle ADF Essentials
###################################################################
:date: 2013-11-18 23:47
:author: mickem
:category: Development
:tags: Adf, Java, oracle, Packt, review
:slug: book-review-developing-web-applications-with-oracle-adf-essentials
:image: /images/0686EN_cov.png
:social_image: /images/0686EN_cov.png

Packt sent me an e-copy of “Developing Web Applications with Oracle ADF
Essentials” by `Sten E. Vesterli <https://twitter.com/stenvesterli>`__
asking me to review it. The book is a pretty good and probably rather
unique book which covers the **Open Source version of the**
`**Oracle** <http://oracle.com/>`__ ** ** `**ADF
library** <http://www.oracle.com/technetwork/developer-tools/adf/overview/index.html>`__.
This does not mean the book is only for “open source” ADF since
everything you can do in this book you can also do with regular ADF
instead it means it covers using Adf with non-standard technology such
as GlassFish, Mysql and so on and so forth.

.. PELICAN_END_SUMMARY

First off beware this is technically a sponsored review
as I did not pay for the book. But fear not I will remain objective
despite this fact.

All in all I liked the book but it is not without its flaws. The chief
flaw is actually not the author's fault but the fact that the Open
Source version of ADF seems very immature and after having read the book
I am left wondering why anyone would even bother with it?

To Adf or Not to Adf?
=====================

I think the previous section requires some explanation. ADF for me is a
nice framework for rapid prototyping of administrative user interfaces.
What I mean by this is that you can (starting from a database model)
prototype a fully working application in minutes. This is a really
amazing feat and Oracle has really succeeded in this regard.

Now to the problem. The book is around 200 pages long. The first 100
pages covers creating the first working application. Then another 50
with some additional workarounds for the various technologies used.

Yes, the first 150 pages is essentially fighting with Adf Essentials and
various issues from using non standard technology.

Now this is not quite as bad as it sounds because Sten does a superb job
of explaining why it does not work and how to fix it. So all in all you
learn quite a lot about ADF from this experience.

Instead it makes me wonder why Adf Essential even exists. As I said the
normal Adf tutorial is maybe some 10-15 minutes of clicking. But while
reading his book I often get the urge to pickup my Ruby on Rails book
and see if it would not be faster learn to learn Ruby first than
struggling with this?

I mean when he wrote: ***“…Version 4.0 of GlassFish has been released
but you cannot run ADF Essential on it…”*** I cant but help to wonder
why he did not drop the “Essential” part from the title and instead
produce a nice Adf book.

The book
========

So if we excuse the fact that Adf Essentials seem to be an early beta at
the moment and focus on the book. It is as I said pretty good. Some
analogies really made me go: What? But that could be me lacking his
background and apart from this the Language is very good and you really
can tell that Sten knows his way around Adf and is good at explaining.

The book is written so an absolute beginner to Java would understand
most of it (which is also the way Oracle often pitches Adf). And he even
managed to explain the View vs Entity which I have always found a bit
odd before.

A few things I really disliked with the book are that he gives a default
password to use. And while he does mention default passwords should not
be used I find it bad to encourage it by printing a sample password. A
better way would have been to teach the reader how to reset the password
instead.

Another thing is that he prints CSS rules directly in his code which is
another no-no in my book and should not be encouraged. And while I
understand that you have to do things like this to make things simple
for the reader I personally think it is better to skip sections
requiring it since I know most newbies will copy the code as-is not
understanding that it is bad practice.

On the other had there are also many thing I really enjoyed such as
explaining that applications should be split up (and how to do it) as
well as introduce version control systems, logging frameworks, code
templates as well as build scripts and many other similar things. And
these are important things which many books leave out.

What's in the book
==================

The book is around 200 pages (I read the ePub version) and spans eight
chapters. It is designed as a tutorial which means you probably want to
read it from cover to cover. I guess some chapters towards the end could
be considered self contained.

#. **My First ADF Essentials Application**
   Installing and configuring the tools
#. **Creating Business Services**
   Walkthrough of ADF BC
#. **Creating Task Flows and Pages**
   Walkthrough of ADF Web project
#. **Adding Business Logic**
   Extending the application with Logic
#. **Building Enterprise Applications**
   Managing code, libraries and such
#. **Debugging ADF Applications**
   Pretty much what the title says
#. **Securing an ADF Essentials Application**
   How to use `Apache shiro <http://shiro.apache.org/>`__ to secure the application.
#. **Build and Deploy**
   Build scripts and such

The verdict
===========

This is a **good book** for **Java beginners** wanting to learn **Adf
Essentials** (and probably Adf as well) the **main problem** I have with
the book is the Essentials part. **Adf Essentials** does **not** strike
me as a **production read** technology instead I get the feeling it is
something Oracle released as an after thought to be able to say “Open
Source” on a power point presentation somewhere.

That said the book does a good job explaining Adf (and how to maneuver
the various issues and pitfalls of using Adf with non Oracle
technologies).

And most importantly of all it is written by someone who actually knows
what he is talking about and has something to say!

**So all in all I can recommend the book to beginners to Java who want
to learn about Adf.**

For more details:

-  `Book
   Page <http://www.packtpub.com/developing-web-applications-with-oracle-adf-essentials/book>`__
-  `Sten’sTwitter <https://twitter.com/stenvesterli>`__
-  `Svens Blog <http://www.vesterli.com/>`__
