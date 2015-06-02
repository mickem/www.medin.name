Gallery 3: A modern web gallery?
################################
:date: 2011-10-30 19:58
:author: Michael Medin
:category: Development
:tags: code style, css, gallery, js, photo, php, web
:slug: gallery-3-a-modern-web-gallery
:image: /images/image7.png
:social_image: /images/image7.png

Around 10 years ago I wrote a custom gallery in
`php <http://www.php.net/>`__ it was nice and all but since it is
abandoneware it is starting to get less and less usable. So I decided on
`Gallery 3 <http://gallery.menalto.com/>`__ to replace it and I thought
Id share some observations on it here. So how does `Gallery
3 <http://gallery.menalto.com/>`__ stack up? Was it all the modern “web
2.0 social experience” I expected?

.. PELICAN_END_SUMMARY

What is Gallery 3?
==================

`Gallery 3 <http://gallery.menalto.com/>`__ is a complete rewrite of
Gallery 2 (a popular photo gallery). It seems about a year old but since
its release there have only had two minor updates so it seems not to
actively developed.

Still it is one of the major players in the gallery market which I guess
is quickly being eaten alive by sites provided by the big players such
as `Facebook <http://www.facebook.com>`__,
`Google <http://www.google.com>`__ and
`Microsoft <http://www.microsoft.com>`__. Since I have, by far, to many
photos to store it all in the cloud I tend to look for a custom hosting
where I can tinker a bit with the end result.

The good
========

Well first off lets start with the positive. Gallery 3 has a solid
plugin foundation (not Wordpress galore with thousands of them but then
again there is only one plugin per feature so you don’t need thousands
of them) but still a sizable amount somewhere in-between 150 and 200.
Many of the plugins do what they announce and just work without any
issues. They solve most common problems easily without any custom
fidgeting and it is thus a breeze to get started. The plugins I use are:

-  Custom Menus
   Provides the ability to add custom menus to the UI
-  Exif GPS Data
   Provides google maps integration
-  Facebook Comments
   Adds a box for facebook comments (default it has its own).
-  Photo Annotation
   Tagging framework used by wlp face tagging plugin later on.
-  Rebuild items
   Allows you to easily rebuild thumbnails
-  Rectangle Thumbnails
   Allows you to se the aspect ratio of photos (to make thumbs look
   better)
-  Tag Albums
   Allows you to browse tags (a rather strange approach but works).
-  XMP
   Imports Windows Live Photo Gallery tags (this is where I get my face
   tags).

This is pretty much what I would expect. It is a bit low on the social
side but that is not uncommon and there are some interesting plans in
those areas.

Apart from the solid set of plugins things are working quite well and
everything seems solid enough. So happy story all the way?

Not really, because once I had things running smoothly I was forced to
scratch the surface as I wanted to make the style look like my Wordpress
theme. And here is where it all starts to fall apart once you start
scratching you end up with some rather mind bogglingly strange things.

The bad
=======

.. image:: /images/image8.png
   :width: 300 px

First off why is there no out of the box way to configure the sizes of
thumbs and photos? Why is there no way to configure the layout? Hell why
is there no way to configure pretty much anything?

Perhaps they want themes to provide all this?

That is the direction which Greydragon went. Greydragon is a pretty
solid all inclusive theme which seems to add a workaround for most of
the oddities and adds many of the configuration options I would have
expected out of the box. Unfortunately the theme in it self looks rather
dated something easily solved with some minor customizations and CSS
you’d think: right?

Layout and design aside, it is after all up to taste, there is a lot of
things I would have expected in a modern gallery software which is
missing in gallery 3.

.. image:: /images/image9.png
   :width: 300 px
   :align: right

-  Ajax powered
   Seriously, no ajax at al?
-  Built-in Slideshow
   Coloris is a nice touch but no lightweight built-in slideshow?
-  Next image?
   Why is there no way to click the image to skip to the next (or
   perhaps better yet, some modern version of the popup ajax thumbnail
   browser I had in my gallery see screenshot) ?
-  Zooming thumbnails
   Why cant I get at least some javascript goodness (I quite frankly
   had more ajax in my 10 year old gallery).
-  Interesting widgets
   The included widgets would not have been exiting even 10 years ago.

Another thing which really bothered me was the lack of concept such as
views and trees. I would have liked to switch view to something
less spacious like a list view or tiles view. And it would have been
nice to be able to browse a tree somewhere as it is rather slow clicking
around.

Another point I really missed was alias in my previous gallery an album
could reside in multiple folders making it possible to group things in
more then one way. I guess tags could replace this but browsing tags is
an extension and not out of the box. Also tags are "more photos" then
albums.

The ugly
=================

.. image:: /images/image10.png
   :width: 300 px

As a developer my approach to problem is to fix what I feel is broken.
So the first thing I did was open up vi and start to dabble here and
there trying to make things at least look fresh and modern (in my
humble opinion).

And that’s when it start to become really ugly.

Graydragon has pretty much recreated most of the features which would be
found in a gallery in the theme (probably as the API seems limited).

To make matters worse since there is no standard way to interact between
the various models and views the only way to add support for new
features is to recreate the functionality again and again and again.

A good example of this is the “tag_album” module which in theory could
have piggy backed on the normal thumbnails views just replacing the data
with photos based on tags right?

Wrong! instead they opted to recreate the page-template, album
page-template, and thumbnails-template to facilitate the tag browsing.
This as there seems to be no easy way to create an instance of an
“album” and say: Hey, lets render this guy for me.

This means when I want it to integrate nicely in my theme I ended up
having to add the same hard coded stuff in my hacked Greydragon to make
it look nice.

Perhaps this is due to inexperienced plugin developers, perhaps a badly
designed API? I havent looked at Gallery 3 enough to make up my mind.
But regardless of the reason the end result is leaves a lot to be
desired.

And before I get carried away lets end this by briefly mentioning the
clobbered mix of php, html and what not found in parts of the code.
Hello `ASP <http://en.wikipedia.org/wiki/Active_Server_Pages>`__ and
welcome back to the year 2000!

Conclusion
==========

.. image:: /images/image11.png
   :width: 300 px
   :align: right

Now don’t get me wrong `Gallery 3 <http://gallery.menalto.com/>`__ is a
really nice gallery it is one of the best (and I have tried a myriad of
them) it really works handsomely. But it seems that Gallery 3 (and many
others) are stuck somewhere between 10 years ago and now. Where is all
the modern stuff? Ajax, javascript, hell even some flash would have been
a welcome change.

If you are looking for gallery you cant really go wrong with gallery it
has most features you will require albeit packaged in a pre-web 2.0
edition. But for most people this will not be a problem.

So just don’t expect a lot of cool stuff and make sure you like on of
the included themes (as creating a custom one can be a huge endeavor).
