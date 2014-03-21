# Livefyre Python Utility Classes
[![PyPI version](https://badge.fury.io/py/livefyre.png)](http://badge.fury.io/py/livefyre)

Livefyre's official library for common server-side tasks necessary for getting Livefyre apps (comments, reviews, etc.) working on your website.

Works with Python versions: 2.6, 2.7, 3.2, 3.3

## Installation

    pip install livefyre

## Usage

Creating tokens:

**Livefyre token:**
    
    network = Livefyre.get_network(network_name, network_key)
    network.build_user_auth_token()

**User auth token:**

    network = Livefyre.get_network(network_name, network_key)
    network.build_user_auth_token(user_id, display_name, expires)

**Collection meta token:**

    network = Livefyre.get_network(network_name, network_key)

    site = network.get_site(site_id, site_key)
    site.build_collection_meta_token(title, article_id, url, tags)

To validate a Livefyre token:

    network = Livefyre.get_network(network_name, network_key)
    network.validate_livefyre_token(token)

To send Livefyre a user sync url and then have Livefyre pull user data from that url:

    network = Livefyre.get_network(network_name, network_key)
    
    network.set_user_sync_url('http://thisisa.test.url/{id}/'')
    network.sync_user(system)
        
To retrieve content collection data as a tuple:

    network = Livefyre.get_network(network_name, network_key)
    
    site = network.get_site(site_id, site_key)
    site.get_collection_content(article_id)

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request

Note: any feature update on any of Livefyre's libraries will need to be reflected on all libraries. We will try and accommodate when we find a request useful, but please be aware of the time it may take.

## License

MIT