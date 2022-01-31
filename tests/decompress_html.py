import gzip

fp = open("gzip_test_html_expected.out", "rb").read()

original = open("greetingsGzip.html", "r").read()

if gzip.decompress(fp).decode("utf-8") == original :
    print("Successful decompression of file (matches compressed sent file)")
else :
    print ("decompression of sent file failed")