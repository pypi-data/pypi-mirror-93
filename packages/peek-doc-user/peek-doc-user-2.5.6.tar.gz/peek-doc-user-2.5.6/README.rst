================================
Peek Platform - User Doc Service
================================

The Peek User Doc service contains the user documentation container.

User documentation from other plugins are linked in to this container, this will be
RST text files and images.

A sphinx build is then run to generate the HTML and PDF documentation

Manual Builds
-------------

Builds are performed by either the peek-client or peek-server service much the same way
the builds are performed for the mobile-web frontends.

Manual builds can be performed by running the following :

::

        cd <project dir>/peek_doc_user
        build_html_docs.sh

