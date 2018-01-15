# Napster with RethinkDB backend

An implementation of Napster p2p system with RethinkDB backend.
This implementation is used for an exercise of System Engineering 1 course at TU Dresden (https://tu-dresden.de/ing/informatik/sya/se/studium/lehrveranstaltungen/winter-semester/systems_engineering_1)

### How to run ###

1. Start RethinkDB at Indexing Server:

    $ rethinkdb

2. Start Napster Indexing Server:

    $ python3 server.py

3. Start Napster Peers to upload/dowload shared files:

    $ python3 client-up.py

    $ python3 client-down.py
    
