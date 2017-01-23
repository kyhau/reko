from reko.cachestore import CacheStore


def test_cachestore():
    cs = CacheStore()
    assert cs.get_filename("Sorry! I'm not able to identify you!") == "sorryimnotabletoidentifyyou"