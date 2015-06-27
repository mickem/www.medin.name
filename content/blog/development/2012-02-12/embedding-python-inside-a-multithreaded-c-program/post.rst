Embedding Python inside a multithreaded C++ program
###################################################
:author: Michael Medin
:tags: boost, c++, python
:image: /images/python-powered.png
:social_image: /images/python-powered.png

This is a tutorial for how to embed python correctly inside a
multi threaded program. Python is a very neat language which is very
easy to embed inside C++ thanks to the boost::python library. But there
are some crucial parts which is missing from boost:python in regards to
how to manage GIL and thread state which I introduce here. Since this is
my first C++ tutorial I will include boost:thread as well as a quick
hello world application as well.

.. PELICAN_END_SUMMARY

Hello World
-----------

First I’d thought I d mention that the full source can be found on
`github <http://github.com/>`__ https://github.com/mickem/embed_python/.

Then since this is a project which uses
`CMake <http://www.cmake.org/>`__ figured I would start with a simple
Hello World in case you are not familiar with
`CMake <http://www.cmake.org/>`__.

First of all `CMake <http://www.cmake.org/>`__ is a tool which generates
Makefiles similary to automake so the actual build will be performed
with normal make. But `CMake <http://www.cmake.org/>`__ has the added
benefit of being able to also produce build files for Windows (Visual
Studio) as well as other tools and build systems. So for me beeing a
windows developer automake is not really an option.

The `CMake <http://www.cmake.org/>`__ build information resides in files
called CMakeLists.txt which you will find in each directory. Now this
post is not about `CMake <http://www.cmake.org/>`__ so I will not go
into details about this but to make sure “CMake” works make sure that
the project Hello World builds and works. At the end of the root
CMakeList.exe file you can edit which subdirectories are built so if you
run into issues feel free to comment out the latter ones to make sure
CMake is configured correctly.

.. code-block:: cmake

   ADD_SUBDIRECTORY(00_hello_world)
   ADD_SUBDIRECTORY(01_threads)
   ADD_SUBDIRECTORY(02_embed_python)
   ADD_SUBDIRECTORY(03_python_callins)
   ADD_SUBDIRECTORY(04_thread_safe)

If you are on Windows you also need to point CMake to your boost lib and
include folder as well as python this is done by setting options:

.. code-block:: cmake

   SET(BOOST_INCLUDEDIR "D:/source/include/boost-1_47" CACHE PATH "Path to boost includes")
   SET(BOOST_LIBRARYDIR "D:/source/lib/x64" CACHE PATH "Path to boost libraries")
   ...
   if(CMAKE_CL_64)
   MESSAGE(STATUS "Detected x64")
   SET(PYTHON_ROOT c:/python/27x64)
   ELSEIF(WIN32)
   MESSAGE(STATUS "Detected w32")
   SET(PYTHON_ROOT c:/python/27)
   ENDIF()

Looking at the source from Hello World we have two files
hello_world.hpp and hello_world.cpp. The first one merely has some
defines for this to compile on both windows and linux. The cpp file has
the usual “Hello World” sample.

.. code-block:: cpp

   #pragma once
   
   #include <iostream>
   
   #ifdef WIN32
   #define MAIN wmain
   typedef wchar_t unicode_char;
   #else
   #define MAIN main
   typedef char unicode_char;
   #endif
   
   #include "hello_world.hpp"
   
   int MAIN(int argc, const unicode_char\* argv[]) {
     std::cout << "Hello World\\n";
   }

Multithreaded
-------------

The first real step is to write a simple multi threaded C++ program
using boost. This will be in line with keeping it simple so this is a
very minimal multi threaded program.

We add a simple background thread and we start that in a series of
threads.

The thread has to do some work and for this rather simple sample we
simply wait a bit and then log a few messages in a loop.

.. code-block:: cpp

   void thread_proc(const int id, const int delay) {
     for (int i=0;i<thread_loops;i++) {
       boost::posix_time::millisec time_to_sleep(rand()\*delay/RAND_MAX);
       std::stringstream ss;
       ss << ">>> proc: " << id << "\\n";
       safe_cout << ss.str();
       boost::this_thread::sleep(time_to_sleep);
     }
   }

The other part we need is to start the threads which is done like so:

.. code-block:: cpp

   int MAIN(int argc, const unicode_char\* argv[]) {
     boost::thread_group threads;
     
     for (int i=0;i<thread_count;i++) {
       threads.create_thread(boost::bind(&thread_proc, i, 5));
     }
     
     safe_cout << "main: waiting for threads to join\\n";
     threads.join_all();
   }

Now the observing reader will notice that we have replaced
***std::cout*** with ***safe_cout***. This is a rather important step
as std::cout is not thread safe!

And this program uses multiple threads which means the console will
become gibberish if we do not replace cout with a thread safe
alternative. Unfonrtunetly our implementation is rather naïve so each
printed chunk will be thread safe but not the entire statements (this as
we protect the call to <<). TO work around this I am using a string
stream to first construct the string and the just print the output.

.. code-block:: cpp

   class logger {
     boost::recursive_mutex cout_guard;
     public:
     template <typename T>
     logger & operator << (const T & data){
       boost::lock_guard<boost::recursive_mutex> lock(cout_guard);
       std::cout << data;
       return \*this;
     }
   };
   logger safe_cout;

To see the code in its entirety go to the git hub project at
http://github.com/mickem/embed_python/tree/master/01_threads

Embedding Python
----------------

Now that we have a working multi threaded program we need to embed
python inside the program. Initially we will do so without using the
threads. Since I was using boost for threads I will also use boost for
Python but this is fairly straight forward so it should be easy enough
to adapt without boost. The first step is to expose our interface to the
python code. The interface we provide to Python is a function called
hello_cpp() contained inside a module called TEST.

.. code-block:: cpp

   void hello(int id) {
   std::cout << "hello_cpp(" << id << ")\\n";
   }
   
   BOOST_PYTHON_MODULE(TEST)
   {
   bp::def("hello_cpp", hello);
   }
   [/sourcecode]

Then we also need to load and initialize Python in our main procedure
like so. The second function is something generated for us by the
BOOST_PYTHON_MODULE macro.

.. code-block:: cpp

   Py_Initialize();
   initTEST();

And finally we need to run some Python code I have for simplicity opted
to include the actual Python snippet as a string in the C++ code. The
other thing we do here (apart from catching exceptions) is to populate a
copy of the global dictionary using a copy here is strictly not
necessary but normally I allow each script to have its own “context” and
then it is required to create isolation.

.. code-block:: cpp

   try {
     bp::object main_module = bp::import("__main__");
     bp::dict globalDict = bp::extract<bp::dict>(main_module.attr("__dict__"));
     bp::dict localDict = globalDict.copy();
     
     bp::object ignored = bp::exec(
    "from TEST import hello_cpp\\n"
    "\\n"
    "hello_cpp(1234)\\n"
    "\\n"
    , localDict, localDict);
   
   } catch(const bp::error_already_set &e) {
     std::cout << "Exception in script: ";
     print_py_error();
   } catch(const std::exception &e) {
     std::cout << "Exception in script: " << e.what() << "\\n";
   } catch(...) {
     std::cout << "Exception in script: UNKNOWN\\n";
   }

A final piece of the puzzle is to simply print errors from Python. To do
this I have implemented a catch bp::error_already_set for which in
turn calls a function print_py_error(); which prints the error to
stdout. Unfortunately the error_already_set exception does not out of
the box provide information from the Python script so we cant (as we
normally do) call the what() member function.

.. code-block:: cpp

   void print_py_error() {
     try {
       PyErr_Print();
       bp::object sys(bp::handle<>(PyImport_ImportModule("sys")));
       bp::object err = sys.attr("stderr");
       std::string err_text = bp::extract<std::string>(err.attr("getvalue")());
       std::cout << err_text << "\\n";
     } catch (...) {
       std::cout << "Failed to parse python error\\n";
     }
     PyErr_Clear();
   }

That pretty much sums up our python embedding which is very simple
thanks to boost::python. To see the code in its entirety go to the git
hub project at
http://github.com/mickem/embed_python/tree/master/02_embed_python

Calling Python from C++
-----------------------

Calling into Python from C++ is pretty straight forward as well what we
will do here is (again for simplicity) simply call a predefined function
called hello_python() from the C++ application. Adding this is very
simple we need two things a function exposed in our Python script.

.. code-block:: python

   from TEST import hello_cpp
   
   def hello_python(id):
     hello_cpp(id)

And then we just need to call that function.

.. code-block:: cpp

   void call_python(bp::dict &localDict, int id) {
     try {
       bp::object scriptFunction = bp::extract<bp::object>(localDict["hello_python"]);
       if(scriptFunction)
         scriptFunction(id);
       else
         std::cout << "Script did not have a hello function!\\n";
     } catch(const bp::error_already_set &e) {
       std::cout << "Exception in script: ";
       print_py_error();
     } catch(const std::exception &e) {
       std::cout << "Exception in script: " << e.what() << "\\n";
     } catch(...) {
       std::cout << "Exception in script: UNKNOWN\\n";
     }
   }

Simple enough right? Again much thanks to boost python which makes
everything simple and straight forward. I guess the most complicated
parts is the error handling |Ler| Next up is making this thread safe but
first feel free to review the code in its entirty at git hub
http://github.com/mickem/embed_python/tree/master/03_python_callins

Multi threaded Python: GIL
--------------------------

Python is unfortunately single threaded this means only a single thread
(ish) can access python at a given time. To manage this Python has
something called GIL: Global Interpreter Lock. This is something we need
to acquire when we enter python (and very importantly functions
accessing Python state). To manage this we are using a fairly common
`RAII <http://en.wikipedia.org/wiki/Resource_Acquisition_Is_Initialization>`__
concept by having a class to manage our state for us.

.. code-block:: cpp

   struct aquire_py_GIL {
     PyGILState_STATE state;
     aquire_py_GIL() {
       state = PyGILState_Ensure();
     }
     
     ~aquire_py_GIL() {
       PyGILState_Release(state);
     }
   };

This function use construction/destruction to manage the state
automatically meaning to use this all we need to do is define a variable
of this type.

.. code-block:: cpp

   try {
   aquire_py_GIL lock;
   ...
   ...
   }
   ...

The other thing we need to do is to release the GIL when we no longer
need it and I am not referring to after calling into Python (as that is
handled by our manager) I mean when Python leaves Python calling in to
C++. This means whenever the Python script calls a C++ function (which
takes time) we need to hand over GIL to whomever might need it. To help
we also have a similar function which does the reverse of the previous
function.

.. code-block:: cpp

   struct release_py_GIL {
     PyThreadState *state;
     release_py_GIL() {
       state = PyEval_SaveThread();
     }
     ~release_py_GIL() {
       PyEval_RestoreThread(state);
     }
   };

Then we need to switch all std::cout to use our safe_cout which we
introduced previously.  We also want to change our hello function to
actually pretend to do some work.

The resulting code for hello_cpp looks like this:

.. code-block:: cpp

   void hello(int id) {
     release_py_GIL unlocker;
     std::stringstream ss;
     ss << ">>> py: sleep: " << id << "\\n";
     safe_cout << ss.str();
     
     boost::this_thread::sleep(boost::posix_time::millisec(rand()\*delay/RAND_MAX));
   }

As you can see we have now added the ***release_py_GIL unlocker;*** to
allow other threads to call into python while we are “working”.

We have also done some minor but significant change in the
***call_python*** function.

.. code-block:: cpp

   void call_python(bp::dict &localDict, int id) {
     try {
       aquire_py_GIL lock;
       try {
         bp::object scriptFunction = bp::extract<bp::object>(localDict["hello_python"]);
         if(scriptFunction)
           scriptFunction(id);
         else
           safe_cout << "Script did not have a hello function!\\n";
       } catch(const bp::error_already_set &e) {
         safe_cout << "Exception in script: ";
         print_py_error();
       }
     } catch(const std::exception &e) {
       safe_cout << "Exception in script: " << e.what() << "\\n";
     }
   }

As we now have to aquire the GIL before we can access any Python related
functions we need to re-scope our error handling. This is important as
if we get a ***error_already_set*** we still require GIL to retrieve
the error message. The simplest way to achieve this is to have nested
catches.

The init code looks something like this:

.. code-block:: cpp

   int MAIN(int argc, const unicode_char\* argv[]) {
     Py_Initialize();
     PyEval_InitThreads();
     initTEST();
   
     try {
       bp::object main_module = bp::import("__main__");
       bp::dict globalDict = bp::extract<bp::dict>(main_module.attr("__dict__"));
       bp::dict localDict = globalDict.copy();
   
       try {
         bp::object ignored = bp::exec(
         "from TEST import hello_cpp\\n"
         "\\n"
         "def hello_python(id):\\n"
         " hello_cpp(id)\\n"
         "\\n"
         , localDict, localDict);
       } catch(const bp::error_already_set &e) {
         safe_cout << "Exception in script: ";
         print_py_error();
       }
   
       PyThreadState \*state = PyEval_SaveThread();
   
       boost::thread_group threads;
       for (int i=0;i<thread_count;i++)
       threads.create_thread(boost::bind(&thread_proc, i, localDict));
       safe_cout << ":::main: waiting for threads to join\\n";
       threads.join_all();
   
     } catch(const std::exception &e) {
       safe_cout << "Exception in script: " << e.what() << "\\n";
     }
   }

The main change from our previous attempt is the rescoping of the error
handling (again to accommodate GIL) as well as a very very important
often left out piece of the puzzle. Namely releasing GIL!

Once we have initialized Python we leave processing over to our threads
(the main thread which now own GIL has no further use for it) so we need
to release the GIL which we automatically receive when we start Python.
To do this we add the ***PyThreadState \*state =
PyEval_SaveThread();***. The actual value of the save state function is
not really necessary as we never intend to reacquire GIL in this thread.

Download the Source
-------------------

This is pretty much it. We now have a bi directional Python program
embedded in our multi threaded C++ program.

The full source can be found on `github <http://github.com/>`__
https://github.com/mickem/embed_python/.

.. |Ler| image:: /images/wlEmoticon-smile.png
