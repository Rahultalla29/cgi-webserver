import gzip

fp = open("cgi_gzip_test_expected.in", "rb").read()

original = open("cgi_gzip_test_expected.out", "r").read()

if gzip.decompress(fp).decode("utf-8") == original :
    print("Successful decompression of file (matches compressed sent file)")
else :
    print ("decompression of sent file failed")