# async_translate


Multi-provider async translate API

## Why?
Most translate APIs work on one backend (usually Google Translate), and few are fully asynchronous.

I wanted a translate API that uses `async` and `await`, and I wanted to be able to use multiple providers without having
to deal with their different APIs.
 
I built this to use with my Discord bot, [Mr. Translate](https://docs.mrtranslate.xyz).


## Installation
**Currently this uses Python 3.8 specific features. See [ROADMAP.md](ROADMAP.md)**
 
Install with `pip install -U async-translate`.

## Optional Default Providers
A few providers are baked into this package. You can install them with:
* [Azure Cognitive Services][azure] `pip install -U async-translate[azure]`
* [Google Translate][google] `pip install -U async-translate[google]`

## Custom Providers
See [CUSTOM_PROVIDERS.md](async_translate/providers/CUSTOM_PROVIDERS.md) on making your own providers.

Feel free to contribute back to the project with a pull request containing code for other providers.

## Sample Usage
See [sample.py](sample.py) for basic sample usage


[azure]: https://azure.microsoft.com/en-us/services/cognitive-services/translator/
[google]: https://cloud.google.com/translate