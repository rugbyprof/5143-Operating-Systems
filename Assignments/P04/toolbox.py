import gzip


def compress(string_to_compress):
    """Compress a string using gzip compression."""
    compressed_data = gzip.compress(string_to_compress.encode())
    return compressed_data


def decompress(string_to_decompress):
    # Decompress the string
    decompressed_data = gzip.decompress(string_to_decompress)

    # Convert the decompressed data back to a string
    decompressed_string = decompressed_data.decode()

    return decompressed_string


def mykwargs(argv):
    """
    Processes argv list into plain args and kwargs.
    Just easier than using a library like argparse for small things.
    Example:
        python file.py arg1 arg2 arg3=val1 arg4=val2 -arg5 -arg6 --arg7
        Would create:
            args[arg1, arg2, -arg5, -arg6, --arg7]
            kargs{arg3 : val1, arg4 : val2}

        Params with dashes (flags) can now be processed seperately
    Shortfalls:
        spaces between k=v would result in bad params
    Returns:
        tuple  (args,kargs)
    """
    args = []
    kargs = {}

    for arg in argv:
        if "=" in arg:
            key, val = arg.split("=")
            kargs[key] = val
        else:
            args.append(arg)
    return args, kargs
