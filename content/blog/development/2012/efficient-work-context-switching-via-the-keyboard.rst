Efficient Work: Context switching via the Keyboard
##################################################
:date: 2012-02-12 10:30
:author: Michael Medin
:category: Development
:tags: console, far manager, keyboard, multiple monitors, unix, windows, windows 7
:slug: efficient-work-context-switching-via-the-keyboard
:image: /images/BeOS_Workspaces.png
:social_image: /images/BeOS_Workspaces.png

One of the most common perceptions of windows is that it is a PUI (PARC
User interface) oriented operation system. In other words the mouse is
required to do everything. This is in many places true but fortunately
Microsoft has recently changed this and incorporated the keyboard more
and more into what was previously a mouse only domain. With Vista and
Windows 7 a whole range of new keyboard shortcuts emerged and slapping
on some third-party tools on top of that and we get a full-fledged
keyboard experience.

.. PELICAN_END_SUMMARY

This is a short introduction to how I use Modern Windows features and
various third-party tools to optimize my workflow using the Keyboards in
Windows..

History
-------

In the past context switching has for me always been associated with
Unix and the concept of virtual desktops. The idea with virtual desktop
is that you define a fixed set of contexts and then (normally) using
keyboard shortcuts you switch between them. This has been attempted many
times on windows but due to various issues with the Windows windowing
model this never works out as smoothly as it does on Unix.

Thus, me being an avid Windows user, have never really gotten around to
it. But a few years back I started to use a different approach to
context switching. I discovered a tool from
`Stardock <http://stardock.com>`__ called `Keyboard
LaunchPad <http://www.stardock.com/products/klp/>`__ which introduced
the idea of using keyboard shortcuts to switch between fixed
applications. In essence bind Explorer to +E and so on and so forth.
After having lived happily with this for years I ended up on Windows
Vista which: Tada had hijacked all my shortcut keys assigning them to
launching programs instead. Now this might sound like almost the same
thing but alas it is something very different indeed and in my humble
opinion completely useless. If I have `Google <http://www.google.com>`__
chrome started I want to switch to it not start a new
instance.Thankfully this was fixed with Windows 7 which now does
switching.

Modern Context Switching
========================

I call this modern as I feel the Unix model of having Virtual Desktops
is dated. The main problem is that virtual desktops assumes that a given
context always need the same toolkit and that a given tool is only
associated with a given context. Where as with the multi purpose tools
we have today you cant not normally associate a single tool with a
context and definitely not vice versa.

So the first ting to understand is how this is handled in Windows 7. The
idea is that the Windows button in conjunction with a number will launch
or switch to the application in the n:th place of the taskbar.
|image|\ In the following example we can thus click |image1| to switch to
Google Chrome, |image2| to switch to Thunderbird, |image3| to Visual
Studio and so on and so forth.

Now this is much better then just switching all applications around as
you quite often work with the same web browser in many context and I
tend to use notepad++ as a “clipboard history tool” and generic text
manipulation tool. So instead of switching between desktops we simply
switch between applications.

|Multiple Monitors Circa 2001|\ Multiple Monitors
=================================================

I have in for almost as long as I can remember been using multiple
monitors. It started back when I was programming assembler and you could
connect both a monochrome monitor and a color monitor (they used
different video memory) to Microsoft CodeView showing the application on
one and the debugger on the other. Then I used it with 3D Studio MAX and
pretty much everything since then. Now with modern widescreen monitors
the need is somewhat lessened (especially if you have window positions
tools in place). But I still find it extremely nice to have all passive
applications (which does not require input) reside on a side monitor and
all active (which requires input) ones on the other monitor. This means
I usually put things like chat windows, Spotify, widgets and such on the
secondary monitor.

To make the most of this though you need to quick be able to switch
application into active mode and back into passive mode. This is
important as the secondary monitor to the right of my 23” monitor is by
far to far away for me to b able to interact with it. Happily in Windows
7 `Microsoft <http://www.microsoft.com>`__ added a couple of keyboard
shortcuts for this.

|image4| will move a window from a monitor to the next monitor on the
left and |image5| will do the same moving a windows to the next right
most monitor. In my case I just have two so both these do the same:
Toggle the monitor a windows is showed upon.

Modern Console
==============

|image6| Another issue which often plagues Windows user is the lack of a modern
console application. Unfortunately Microsoft has not deemed it important
enough to rectify this with Windows 7 but fortunately others have. I
currently use two open source tools one called ConEmu-Maximus5 and the
other Far Manager. This gives me a modern tabbed console which is very
feature full and rapidly evolving. The main benefit of conemu over other
similar tools is that it integrates with Far Manger very nicely. It can
also launch putty inside tabs but this is a bit flaky currently and
nothing I use.

|image7|\ Now tying this into the keyboard I figured I would mention some
keyboard shortcuts which really makes conemu and Far Manager shine.
First off you can switch tab using Host+#. In my case this means |image8|
to |image9|. But once you add in Far you have automatically get command
history with completion as well as filename completion and other such
thing. And I honestly think the Far version of completion is by far
beyond the similar bash equal if you look in the screen shot on the
right typing **more n** pops up a list with all available file
starting with n (as well as all historical entries matching “\ **more
n**\ ”).

I think someday I will write-up a blog post on just Far manager as it is
one of the best tools I have ever come across.

Summary
-------

So to summaries a bit: Windows has a lot to offer when it comes to
keyboard shortcuts and tools for managing your contexts and work flow. I
think, as is often the case, Microsoft main problem is the perceptions
people have about their tools and not the quality of the tools.

IN this section I only mentioned three tools by name:

-  `Keyboard LaunchPad <http://www.stardock.com/products/klp/>`__
   Which I no longer use in favor of
   `AutoHotKey <http://www.autohotkey.com/>`__ which is better, more
   flexible and free (albeit slightly more difficult to use)
-  `FAR Manager <http://www.farmanager.com/>`__
   Free, Open Source file manager
-  `ConEmu-Maximus 5 <http://code.google.com/p/conemu-maximus5/>`__
   Free, Open Source shell for Windows.

In addition to this I almost mentioned another tool I use often which is
called `Actual Window
Manager <http://www.actualtools.com/windowmanager/>`__. I use this for
managing Windows and such but since I wanted to keep this article short
I left that out. It is not free and not Open Source  but has a myriad of
cool features and is to my knowledge the most complete Window Manager
out there.

.. |image0| image:: http://upload.wikimedia.org/wikipedia/commons/f/f5/BeOS_Workspaces.gif
.. |image| image:: /images/image.png
.. |image1| image:: /images/image1.png
.. |image2| image:: /images/image2.png
.. |image3| image:: /images/image3.png
.. |Multiple Monitors Circa 2001| image:: /images/P1010003.jpg
.. |image4| image:: /images/image4.png
.. |image5| image:: /images/image5.png
.. |image6| image:: /images/image6.png
.. |image7| image:: /images/efficient-work-context-switching-via-the-keyboard-image7.png
.. |image8| image:: /images/efficient-work-context-switching-via-the-keyboard-image8.png
.. |image9| image:: /images/efficient-work-context-switching-via-the-keyboard-image9.png
