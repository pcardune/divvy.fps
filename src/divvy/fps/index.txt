=============
``divvy.fps``
=============

Welcome to the **divvy.fps** documentation site.

**divvy.fps** is a python library for integrating your website with
Amazon's Flexible Payment Service (FPS).  The project is brand new and
currently under heavy development.  The initial goal of divvy.fps is
to support the FPS "Basic Quick Start" API in it's entirety.  It would
be great if eventually divvy.fps supported the entire Amazon FPS API.

If you would like to help in the
development of divvy.fps, read the Getting Started section.


Getting Started
===============

Here are the steps you need to get a development environment set up
for divvy.fps:

#. Grab the source code from the mainline git repository::

     $ git clone git://github.com/pcardune/divvy.fps.git
     $ cd divvy.fps

#. Run the bootstrap.py script to get the development environment
   setup::

     $ python bootstrap.py

#. Run buildout to download the depencies and setup the test scripts::

     $ ./bin/buildout

#. Run the tests::

     $ ./bin/test


Get in Touch
============

Join us on **#divvyshot** at **irc.freenode.net** to chat about **divvy.fps** or
send Paul an email at paul@divvyshot.com.


Read the Documentation
======================

.. toctree::
   :maxdepth: 2

   README
