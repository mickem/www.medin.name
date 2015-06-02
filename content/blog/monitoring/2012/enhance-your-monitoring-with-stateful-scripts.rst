Enhance your monitoring with stateful scripts
#############################################
:date: 2012-11-26 00:25
:author: Michael Medin
:category: Monitoring
:tags: icinga, lua, nagios, nsclient++, scripting, windows
:slug: enhance-your-monitoring-with-stateful-scripts
:image: /images/lua.gif
:social_image: /images/lua.gif

Stateful scripts are a simple yet powerfully way to enhance your
monitoring which I think is used far to little. Using stateful script
you can easily add simple predictions and change management. This is
very easy to accomplished using NSClient++ as its built-in scripting
modules by default provides stateful scripts (in contrast to Nagios and
`Icinga <https://www.icinga.org/>`__ which tends to be stateless). This
tutorial will walk you through writing a simple stateful script in Lua.
If you are still confused about stateful scripts the main benefit is
that they remember things. Thus you can alert when something changes as
well as predict the future. A good example of this is disk growth
prediction but there are a lot of other scenarios where they are useful.

.. PELICAN_END_SUMMARY

Remember the language: What is Lua?
-----------------------------------

`Lua <http://www.lua.org/>`__ scripts are pretty straight forward to
write, the biggest issue is that `Lua <http://www.lua.org/>`__ is a bit
of arcane language (if you ask me) with a very basic set of features
which means you end up writing a lot of the things you need by hand (in
contrast to so other scripting languages such as
`Python <http://www.python.org/>`__ or Perl which has massive libraries
with pretty much everything you need already written). The big benefit
to using `Lua <http://www.lua.org/>`__ is that it is easily embeddable
and requires very little in the form of infrastructure hence it is fully
embedded inside `NSClient++ <http://nsclient.org/>`__ and you need
nothing else.

Thus I try to keep things simple and use python if I need to do
something advanced. As a note I would like to add that there are a lot
of libraries and such for `Lua <http://www.lua.org/>`__ but due to
linkage it is not easy to get many of the native once to work “out of
the box”.

Remember the begging: Writing a simple Lua script
-------------------------------------------------

Lets get our hands dirty and begin by looking at a simple
`Lua <http://www.lua.org/>`__ script and dissect it bit by bit:

.. code-block:: text

     nscp.print('Hello world from Lua...')
    
    .. raw:: html
    
       </p>
    
    function my\_command(command, args)
     nscp.print('Yayyy we got executed: ' .. command)
     return 'ok', 'Everything is fine', ''
     end
    
    reg = nscp.Registry()
     reg:simple\_query('lua\_test', my\_command, 'This is a sample Lua
      script')
    >THE END<

Since I am not about to teach you `Lua <http://www.lua.org/>`__
scripting (there are plenty of
`tutorials <http://www.lua.org/docs.html>`__ for that already) I will
only quickly walk you through the script.

The first line uses the dot notation to access a static function inside
the nscp object or namespace. This is similar to
***System.out.println()*** in java in many ways. The string you pass to
the function is sent to the NSCP log.

Then we have a block ***function … end*** which creates a function
inside our script. The function again use the print function to tell us
it is being executed and then returns a result (think
`nagios <http://www.nagios.org/>`__) saying the status is ok with a
friendly message.

Lastly we have some object orientation. We create an instance of the
Registry object calling it reg and then use the colon operator (notice
colon!!!!) to access the (non static) member function simple_query
which registers a query (which is a fancy name for function available to
call).

An important note about : syntax versus . in lua. Lua has no real
concept of “objects” hence you have to pass around the “object” when you
call functions. To work around this they have a : operator which is a
bit of a macro the to make this simpler thus the following are
equivalent:

#. ***reg.simple_function(reg,‘lua_’test’, …)***
#. ***reg:simple_function(‘lua_’test’, …)***

This is in a way similar to how `python <http://www.python.org/>`__
handles self but in lua there are different syntaxes.

So lets fire this baby up and see how to use this from
`NSClient++ <http://nsclient.org/>`__.

.. code-block:: text

     # rm nsclient.ini (or del nsclient.ini)
     nscp settings --activate-module LUAScript
     nscp settings --path /settings/lua/scripts --key foo --set
    demo\_001.lua
    >THE END<

When I demo something or write tutorials I tend to always start by
removing the configuration to make sure there is no residual old
configuration somewhere causing havoc. Then the first step is to load
the LUAScript module as well as add our script. Next we start
`NSClient++ <http://nsclient.org/>`__ using the --log option to skip
debug logging. If you have problems you might want to remove this option
to see any debug messages which might help pinpoint the problem.

.. code-block:: text

    highlight="2"]
     nscp test --log info
     l pts/lua/demo\_001.lua:1 Hello world from Lua...
     l ce\\simple\_client.hpp:32 Enter command to inject or exit to
    terminate...
    >THE END<

As we can see here we get the message in the script printed as the
entire script is executed when `NSClient++ <http://nsclient.org/>`__ is
started. Next we use the command “commands” to list all commands in our
case the lua_test command is present as that is the one exposed from
our script.

.. code-block:: text

    highlight="1,3"]
     commands
     l ce\\simple\_client.hpp:54 Commands:
     l ce\\simple\_client.hpp:57 \| lua\_test: Tis is a sample Lua script
    >THE END<

Finally we run the command and then exit. Our command will first print
the message and then return an OK message with associated status text.

.. code-block:: text

    highlight="2,3"]
     lua\_test
     l pts/lua/demo\_001.lua:4 Yayyy we got executed: lua\_test
     l ce\\simple\_client.hpp:80 OK:Everything is fine
     exit
    >THE END<

So there we have it a few simple lines of `Lua <http://www.lua.org/>`__
and we are already on our way to create our state full disc check
script. Next up we shall learn about wrapping
`NSClient++ <http://nsclient.org/>`__ commands and using state.

Remember the past: The power of state
-------------------------------------

Now that we have rudimentary understanding of how to create a Lua script
and wire it up to NSClient++ lets begin exploring the newfound power of
state. The first thing we shall do is use the built-in disk check
commands and wrap that so we can store the data in between runs. The
simplest way to wrap a command inside a Lua script is to use the
simple_query function in the core object like so:

#. local core = Core()
#. code,msg,perf = core:simple_query('lua_test', {'a', 'b'})

In our case we want to check the C drive so we run the following command
(due to a rather annoying “feature” in NSClient++ we wont get
performance data unless we have a warning or critical criteria):

-  *checkDrive drive=c maxWarn=90%*
-  code,msg,perf = core:simple_query('checkDrive', {'c:',
   'maxWarn=90%'})

So what we do expose a function which simple run this command and return
the data as is. Now to create the idea of state we will use an internal
variable to append the performance data on top of each other so every
time we call it we will get a bit more.

The script in its entirety looks like this:

.. code-block:: text

     gperf = ''
     function drive\_statefull(command, args)
     local core = nscp.Core()
     code,msg,perf = core:simple\_query('checkDriveSize', {'c'})
     gperf = gperf .. perf
     return code, msg, gperf
     end
    
    .. raw:: html
    
       </p>
    
    reg = nscp.Registry()
     reg:simple\_query('check\_sdrive', drive\_statefull, 'Check if the
      drive is full (statefull nonsense version)')
    >THE END<

Now don’t forget to load the CheckDisk module as well using the
following command: ***nscp settings --activate-module CheckDisk***

A session with nscp test using the script will look like this (again
starting it with ***nscp test --log info***):

.. code-block:: text

     check\_sdrive
     l ce\\simple\_client.hpp:80 OK:OK: All drives within bounds.
     l ce\\simple\_client.hpp:82 Performance data: 'c: %'=98% 'c:'=221.21G
     check\_sdrive
     l ce\\simple\_client.hpp:80 OK:OK: All drives within bounds.
     l ce\\simple\_client.hpp:82 Performance data: 'c: %'=98%
    'c:'=221.21G'c: '%''=98% 'c:'=221.21G
     check\_sdrive
     l ce\\simple\_client.hpp:80 OK:OK: All drives within bounds.
     l ce\\simple\_client.hpp:82 Performance data: 'c: %'=98%
    'c:'=221.21G'c: '%''=98% 'c:'=221.21G'c: '%''=98% 'c:'=221.21G
     check\_sdrive
     l ce\\simple\_client.hpp:80 OK:OK: All drives within bounds.
     l ce\\simple\_client.hpp:82 Performance data: 'c: %'=98%
    'c:'=221.21G'c: '%''=98% 'c:'=221.21G'c: '%''=98% 'c:'=221.21G'c:
    '%''=98% 'c:'=221.21G
    >THE END<

If you scroll to the right you can see that every time we run the
command we get a bit more performance data returned. So state handling
and wrapping commands is really simple using NSClient++ built in
scripting. Now we are off to try to add some real logic and start making
some real predictions.

Remember the future: Making simple predictions
----------------------------------------------

The simplest way to access the actual values is to use the performance
data. To use performance data from scripts there are a few things we
should tweak in our command. The first thing is to make sure we have the
same units (as having to manage unit changes will be cumbersome) to
facilitate there is an option we can use called perf-unit=K which means
we will always get performance data in kilobytes.

The other thing we need to do is force CheckDriveSize to return the full
size value to do this we need to have at least one bounds check so we
will add MaxWarn=80%. Thus our checkDriveSize command will look like
this: ***checkDriveSize c 'perf-unit=K MaxWarn=80%***.

But lets return to our script and do a quick walk-through of what we
want the script to do.

#. Store the date and time as well as the value of the last check.
#. Extract the current value and maximum size from the performance data
#. Calculate the rate of change (in bytes per second)
#. Calculate the expected value 7 days from now
#. If the expected value 7 days from now is above the maximum change the
   status to critical and set the message

That is pretty much it but of course the script will be a bit more code
as we need to accomplish all this. The entire script looks like this:

.. code-block:: text

     last\_value = 0
     last\_time = 0
     function split\_perfdata(str)
     for v,w,c,mi,ma in string.gmatch(str,
    "(%d-)K;(%d-);(%d-);(%d-);(%d\*)") do
     return v,w,c,mi,ma
     end
     return nil
     end
     function make\_perfdata(v,w,c,mi,ma)
     return v..'K;'..w..';'..c..';'..mi..';'..ma
     end
    
    .. raw:: html
    
       </p>
    
    function drive\_statefull(command, args)
     -- Reset all variables to default values
     value = 0
     delta = 0
     change = 0
     extra\_perf = ''
     time = os.time()
     -- Execute drive check command
     local core = nscp.Core()
     code,msg,perf = core:simple\_query('checkDriveSize', {'c',
      'perf-unit=K', 'MaxWarn=80%'})
     -- Extract all (for simplicity we support only one)
     for k,d in string.gmatch(perf, "'?(.-)'?=([%d;K%%]\*) ?") do
     if not string.find(k, '%%') then
     v,w,c,mi,ma = split\_perfdata(d)
     value = v\*1024
     max = ma\*1024
     end
     end
     -- If we have values: Check values and caluclate rates
     if value ~= 0 and last\_value ~= 0 then
     change = (value - last\_value)
     duration = time-last\_time
     nscp.print('Change: '..change .. ', Duration: '..duration)
     if change ~= 0 and duration ~= 0 then
     delta = math.floor(change / duration)
     -- caluclate predicated value one week from now and create perf data
     predicted\_value = value + (delta\*7\*24\*60\*60)
     extra\_perf = " 'c: +7d'=" ..
      make\_perfdata(math.floor(predicted\_value/1024),0,0,0,math.floor(max/1024))
     if predicted\_value > max then
     code = 'crit'
     msg = 'We expect to be full in a week'
     end
     end
     end
     -- If we have a new value update "last value"
     if value > 0 then
     last\_value = value
     last\_time = time
     end
     return code, msg, perf .. extra\_perf
     end
    
    reg = nscp.Registry()
     reg:simple\_query('check\_sdrive', drive\_statefull, 'Check if the
      drive is full')
    >THE END<

So there we have it amazing magic to warn if the disk will become full
in the next seven days. Now this is a very crude script and not very
useful in the real world but more about that in the next section.

Remember perfection: My script sucks!
-------------------------------------

This script has several critical flaws and the most obvious one is that
if we run this check every 5 minutes we will only use the last 5 minutes
as basis for our prognosis this is rather crude as if we temporarily get
a lot of disk activity during this period we will erroneously report
that it will be full in 7 days. A better approach would be to use a
normalized value over the last 24 hours or something along those lines.

Another problem is that we have hard-coded this to work only with the C
drive. And worse is we can't even handle more than one drive currently.

Neither do we accept any arguments so the boundaries are fixed currently
at 80% as well as 100%.

Finally this script could easily be used for checking other metrics as
well by making the command configurable.

But the aide here is to introduce stateful scripts not create miles and
miles of Lua code. So I have tried to keep this as simple as possible.
The idea is to follow up with a new tutorial in the future which show
cases some more advanced features of both Lua and NSClient++ such as
using libraries, reading configuration as well as some other nifty
features.

***But hopefully I have wetted your appetite a bit and hopefully you
have enough information here to start creating some stateful scripts of
you own!***

.. |lua| image:: /images/lua_thumb.gif
   :target: /images/lua.gif
