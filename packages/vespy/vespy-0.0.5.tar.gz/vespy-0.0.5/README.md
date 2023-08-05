Repository for various utility functions specific to Vestas.

## SSLError

If you encounter an SSLError from within Vestas firewalls, chances are that you haven't added the proper certificates. You can do that like this,

    from vespy import fix_ssl_error
    fix_ssl_error()




