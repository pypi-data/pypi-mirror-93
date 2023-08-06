NeuroMMSig Epilepsy
===================
Mechanistic pathway knowledge on Epilepsy encoded in Biological Expression
Language.

Installation
------------
To install the ``neurommsig_epilepsy`` python package for programmatic access
to the BEL files in this repository, use the following code in your shell:

.. code-block:: sh

    $ pip install neurommsig_epilepsy

To install the ``neurommsig_epilepsy`` python package for programmatic access
to the BEL files in this repository, use the following code in your shell:

.. code-block:: sh

    $ git clone https://github.com/neurommsig-epilepsy/neurommsig-epilepsy.git
    $ cd neurommsig_epilepsy
    $ pip install -e .

To optionally re-compile all of the BEL files, use

.. code-block:: sh

    $ neurommsig-epilepsy compile

Usage
-----
To get the knowledge and summarize it, use:

.. code-block:: python

    import neurommsig_epilepsy

    graph = neurommsig_epilepsy.get_graph()
    graph.summarize()
