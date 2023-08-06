# wynncraft-python

A wrapper for the Wynncraft API, with local caching.

# Install
Needs at least python 3.6

    pip install wynncraft

# Example

    import wynncraft
    
    # Get guild list
    guilds = wynncraft.Guild.list()
    print(guilds)
    
    # Get guild list from cache.
    # If it hasn't been cached, it will make a request.
    for _ in range(100):
	    guilds = wynncraft.cache.Guild.list()
	    print(guilds)
