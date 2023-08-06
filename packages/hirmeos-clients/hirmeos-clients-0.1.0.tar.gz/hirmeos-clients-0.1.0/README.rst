HIRMEOS Clients
===============

Python clients for interacting with APIs that were developed as part of the
HIRMEOS project.

Once this has been shown to be working properly, and able to integrate with the
HIRMEOS drivers it can be moved to a HIRMEOS/OPERAS PyPI Repo.


Until CI is ready
-----------------
  .. code-block:: bash

    $ python3 setup.py sdist bdist_wheel
    $ twine upload dist/*


Note: We are still in the early stages of this project so there will be many
breaking changes as we go along.

Release Notes:
==============

[0.1.0] - 2021-02-02
---------------------

Added:
 - Unit Tests for Translator Client
 - Translator Client attributes: `remove_uri_trailing_slash` &
   `use_lower_case_uris`. These automatically format URIs for consistency.


[0.0.20] - 2021-01-26
---------------------
Changed:
 - TokenClient Bug Fix: Check encoded token type before attempting to decode.


[0.0.19] - 2021-01-26
---------------------
Changed:
 - TokenClient Code Change: Separate token encode and decode steps (for
   debugging).


[0.0.18] - 2020-07-30
---------------------
Changed:
 - TokenClient Bug Fix: Correctly update request header after refreshing token.


[0.0.17] - 2020-07-29
---------------------
Changed:
 - TokenClient: update request header after refreshing token, and before
   retrying request.


[0.0.16] - 2020-07-29
---------------------
Changed:
 - TokenClient: When creating token, convert from bytes to a string.


[0.0.15] - 2020-07-29
---------------------
Changed:
 - TranslatorClient.work_exists: Report all content from the translation API
   response when this method fails (investigation).


[0.0.14] - 2020-07-29
---------------------
Changed:
 - TranslatorClient.work_exists: Report 'data' content from the translation API
   when this method fails (investigation).


[0.0.13] - 2020-07-27
---------------------
Added
 - Token creation option: The TokenClient can now also be used to create a
   token, based on the logic used by the Tokens API.


[0.0.12] - 2020-05-20
---------------------
Added
 - New client: AltmetricsClient


[0.0.11] - 2020-04-15
---------------------
Changed
 - TranslatorClient.prepare_uri: Now returns the URI as a string in the format
   expected by TranslatorClient.get_work_uris. 


[0.0.10] - 2020-04-15
---------------------
Changed
 - TranslatorClient.post_new_work: 'uris' parameter now assumes the same format
   as the output from TranslatorClient.get_work_uris, which was causing errors.
   (bug fix)


[0.0.9] - 2020-04-06
---------------------
Added
 - translator: Reference variables for work types and URI schemes.
 - translator: Check if a work exists.
 - translator: Fetch all URIs associated with a work.
 - translator: Post new work.


[0.0.8] - 2020-03-06
---------------------
Changed
 - Make requirements for flexible to avoid conflicts with other packages.


[0.0.7] - 2020-03-06
---------------------

Added
 - Release notes

Changed
 - Strip trailing slash from TranslatorClient API base.
