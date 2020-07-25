=======
stowage
=======

Stowage is a symlink farm manager, similar to `GNU Stow`__.

.. __: https://www.gnu.org/software/stow/

Why?
====

To simplify my dotfile management and to allow me to use multiple dotfile
repositories, I wanted to move to something like GNU Stow. The problem is that
I wanted something (a) standalone, (b) that didn't require compilation, (c)
didn't use any GNU-isms or depend on bash, and (d) would allow me to exclude
certain files. Stow itself fulfilled all of these except for the first one,
and all the alternatives fell down in some way. Given every machine I use has
Python installed by default or typically gets installed pretty quickly,
writing something that did the job in Python seemed like a good idea.

Symlink farms
=============

A symlink farm is a directory hierarchy consisting of symlinks to files
elsewhere. You can think of it as a kind of primitive package management tool.
For instance, say you had a bunch of directories like the following::

    packages
    +- thingy-0.5
    |  +- bin
    |  |  +- thingyctl
    |  |  +- thingyd
    |  +- man
    |     +- man8
    |        +- thingyctl.8
    |        +- thingyd.8
    +- foobar-2.6
       +- bin
       |  +- foobar
       +- man
          +- man1
             +- foobar.1

And you wanted to combine that into a single hierarchy under the `everything`
directory. To do so with stowage, you'd issue the following command::

    stowage --target everything packages/*

That would walk the contents of all the subdirectories of `packages`, create
a common directory hierarchy, and symlink all the files back, giving you a
directory structure like so::

    everything
    +- bin
    |  +- foobar
    |  +- thingyctl
    |  +- thingyd
    +- man
       +- man1
       |  +- foobar.1
       +- man8
          +- thingyctl.8
          +- thingyd.8

There are no regular files here, just symlinks back to the files under the
various package directories.

Uninstalling is similar, but you pass the `--uninstall` flag. For instance, to
remove anything pointing to the contents of the `foobar-2.6` package from
the symlink farm, you'd issue the following::

    stowage --uninstall --target everything packages/foobar-2.6

Further help
============

Use the `--help` flag to get a list of all flags.

To do
=====

* Currently exclusions only work with files, but ought to work with
  directories too.

.. vim:set ft=rst:
