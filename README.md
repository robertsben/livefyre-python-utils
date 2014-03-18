Livefyre Python Utility Classes
===============================

Works with Python versions: 2.6, 2.7, 3.2, 3.3

Installation
============

    pip install livefyre

Usage
=====

Creating tokens:

**User auth token:**

    Network('networkname', 'networkkey').build_user_auth_token('userid', 'displayname', 'timetillexpire')

**Collection meta token:**

    network = Network('networkname', 'networkkey')
    network.get_site('siteid', 'sitekey').build_collection_token('title', 'articleid', 'url', 'tags')


To validate a Livefyre token:

    Network('networkname', 'networkkey').validate_livefyre_token('token')


To send Livefyre a user sync url and then have Livefyre pull user data from that url:

    network = Network('networkname', 'networkkey')
    
    network.set_user_sync_url('http://thisisa.test.url/{id}/')
    network.sync_user('system')

        
To retrieve content collection data as a string and json object from Livefyre (note that both are in JSON, but the latter is encapsulated in a JsonObject):

    site = Network('networkname', 'networkkey').get_site('siteid', 'sitesecret')
    content = site.get_collection_content(articleid)

License
=======

MIT