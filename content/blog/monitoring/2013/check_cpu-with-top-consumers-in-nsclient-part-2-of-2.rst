check_cpu with top consumers in NSClient++ (part 2 of 2)
########################################################
:date: 2013-12-16 08:21
:author: Michael Medin
:category: Monitoring
:tags: icinga, lua, monitoring, nagios, nsclient++, scripting, windows
:slug: check_cpu-with-top-consumers-in-nsclient-part-2-of-2
:image: /images/check_cpu-with-top-consumers-in-nsclient-part-2-of-2.png
:social_image: /images/check_cpu-with-top-consumers-in-nsclient-part-2-of-2.png

A tutorial for writing a quick and simple `Lua <http://www.lua.org/>`__
script which will turn check_cpu into a multi functional check which
return top CPU consumers. In last weeks edition I introduced the various
parts we need to make this a reality. And that idea I have with
`NSClient++ <http://nsclient.org/>`__ is to create a Lego box with small
multi purpose functions which the users can combine in many different
ways. Here I will show you how we can do that.

.. PELICAN_END_SUMMARY

Before you embark on this article please review the first part:
`check_cpu with top consumers in NSClient++ (part 1 of
2) <http://blog.medin.name/?p=1045>`__

Here is a quick summary of the necessary parts.

**Modules:**

-  LUAScript
-  CheckSystem
-  CheckHelpers

**Commands:**

-  check_cpu
-  check_process
-  filter_perf

Writing Lua scripts
===================

This tutorial is not about teaching the Lua language (refer to the Lua
docs for that). But there is a few things we need to understand about
how Lua scripts work in NSClient++.

First thing we need to understand is that the script will be loaded
as-is before it is executed. Now while you can add as much code as you
like during the loading phase it is generally a good idea to keep this
short as it will slow down NSClient++ startup.

The general way a script is executed is:

#. load
   Used to parse, load and bind all functions
#. main()
   Used if the script is executed from command line. This is where the
   “script” logic should be placed.
#. Any bound function/query/\*
   This is similar to the main function except intended for general
   purpose code such as queries and functions. This means that whenever
   a function is executed via NRPE it will be executed.

The code which is executed during load is all code inside the script.
This means that if you place “logic” there it will be executed.

In the case of command line execution of a script after it has been
loaded the main function will be called. In our case this is where we
install the script.

In the much more common case when the script provides functionality
nothing else will happen until the functionality is requested via
check_nrpe or similarly.

To summarize this a bit:

-  main()
   This is where we place our static functionality such as installation
   (or uninstallation).
-  in the script (outside of functions)
   This is where we place function to bind to NSClient++
-  bound functions
   This is where we place dynamic functionality which will b executed
   via check_nrpe.

A quick example
===============

Now this is a tad confusing so lets show a quick example.

.. code-block: lua

   local reg = nscp.Registry()
   reg:simple_query('check_cpu_ex', check_cpu_ex, 'Check CPU version which returns top consumers')
   
   function check_cpu_ex(command, request_payload, request_message)
    return ''
    end
   
   function main(args)
    cmd = args[0] or ''
    if cmd == 'install' then
    return 'ok', 'Script installed'
    else
    return 'error', 'Usage: .. install'
    end
    end

The first two lines is not contained in a function. They will be
executed when we load the script. What they do is bind a function to a
query. In essence after these lines we can do:

.. code-block: text

   check_nrpe ... -c check_cpu_ex

Then we have the function ***check_cpu_ex*** which is what will be
called. Right now we don’t do anything at all but later we will add some
code in this function to call ***check_cpu***.

Lastly we have the main function where we check the input arguments and
if they contain install we return ok and the message ***Script
installed**.*

This allows us to run the following:

.. code-block:: text

   nscp lua --script check_cpu_ex install

Installation
============

Lets start on our real script. The first thing we need to do is make it
simple to add the script. Currently adding this script requires a bit of
configuration:

.. code-block:: ini

   [/modules]
   CheckHelpers = enabled
   CheckSystem = enabled
   LUAScript = enabled
   
   [/settings/lua/scripts]
   check_cpu_ex = check_cpu_ex

So what we do is we create a lua function called install and add some
code to it which will install our script. We also reuse the main
function from above and add a call to our install function.

Starting with the install function we first get the settings instance
and then we in turn setup all the above keys.

.. code-block::lua

   function install()
      -- Used to install this script
      local conf = nscp.Settings()
      conf:set_string('/modules', 'CheckSystem', 'enabled')
      conf:set_string('/modules', 'CheckHelpers', 'enabled')
      conf:set_string('/modules', 'LUAScript', 'enabled')
      conf:set_string('/settings/lua/scripts', 'check_cpu_ex', 'check_cpu_ex')
      conf:save()
   end

And our our modified main function looks like this:

.. code-block::lua

   function main(args)
     cmd = args[0] or ''
     if cmd == 'install' then
       install()
       return 'ok', 'Script installed'
     else
       return 'error', 'Usage: .. install'
     end
   end

Calling binding functions
=========================

In our previous code we placed the bind function in the body of the
script. This is not very nice so we will change it slightly here to
place all the setup code inside a function called setup and then call
that function from the body. This has the same effect but makes it look
a bit nicer.

.. code-block:: lua

   function setup()
   -- register our function
   local reg = nscp.Registry()
   reg:query('check_cpu_ex', check_cpu_ex, 'Check CPU version which returns top consumers')
   end
   
   setup()

Calling check_cpu
==================

The previous code chunks bound ***check_cpu_ex*** with our function so
lets create that function now.

.. code-block:: lua

   local core = nscp.Core()
   cpu_result, cpu_message, cpu_perf = core:simple_query('check_cpu', arguments)
   if cpu_result == 'UNKNOWN' then
   core:log('error', string.format('Invalid return from check_cpu: %s', cpu_result))
   return cpu_result, cpu_message, cpu_perf
   end

We will use all “simple” commands here to make things simple to
understand. The difference between the *simple* and the *raw functions*
is that the simple ones only return strings. This means we would have to
parse the performance data if we wanted to get access to it. Since we
don’t need that here we use the simple calls.

The first thing we do is get an instance to the core object so we can
interact with NSClient++.

.. code-block::lua

   local core = nscp.Core()

Next up we forward all our arguments to the regular check_cpu command.

.. code-block:: lua

   cpu_result, cpu_message, cpu_perf = core:simple_query('check_cpu', arguments)

Next up we check that we get ok/warning/critical (if we get an unknown
something is wrong).

.. code-block::lua

   if cpu_result == 'UNKNOWN' then
     core:log('error', string.format('Invalid return from check_cpu: %s', cpu_result))
     return cpu_result, cpu_message, cpu_perf
   end

And that is pretty much it so wrapping a call inside Lua is pretty
straight forward.

Calling check_process
======================

Calling check_process is more of the same. Since we have already
covered the filter_perf in previous chapter I will just execute the
command here so refer to the previous article for details about what
this does.

.. code-block:: lua

   -- Status is good, lets execute check_process and filter_perf.
   proc_result, proc_message, proc_perf = core:simple_query('filter_perf', {'command=check_process', 'sort=normal', 'limit=5', 'arguments', 'delta=true', 'warn=time>0', 'filter=time>0'})

The last thing to do is swap the original message with the list of top
CPU consumers. This information we get back in the performance data from
filter_perf/check_process.

.. code-block::lua

   return cpu_result, 'Top preformers: ' .. proc_perf, cpu_perf

That’s all folks
================

And that’s all there is to it the script in its entirety looks like
this:

.. code-block:: lua

   function install()
    -- Used to install this script
    local conf = nscp.Settings()
    conf:set_string('/modules', 'CheckSystem', 'enabled')
    conf:set_string('/modules', 'CheckHelpers', 'enabled')
    conf:set_string('/modules', 'LUAScript', 'enabled')
    conf:set_string('/settings/lua/scripts', 'check_cpu_ex', 'check_cpu_ex')
    conf:save()
   end

   function setup()
     -- register our function
     local reg = nscp.Registry()
     reg:simple_query('check_cpu_ex', check_cpu_ex, 'Check CPU version which returns top consumers')
   end

   function check_cpu_ex(command, arguments)
     local core = nscp.Core()
     cpu_result, cpu_message, cpu_perf = core:simple_query('check_cpu', arguments)
     if cpu_result == 'UNKNOWN' then
       core:log('error', string.format('Invalid return from check_cpu: %s', cpu_result))
       return cpu_result, cpu_message, cpu_perf
     end
     -- Status is good, lets execute check_process and filter_perf.
     proc_result, proc_message, proc_perf = core:simple_query('filter_perf', {'command=check_process', 'sort=normal', 'limit=5', 'arguments', 'delta=true', 'warn=time>0', 'filter=time>0'})
     return cpu_result, 'Top preformers: ' .. proc_perf, cpu_perf
   end
   
   setup()
   
   function main(args)
     cmd = args[0] or ''
     if cmd == 'install' then
       install()
       return 'ok', 'Script installed'
     else
       return 'error', 'Usage: .. install'
     end
    end

Hopefully you will now have some nice idea for how you can modify your
own checks to return better data. And if you do make some modification
feel free to send them to me and I will add them to NSClient++.
