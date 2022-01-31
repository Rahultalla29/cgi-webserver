import gzip

fp = open("gzip_test_js_expected.out", "rb").read()

original = open("js_gzip_test.js", "r").read()

if gzip.decompress(fp).decode("utf-8") == original :
    print("Successful decompression of file (matches compressed sent file)")
else :
    print ("decompression of sent file failed")