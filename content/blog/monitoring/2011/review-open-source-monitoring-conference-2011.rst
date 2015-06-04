Review: Open Source Monitoring Conference 2011
##############################################
:date: 2011-12-06 21:21
:author: Michael Medin
:category: Monitoring
:tags: conference, icinga, nagios, netways, OSMC
:slug: review-open-source-monitoring-conference-2011
:image: /images/OSMC-62.png
:social_image: /images/OSMC-62.png

A rather more honest review of the
`OSMC <http://www.netways.de/en/osmc/y2011/>`__ conference 2011 then the
spoof comparison yesterday.

Unfortunately I did not take much in the way of photos this year (don’t
know why actually) so no photos.

.. PELICAN_END_SUMMARY

My overall impression was that it was a really nice conference with some
really interesting sessions. A drawback for me was again this year the
Incinga session was in German (meaning I understood little of it) as
well as there being two “all German” slots (meaning I sort of missed not
only Icinga but also another session) this as I don’t speak German.
Again since I only speak English I attend the so called English track
which consist of the sessions mentioned I this review.

The first session I attended was **SNMPv3 Made Easy** by Dr.
**Michael Schwartzkopff**. Since I had bumped in to Dr Schwartzkopff
the night before and chatted a bit I had a good impression of him and
the talk and he did not let me down. I would probably argue that SNMPv3
is not really simple (without actually having used it) as it is fairly
complex. Especially if you compare it to the older SNMP which “just
works” when it comes to SNMPv3 there is a  lot of things which can go
wrong (and judging by my Italian friend sitting next to me: it also
does). But all in all he did an excellent job of slicing the information
into digestible chunks and I would say I have a good understanding of
SNMPv3 now.

|DSC02790|\ The next session was **Georg Kostner** (strangely enough
not Juergen Virginia who was also at the conference) from `Würth
Phoenix <http://www.wuerth-phoenix.com/en/>`__ who presented their
`safed <http://www.neteye-blog.it/downloads/>`__ a log demon for Unix
and Windows.The talked which carried the rather long title “\ **Safed
as an agent for supporting a central collection of events with
SYSLOG**\ ” was in essence a quick introduction to
`safed <http://www.neteye-blog.it/downloads/>`__ which is interesting
and I kept thinking: I need to steel it all for my
`NSClient++ <http://nsclient.org/>`__ project. But we shall see for now
I will focus on getting 0.4.0 out the door. It was an interesting
session and albeit much of the challenges they had revolved around
Italian legislation I think the overall agent is sound and worth wile.

Then it was time for the one I had been looking forward to the most
**Monitoring Solutions for the Next Decade** and it was, in difference
to a similar session on Nagios World Conference, very very good.
**Olivier Jan** from the French Nagios community presented his
predictions for the next 10 years all the whilst presenting various
existing projects which provided the embryos to support his predictions.
So in addition to prediction the future he also did a very good job of
explaining how you cold easily get half-way there today. I tended to
agree with most of his predictions but I lacked a segment about
simplifying monitoring and configuration which I personally think is
overly complicated today.

Then we had the usual lunch which was a nice buffet in addition to some
rather tasty small treats they branded as “finger food”. As always the
menu was in German giving me ample reason to convers with my neighbors
around the table to figure out what the various treats was.

Next I decided to skip **Reinhard Scheck** and his **Cacti Graphing
Solution** presentation citing I had seen it before but mainly I had to
work on my own presentation for the next day which was sorely lacking.

Then we had **Remo Rickli** a guy from Switzerland speaking very good
English with a rather American accent but given that he had lived in the
States I guess there was a reason for it. His talk was really the **gem
of the conference** **NeDi - Network Discovery** such a humble little
thing. `NeDi <http://www.nedi.ch/>`__ really seems to combine a
tremendous feature set with almost child like ease of use. Very
impressive this is definitely something I will investigate in the future
(even though I probably only have 5 SNMP capable devices).

Then it was time for the last session of the day which was **The Icinga
Team** (read **Bernd Erk**) presenting **The Latest from Icinga**.
Unfortunately again in German so my understanding was rather limited.
From what I can say Icinga seems to still be a thriving nice community
and a lot of things have both been delivered as well as in the pipe for
the next few years.

|Vin_chaud_2|\ The the evening event kicked off and we spend the day
walking towards the
`ChristKindlMarkt <http://www.christkindlesmarkt.de/>`__ in Nuremberg
where we went to a restaurant and had some Glüewein. Around now I teamed
up with a Dane working at “the Muhammad Cartoon Newspaper” (security was
apparently pretty tight there) Juergen Virginia from Würth Phoneix whom
I have meet many times before as well as some other guys I cant remember
the name of. As always it was nice food, nice beer, nice drinks and
perhaps more of all nice company. Unfortunately, as I had the morning
session, I retired early and went home around midnight. From what I
understood some people got home around 4-5 which meant they bumped into
my session fashionably late (I’m looking at you Rune).

|DSC02775|\ Starting the second day was me (**Michael Medin**) giving
a session on **Distributed monitoring with NSClient++**. Cant really
say much for my talk but I mainly did some gags around playing Skyrim
instead of writing slides. I had planned to do some videos of me using
the scenarios but since my virtual machine refused to recover network
after switching hotspot I gave up on the idea late the night before.
Something I hope to rectify for next time.

Next up was **Werner Fischer** from `Thomas
Krenn <http://www.thomas-krenn.com>`__ who pressented **Hardware
Monitoring with the New IPMI Plugin v2** which was really cool. Whenh I
last tried to doe something like this was way back some 10 years ago and
then it was very very difficult to even get access to this kind of data.
But seems nowadays it is dead simple to monitor the hardware from the
hardware!.

Then I decided to miss another session sitting down with amongst other
Juergen speaking a bit about how to create a configuration interface for
NSClient++.

This break was followed by another gem of a presentation from **Jean
Gabès** who gave a talk on **Shinken - The Next Chapter**. I have
always considered Shinken as a cool idea but… Now after this talk I get
pretty hooked and I definitely need to check it out. Really cool stuff
with some pretty interesting concepts solving many of the problems found
with Nagios (and inherently Icinga).

Lastly I they had a double German session which is something that annoys
me a bit. When they have an **“English track”** I think they should
have an **English track** and no dual-German sessions.

Anyways I decided to call it a day and headed home to catch an hour or
so of sleep as I was very very tired. This showed to be remarkable good
thinking as when I got back 2-3 hours or so later I hooked up with
Netways/Icinga who had a beer after the conference. This beer turned
into food, which turned into (rum) drinks which turned into bar-hopping
which turned into… well… I got home around 4 in the morning, and woke up
the next day around noon with a seriously nasty hangover!

And thus ended the 6:th edition of the Open Source Monitoring
Conference!

.. |DSC02790| image:: /images/DSC02790.jpg
.. |Vin_chaud_2| image:: /images/Vin_chaud_2.jpg
.. |DSC02775| image:: /images/DSC02775.jpg
