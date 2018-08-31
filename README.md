UPDATE 2018
-----------

The functionality of this has been integrated into the Socorro tooling now. 
Please read https://socorro.readthedocs.io/en/latest/howto.html#reprocess-crashes instead if you want to reprocess a bunch of Socorro crashes.

---

Script to help when you use [SuperSearch](https://crash-stats.mozilla.com/search/?product=Firefox&_dont_run=1)
and want to send the found crashes in for reprocessing.


Installation
------------

Download, then install the stuff in `requirements.txt`

Run
---

For example...

```
python main.py -t 32729936d2b94640bb2039b33ceadb61 \
 "https://crash-stats.mozilla.com/search/?product=FennecAndroid&build_id=20160610073607&platform=Android&date=%3E%3D2016-06-10&release_channel=nightly&_facets=signature&_columns=date&_columns=signature&_columns=product&_columns=version&_columns=build_id&_columns=platform#crash-reports"
```

You can type multiple URLs. Basically multiple SuperSearch queries.
