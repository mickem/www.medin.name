Unit test your monitoring: Introducing unit tests in Python for NSClient++
##########################################################################
:date: 2011-10-23 21:28
:author: Michael Medin
:category: Monitoring
:tags: monitoring, NSCP, python, unit test
:slug: creating-nsclient-unit-tests-in-python
:image: /images/thumbnails/400x-/image6.png
:social_image: /images/thumbnails/400x-/image6.png

One of the new features of the up-coming NSClient++ 0.4.0 will be Python
scripting support. The main reason for me to include Python script
(apart from the coolness factor) is to write unit tests. Writing unit
test for a monitoring agent with a C++ unit test kit is pretty difficult
but more importantly not very productive. The main feature of an agent
is to interact with the system and thus you need to know about the
system to be able to test it (or mock the system which is tedious at
best).

.. PELICAN_END_SUMMARY

So how does the unit tests work and, perhaps more importantly, why
should you care?

Well, where as I write unit tests to see if NSClient++ is working you
should want to test if your monitoring is working. In essence it would
really suck if you spent hours and hours to configure and setup your
monitoring only to discover when some thing broke that it was in fact
not setup correctly. So a good idea is to write unit tests to make sure
your monitoring is actually working.

So how does the unit test framework in NSClient++ work? Well it is
fairly straight forward as long as you understand some basic Python.

In this series (this is the first part) I will introduce how to write
unit tests in Python and how to make sure your monitoring is actually
working (before it breaks). As this is a work in progress the various
topics are not nailed down but the over all idea is something like this:

#. Unit test your monitoring: Introducing unit tests in Python for
   NSClient++
   Where we learn how to get started with the unit test framework.
#. Unit test your monitoring: Write your first real unit test
   Where we learn how to write a useful test which actually tests
   something.
#. Unit test your monitoring: Breaking (or faking) your system
   How you can create event log messages, files, or fake system load?
#. ?

Writing a test
==============

So lets start what is the minimum effort required to get a unit test
setup and installed in NSClient++?

.. code-block:: python

     from test\_helper import BasicTest, TestResult, setup\_singleton,
    install\_testcases, init\_testcases, shutdown\_testcases
    
    .. raw:: html
    
       </p>
    
    class SampleTest(BasicTest):
     pass
    
    setup\_singleton(SampleTest)
    
    all\_tests = [SampleTest]
    
    def \_\_main\_\_():
     install\_testcases(all\_tests)
    
    def init(plugin\_id, plugin\_alias, script\_alias):
     init\_testcases(plugin\_id, plugin\_alias, script\_alias, all\_tests)
    
    def shutdown():
     shutdown\_testcases()
    >THE END<

Now this is not to bad right?

Going through the code briefly we have:

-  [1] Import some random stuff we need from the unit test framework
-  [3-4] Create a dummy unit test (this is where we will expand and
   include the actual test later on).
-  [6] This creates a singleton from our test case since the plugin
   might be called from various ends it is important to use single ton
   patterns or else a message might end up being sent to the “wrong”
   test.
-  [8] Here we define all test instances in this file (not required but
   I think it is a neat way to have them all in one place)
-  [10-11] This is the main function called when the script is executed
   from command line. Here we normally want to install the test script
   (which is what we do here)
-  [13-14] The init function is called when the script is executed from
   NSCP and here we want to setup our unit test so we call the framework
   asking it to add and initialize our test case.
-  [16-17] When NSCP is finished this function is called so we can
   un-initialize all resources just relay this on to the test framework.

Installing a test
=================

One of the nice features of using the framework for writing your unit
tests is that you get install automagically (and eventually uninstall as
well). This is done when we call the install wrapper on line 11 above.
So how do we call the script on command line?

Well the rather complicated way to do this now is:

.. code-block:: text

    nscp --client --module PythonScript --command run --script test_sample

This will be prettified eventually but for now all these arguments are
required so lets try to explain them quickly to see if it makes sense.

-  --client
   Means we run in client mode (in other words don’t actually start
   NSClient++ just utilize some offline features)
-  --module
   Not strictly required but makes it simpler for NSClient++. This
   tells NSClient++ which plugin to load.
-  --command run
   This is the command to execute on the module in question. In this
   case tell “PytonScript” to execute “run”.
-  --script <script>
   This is the actual script we want to load. The path is magically
   added by the module (which in turn will look inside various folders).

So it was not quite as complicated as it seemed right? Well it is far to
complicated and it is on my TODO list so eventually you will most likely
have something along the lines of nscp_client –script test_sample.py
but for now we are stuck with the long version.

What this chunk does is add a few lines to the nsclient.ini file (or
whatever settings store you are using).

.. code-block:: text

    [/modules]

    pytest = PythonScript

    [/settings/pytest/scripts]

    ; UNIT TEST SCRIPT: SampleTest - A script for running unittests for: TODO: Describe: SampleTest
    test_sample = test_sample.py

Running a test
==============

So all that is left is actually running the test right?

Well, this is straight forward enough just start NSClient++ in test mode
like so:

.. code-block:: text

    nscp --test

Once that is don we run the following command ***py_unittest***.

Which yield the following:

.. code-block:: text

    py_unittest
    e \modules\PythonScript\script_wrapper.cpp:120  ERROR: Running suite: SampleTest (None)
    e \modules\PythonScript\script_wrapper.cpp:120    ERROR: TODO add implementation (None)
    l \modules\PythonScript\script_wrapper.cpp:113  ERROR: 0 of 2 test(s) succedded (2 failed)
    l rce\nscp\trunk\service\simple_client.hpp:12   CRITICAL:ERROR: 2/2 test(s) failed

So that’s pretty nice… all test failing (as we haven’t actually written
one). But hopefully you get the idea. It is pretty damn simple to write
unit tests in Python.

Thus ends this installment of this series and although it is not nailed
down the general topic ideas for the next few installments are:

#. Unit test your monitoring: Introducing unit tests in Python for
   NSClient++
   Where we learn how to get started with the unit test framework.
#. Unit test your monitoring: Write your first real unit test
   Where we learn how to write a useful test which actually tests
   something.
#. Unit test your monitoring: Breaking (or faking) your system
   How you can create event log messages, files, or fake system load?
#. ???

