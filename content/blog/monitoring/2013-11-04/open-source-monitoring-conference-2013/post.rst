Open Source Monitoring Conference 2013
######################################
:author: Michael Medin
:tags: conference, icinga, nagios, netways, nsclient++, NSCP, OSMC, travel
:image: /images/CameraZOOM-20131023085443841.jpg
:social_image: /images/CameraZOOM-20131023085443841.jpg

As always I really enjoyed the conference as much as the social aspect
of it. It truly is one of the best conferences in the field. This was my
sixth year which `as I noted earlier <http://blog.medin.name/?p=989>`__
started out a bit weird. I will not cover the limousine story here again
instead this is purely about the conference.

The conference started off with the
usual introduction by `bernd <https://twitter.com/gethash>`__ who did it
in English this year which I think was nice but quite frankly the usual
“food is in the food area” and “conference is in the conference are” I
can pretty much understand even in German. As I only speak English I
will, as usual, only cover the English track here.

.. PELICAN_END_SUMMARY

Monitoring network traffic using ntop-ng
----------------------------------------

This was extremely interesting for me (not because I am very interested
in network monitoring) but because he did a lot of cool stuff which I
intend to steal, like the web which was written in
`Lua <http://www.lua.org/>`__ and so on and so forth.

The It was pretty cool that “ntop” which I use quite frequently has
grown to become so much more then I know it was.

Making monitoring simple?
-------------------------

|DSC07334|\ Given that this was my session I wont really comment, except
that I got some question this year which I always appreciate. And it
seemed like the ntop-ng guy actually got excited about the filtering
stuff.

End User Experience Monitoring with `Al’exa <http://www.alexa-monitoring.com/>`__
---------------------------------------------------------------------------------

To be honest I sort of skipped this one and did some chatting, Not
because I think Georg does a bad job nor because I think it is a bad
project but mainly that I had already seen this in Bolzano earlier this
fall. It is an interesting concept however and from what I know they are
the only Open Source player in this field.

News in `Nagios <http://www.nagios.org/>`__ `Naemon <http://naemon.github.io/>`__ 4.1 and 5.0
---------------------------------------------------------------------------------------------

|CameraZOOM-20131023142337912|\ This was really interesting, mainly due
to the story (which I sort of knew about in advance) but it was very
emotional and you could really feel that Andres was less then happy
about the outcome. One could tell he did not want the fork and felt that
all his work was being neglected by Nagios Inc. and that they treated
him unfairly by kicking him.

During the last fork refused to get involved in the Nagios soap opera
and will do so yet again this time. But to be fair one has to ask. When
a project has been forked publicly but core developers twice: maybe
there is something not right at the source?

`Flapjack <http://flapjack.io/>`__ – monitoring notification system.
--------------------------------------------------------------------

|DSC07327|\ This was a bit long winded talk which was on the interesting
side but seemed mainly about the problems with current monitoring
solutions and why `Flapjack <http://flapjack.io/>`__ was created as well
as how it had evolved. I am not really sure if it is useful or not but
it is always nice to see new ideas.

`Adagios <http://adagios.org/>`__ – Web configuration done right!
-----------------------------------------------------------------

I had to see this one because last time I complained about his slides
and he promised to improve them. To be fair they looked a bit better but
the transitions was still choppy. That aside
`adagios <http://adagios.org/>`__ is really really cool and probably the
best configuration interface for Nagios ever conceived.

Evening event!
--------------

|CameraZOOM-20131023195143563|\ The evening event was as always at a new
venue (though it was remarkably similar to a place we visited a few
years back). It was pretty ok but I really disliked the bench concept
since it made talking difficult. Essentially they had a single long
bench going down the side of the room so there was no one across (apart
from the poor people standing).

An interesting thing was the smoking they had going on (smoking of
food). One wonders how much flavor food picks up in 3 minutes inside a
smoking chamber?

After party
-----------

|CameraZOOM-20131024013056555|\ Since I had asked to be scheduled on the
first day for my presentation this year I was pretty much forced to make
sure I stayed up all night for the after party. And to be honest I think
I did a fair job of it. I hit my bed around 05-06 or some such in the
morning and from what I heard the only up later was Andres Ericsson
which managed to stay up till breakfast.

I wont go into details about the after part apart from saying I had a
great time and Check Point Jenny was not as bad as I had expected.

`Zabbix <http://www.zabbix.com/>`__: A Practical Demo
-----------------------------------------------------

Last year the “\ `zabbix
guy <http://www.packtpub.com/article/rihards-olups>`__\ ” was pretty
active at the After Part so we joked about it being the reason for
getting my usual slot. If that is true or not we will probably never
know but it did make for a good joke. Unfortunately my bed time and his
presentation time did not match to well so I ended up just catching the
end of it. Which was a shame as I really like
`Zabbix <http://www.zabbix.com/>`__. But hopefully he will be back next
year.

`Monitoring and Discovery without Limit <http://techthoughts.typepad.com/managing_computers/>`__
------------------------------------------------------------------------------------------------

|CameraZOOM-20131023164639885|\ The very entertaining (and selling)
`Alan Robertson <https://twitter.com/OSSAlanR>`__ was up next and tried
to convince the world we need to be assimilated by his nano probes. In
all honest I have to say it all sounds really cool but like nano probes
it al seems a bit too much like Science Fiction. But perhaps next year
he will show up and demo the system he wants to build but it all seems
like a lot of vaporware™ currently. That said a lot of the technology is
awesome and really really cool. And he has from what I can tell
delivered before so we shall see.

`openTSDB <http://opentsdb.net/>`__ – metrics for a distributed world
---------------------------------------------------------------------

|CameraZOOM-20131024204047843|\ Another “wow” moment.
`openTSDB <http://opentsdb.net/>`__ seem really really cool and
something I will look into integrating into
`NSClient++ <http://nsclient.org/>`__. It is a bit like RRD but without
any of the drawbacks. In other words pure awesomeness.

TKmon – easy web-based configuration of `Icinga <https://www.icinga.org/>`__
----------------------------------------------------------------------------

This one was a bit so-so seemed like a very special tool for a very
special use case.

Not sure it will survive outside the small space it now occupies. It
surly looks nice and surely solves a number of problems but they all
seemed very specific and not very extensible.

Distributed Monitoring and Cloud Scaling for Web Apps
-----------------------------------------------------

|CameraZOOM-20131024161758657|\ This was a pretty cool way to monitor
and auto scaling environment purely in the cloud. I personally think
they missed a key issue as they only monitored the state they had not
the state they wanted but that could be me not understanding the cloud
environment. Still the concept is really cool.

Why dynamic and adaptive thresholds matters
-------------------------------------------

This was a presentation by `Anders
Håål <https://twitter.com/thenodon>`__ from Sweden about his really cool
tool `BisCheck <http://www.bischeck.org/>`__ which can do some adaptive
thresholds stuff. Fairly impressive stuff but a bit on the mathematical
side which I think is why it is a bit to difficult to use. But with some
templates and a nice UI it could actually become really really cool.

The end: Where is my loot?
--------------------------

|DSC07340|\ Thus ended the Open Source Monitoring Conference 2013
edition. It was probably even better than last year and as I have said
before the best Monitoring conference I know about! So if you have any
interest in monitoring be sure to `book a place at next years
conference <http://www.netways.de/osmc/>`__ before the tickets run out!
(which they have been doing for the last few years). Speaking of loot: I
guess Nagios World was better this year. While OSMC still have the
wicked cool star-system on the badges and some seriously wicked cups
that was pretty much it.

**So the only bad thing you can say about the conference is that there
is no t-shirt!**

.. |CameraZOOM-20131023085443841| image:: /images/thumbnails/300x-/CameraZOOM-20131023085443841.jpg
.. |DSC07334| image:: /images/thumbnails/300x-/DSC07334.jpg
.. |CameraZOOM-20131023142337912| image:: /images/thumbnails/300x-/CameraZOOM-20131023142337912.jpg
.. |DSC07327| image:: /images/thumbnails/300x-/DSC07327.jpg
.. |CameraZOOM-20131023195143563| image:: /images/thumbnails/300x-/CameraZOOM-20131023195143563.jpg
.. |CameraZOOM-20131024013056555| image:: /images/thumbnails/300x-/CameraZOOM-20131024013056555.jpg
.. |CameraZOOM-20131023164639885| image:: /images/thumbnails/300x-/CameraZOOM-20131023164639885.jpg
.. |CameraZOOM-20131024204047843| image:: /images/thumbnails/300x-/CameraZOOM-20131024204047843.jpg
.. |CameraZOOM-20131024161758657| image:: /images/thumbnails/300x-/CameraZOOM-20131024161758657.jpg
.. |DSC07340| image:: /images/thumbnails/300x-/DSC07340.jpg
