import petl

from .metadataheaders import parse_metadata_header



def fromcsvwithheader(source, **kwargs):
    """
    Call `petl.fromcsv` and automatically parse metadata header if present.
    """
    # preliminary open for inspection
    rawtable = petl.fromcsv(source, header=None, **kwargs)
    metadata, header, data = parse_metadata_header(rawtable)

    # transfer data to a in-memory data buffer
    databuffer = petl.MemorySource()
    petl.tocsv(data, databuffer, write_header=False, encoding='utf-8')
    databuffer.s = databuffer.getvalue()

    # re-open with right headers and add metadata
    table = petl.fromcsv(databuffer, header=header)
    table.metadata = metadata

    return table

