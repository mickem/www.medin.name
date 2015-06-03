OSMC 2012 - Open Source Monitoring Conference
#############################################
:date: 2012-10-22 23:14
:author: Michael Medin
:category: Monitoring
:tags: cern, conference, icinga, nagios, nsclient++, OSMC, review, twitter, zabbix
:slug: osmc-2012-open-source-monitoring-conference
:image: /images/thumbnails/400x-/OSMC-genmeric.png

As always Netways arranged for the yearly Open Source
Monitoring Conference in Nürenburg.  As always I was suckered into
coming.

I had originally planned not to come but alas since my planned vacation
was postponed I decided on going. This is a short review of the sessions I attended and my
impressions of the conference as a whole.

.. PELICAN_END_SUMMARY

The Elevator
------------

|20121018_133428| One massive problem with the venue for this conference is that there are
no stairs (ish) so you have to use on of the two elevators when you want
to visit your room. This means when you head down for breakfast it
usually takes 5-10 minutes as you have to wait for the overfull
elevator. To top that this year they had managed to break one of the
elevator. On the upside I managed to get some nice pictures of the
surprisingly large number of components which makes up an elevator
panel.

Andreas Ericsson: News in Nagios 4.0
------------------------------------

| Conference started off with a presentation on Nagios 4 by Andreas
  Ericsson.
|  The presentation started off impressively with some Algorithm theory
  but unfortunately I never really felt he connected the rest of the
  slides with this theory (apart from dropping the odd O(x) here and
  there so I felt a bit cheated. Apart from this he did a nice job
  introducing the new performance enhancements in Nagios 4 which seems
  like pretty cool stuff.

Martin Gerhard Loschwitz: Monitoring with Pacemaker
---------------------------------------------------

| Next up was a session about Pacemaker which I guess is not strictly
  monitoring (in my sense) but a way to prevent you from even having a
  problem in the first place. Pacemaker seems like cool stuff but since
  I am not really playing much with clusters I can’t really compare.

Rihards Olups: Zabbix 2.0: Even Better
--------------------------------------

| Wow, this was really cool. The message (in comparison to Nagios?) was
|  It is open source (not open core) as well as the always reoccurring
  phrase "and it is all included" (in comparison to the
  `Nagios <http://www.nagios.org/>`__ way which tends to be it is all in
  an add-on). I really liked the presentation and much of the stuff
  which `Zabbix <http://www.zabbix.com/>`__ has “out of the box” is
  really impressive. ***Definitely on my check-it-out list.***

Lunch
-----

|20121018_124200|\ Lunch was the usual choice of food as well as the
rather nice side dishes(?) in various forms. I was rather impressed with
the glass configuration where someone had taken the time to arranged
juice and water glasses in a triangle with juice and water every other
row.

 

Jens Michelsons: Monitoring by extending the Net-SNMP agent
-----------------------------------------------------------

After attending a few minutes of this where he explained how the MIB
worked I feel naah, to basic for me and left seeking to chat a bit to
the Icinga people about “the other project”.

Christophe Haen: Monitoring at CERN
-----------------------------------

| Next up was a presentation about the monitoring they do at CERN which
  was very cool.
|  It is always interesting to hear when people who have insanely large
  environments speak especially if they have spent a lot of time working
  in the monitoring space.
|  Seems CERN previously had a “use what you like” philosophy but are
  now trying to gear towards a streamlined approach where they can
  interchange monitoring data between departments.

Sounds reasonable I guess and I have been, with NSClient++, wanted for
some time to create a standard solution.

| He also talked a lot of about CEP (Complex Event Processing) and
  self-learning monitoring which (on the theoretical side) is really
  really cool (and something I have been advocating as well).
|  ***Kudos for mentioning they use NSClient++ (made my day).***

Pierre Waellemacq: PMp - another approach to configure Nagios
-------------------------------------------------------------

Not really my cup of tea really. Was a Nagios add-on for harvesting
information via SNMP and the like? Seemed to me a lot like NIDI apart
from tighter integration with Nagios.

Evening event
-------------

|20121017_210442|\ Next up was the evening event where I met up with
the "old crew" from Tom-Tom as well with "The Zabbix" guy (I am bad with
names, ok?). And we had a blast as always. This year they had added some
entertainment in the form of light jugglers as well as what might have
been some German stand-up-comedy. No idea what they were on about since
I don't understand German at all.

The night ended early for me as I was scheduled the next day and had to
be respectable J

From what I heard “the Zabbix” guy and Andreas Ericsson had a great time
;)

Jean Gabès: Shinken
-------------------

| `Shinken <http://www.shinken-monitoring.org/>`__ is as always
  innovating and coming up with new stuff. But seems they really are
  encumbered a bit by their Nagios roots as a lot of what they do is to
  "create Nagios configuration" automagically.
|  This might seem good on paper but magic tends to break once you start
  using it to much as well as it makes things very difficult to
  understand.
|  So not sure if I agree with this really but I guess it saves time as
  long as you know what you are doing.
|  But regardless of the methods they have some really cool stuff and I
  really think `Zabbix <http://www.zabbix.com/>`__ and
  `Shinken <http://www.shinken-monitoring.org/>`__ are innovating and
  moving quite far beyond Nagios.

Michael Medin: NSClient++
-------------------------

Since this is my blog I won’t really go into my presentation apart from
saying I (as last year) had issues with the presenter and I think it is
time to abandon Logitech for a new brand to see if someone else’s stuff
is not utterly broken, seems that the Logitech can’t work when you have
a wireless microphone in the vicinity of the presenter.

Christoph Mitasch: MySQL Monitoring & Management
------------------------------------------------

| This one I was really looking forward to as I would like to know how
  to setup a MySQL monitoring myself. Unfortunately the information was
  more along the lines of "here is a bunch of plugins" and not so much
  about best practices for monitoring so did not really help me too
  much. But he did reference a book which sounded interesting so at
  least I got some information about of it.

Mike Adolphs: Monitoring Behavioral Driven infrastructures with Cucumber-Nagios
-------------------------------------------------------------------------------

| This I think a lot of people will like but for me being dev this was
  pretty much old news.
|  Disregarding that; the presentation was top notch and the subject
  really cool. Bringing BDD to the monitoring world might actually be a
  good idea?

I guess I might have liked a bit more hands on and experiences and less
theory but perhaps that is due to my dev background.

Dual German sessions and winning the twitter war!
-------------------------------------------------

|20121018_150044|\ For some odd reason each year there is one
dual-German session slot which means I tend to leave early so this was
the end of the actual conference for me.  Instead I brought my bangs
over to my new hotel where I was to stay the last night and managed to
walk around Nuremberg a bit. Finally I managed to get a shot of me
(@mickem) winning the twitter war much thanks to `Rune
Darrud <https://twitter.com/theflyingcorpse>`__ who assisted me by
repeatedly tweating my name |Ler|

After party
-----------

Finally we had the
`netways <http://www.netways.de>`__/`Icinga <https://www.icinga.org/>`__
after party which was nice this year as well. Albeit fortunately no one
(I’m looking at you Pamela) kept feeding various strange drinks this
year which meant I did in fact not have a massive hangover the next day.

The loot
--------

|DSC04204|\ Thanks to my review (`Review: Open Source Monitoring
Conference
2011 <http://blog.medin.name/2011/12/06/review-open-source-monitoring-conference-2011/>`__)
last year they managed to listen and offered some nice loot to all
attendees at the conference. This year the loot extended to a very nice
`Zabbix <http://www.zabbix.com/>`__ pen as well as a mug (blatantly
copied from last years Nagios event) but at least this was more of a
thermos cup with a water tight seal which means I can actually use it to
carry milk and such for the baby |Ler|

Thank you netways!
------------------

A big thank you to `Netways <http://www.netways.de/>`__ for arranging a
nice conference again. And see you all next year!

.. |OSMC-genmeric| image:: /images/OSMC-genmeric.png
.. |20121018_133428| image:: /images/20121018_133428.jpg
.. |20121018_124200| image:: /images/20121018_124200.jpg
.. |20121017_210442| image:: /images/20121017_210442.jpg
.. |20121018_150044| image:: /images/20121018_150044.jpg
.. |Ler| image:: /images/wlEmoticon-smile.png
.. |DSC04204| image:: /images/DSC04204.jpg
