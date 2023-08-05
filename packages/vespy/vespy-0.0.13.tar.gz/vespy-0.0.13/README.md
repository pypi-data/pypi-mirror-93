# vespy

Repository for various Vestas utility functions. It can be installed via pypi,

    pip install vespy

## SSLError

If you encounter an SSLError from within Vestas firewalls, chances are that you haven't added the proper certificates. With vespy, you can do it like this

    vespy --fix-ssl

Alternatively, you can invoke the fix from within python (e.g. in your own library),

    from vespy import fix_ssl_error
    fix_ssl_error()



