Thumbnail 1000:s of photos on a Synology NAS (in hours not months)
##################################################################
:date: 2012-04-22 08:00
:author: Michael Medin
:category: Personal
:tags: gallery, photo, synology
:slug: thumbnail-1000s-of-photos-on-a-synology-nas-in-hours-not-months
:image: /images/synology_ds212.jpg
:social_image: /images/synology_ds212.jpg

I moved all my photos over to my Synology NAS (which
I really enjoy) just to discover that it would take months to index all
photos. So I started to look for options and while most people managed
to increase the speed a bit by reducing the quality of the thumbnails I
figured why not utilize some of the CPU power I have at home?

So I ended up using my Linux box to do the thumbnailing for me instead
which reduced the time to thumbnail 30.000 photos down to hours.

.. PELICAN_END_SUMMARY

The process
===========

The process is simple and straight forward and requires NFS as well as
`ImageMagic <http://www.imagemagick.org>`__ on the Linux box I also
disabled the indexer on the Synology DS (using the pause feature) but I
don’t think this is strictly required.

**The first step is to mount the photo share:**

[sourcecode language="bash" padlinenumbers="true"]
 mkdir /mnt/photo
 sudo mount DS_IP:/volume1/photo /mnt/photo/
 [/sourcecode]

**Second step is to create a script to generate thumbnails.**

This will for all \*.jog create the required thumbnails for you if you
have other files you might need to tweak this.

.. code-block:: bash

   #!/bin/bash
   pushd "$1"
   shopt -s nocaseglob
   if [ ! -d @eaDir ] ; then mkdir @eaDir ; fi
   for f in \*.jpg ; do
   if [ "$f" == "\*.jpg" ] ; then break ; fi
   echo "$1 - $f..."
   if [ ! -d @eaDir/$f ] ; then mkdir @eaDir/$f ; fi
   if [ ! -f @eaDir/$f/SYNOPHOTO:THUMB_XL.jpg ] ; then convert $f -resize 1280x1280\\> -quality 90 -unsharp 0.5x0.5+1.25+0.0 @eaDir/$f/SYNOPHOTO:THUMB_XL.jpg ; fi
   if [ ! -f @eaDir/$f/SYNOPHOTO:THUMB_L.jpg ] ; then convert @eaDir/$f/SYNOPHOTO:THUMB_XL.jpg -resize 800x800\\> -quality 90 -unsharp 0.5x0.5+1.25+0.0 @eaDir/$f/SYNOPHOTO:THUMB_L.jpg ; fi
   if [ ! -f @eaDir/$f/SYNOPHOTO:THUMB_M.jpg ] ; then convert @eaDir/$f/SYNOPHOTO:THUMB_L.jpg -resize 320x320\\> -quality 90 -unsharp 0.5x0.5+1.25+0.0 @eaDir/$f/SYNOPHOTO:THUMB_M.jpg ; fi
   if [ ! -f @eaDir/$f/SYNOPHOTO:THUMB_S.jpg ] ; then convert @eaDir/$f/SYNOPHOTO:THUMB_M.jpg -resize 120x120\\> -quality 90 -unsharp 0.5x0.5+1.25+0.0 @eaDir/$f/SYNOPHOTO:THUMB_S.jpg ; fi
   if [ ! -f @eaDir/$f/SYNOPHOTO:THUMB_B.jpg ] ; then convert @eaDir/$f/SYNOPHOTO:THUMB_L.jpg -resize 640x640\\> -quality 90 -unsharp 0.5x0.5+1.25+0.0 @eaDir/$f/SYNOPHOTO:THUMB_B.jpg ; fi
   done
   popd

**Last step is to run the script in the folder you want to thumbnail**
(or the root if you want to thumbnail it all):

Replace ~/tn.sh with the location of the script you created before.

.. code-block:: bash

   find . -type d -name @eaDir -prune -o ! -name @eaDir -type d -exec ~/tn.sh {} \\;

A big warning
-------------

Now this may void you warranty break your NAS and generally end the
world as you know it. I tried it on my NAS and it works but there are no
guarantees. But I hope that the people at Synology will listen to this
and create a sanctioned way to remotely create thumbnails as it is much
better (especially as upgrading photo station requires re-indexing) than
the rather cheep re-upload photos using a tool solution they have today.

Some theory
===========

So what does this do? And how do the thumbnails work?

Well that is pretty straight forward.

If you create a folder called folder 1 with two photos “photo 1.jpg” and
“photo 2.jpg” the indexer will create the following folder structure:

|image|

In other words a folder called @eaDir with a subfolder for each photo.
The subfolder representing a photo in turn contain the various
thumbnails.

The thumbnail process is configured in the following file
*/usr/syno/etc/thumb.conf* or */usr/syno/etc/thumb_high.conf* depending
on which setting you have. I use the normal one (low resolution
thumbnails) which is defined like so:

.. code-block:: bash

   size=120, quality=90, unsharp=0.5x0.5+1.25+0.0, filename=SYNOPHOTO:THUMB_S.jpg
   size=320, quality=90, unsharp=0.5x0.5+1.25+0.0, filename=SYNOPHOTO:THUMB_M.jpg
   size=640, quality=80, unsharp=0.5x0.5+1.25+0.0, filename=SYNOPHOTO:THUMB_B.jpg
   size=800, quality=90, unsharp=0.5x0.5+1.25+0.0, filename=SYNOPHOTO:THUMB_L.jpg
   size=1280,quality=90, unsharp=0.5x0.5+1.25+0.0, filename=SYNOPHOTO:THUMB_XL.jpg

Which is essentially just command line arguments for ImageMagicks
convert command (which is what I call in my script above).

Samba anyone?
-------------

A quick note is that the reason this doesn’t work via samba (smb) **I
think** is the colon character. A colon in a smb filename (at least in
windows) is a stream A pretty cool but very neglected feature of NTFS. A
stream is a file in a file meaning you can put more than one stream of
data in each file. This was a cool way to “joke” with co-workers back in
the Windows NT4 days as Explorer did not see streams. If you created a
file somewhere with 0 bytes and then put megabytes of data in a stream
the file would still be listed as 0 bytes yet take up all the space on
the hard disk |Ler|

.. |image| image:: /images/image2.png
.. |Ler| image:: /images/wlEmoticon-smile1.png
