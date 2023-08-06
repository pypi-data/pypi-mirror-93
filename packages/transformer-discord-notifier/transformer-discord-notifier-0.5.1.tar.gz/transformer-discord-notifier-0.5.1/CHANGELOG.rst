
Changelog
=========

0.x.0 (WIP)
-----------

* ignore linkcheck with version tag (if tags have not been pushed it will fail)
* Blocking message deletion?

0.5.0 (2021-02-04)
------------------

* Add dynamic experiment channel creation.
* TODO: update docs and tests with better examples for experiment channels.

0.4.5 (2021-02-04)
------------------

* Wrap common errors, like 5xx Discord Gateway errors, to allow uninterrupted training.
* Add python3.10 to tests / github workflows.

0.4.4 (2020-12-22)
------------------

* Github Actions - tox tests

0.4.3 (2020-12-18)
------------------

* Github Actions - pypi publishing

0.4.2 (2020-12-18)
------------------

* Add travis build jobs.
* Add coveralls coverage statistics.

0.4.1 (2020-12-17)
------------------

* Reintroduce tests with ``pytest`` and ``tox``.
* Add simple tests for :class:`~transformer_discord_notifier.discord.DiscordClient`.
* Add tests for :class:`~transformer_discord_notifier.transformers.DiscordProgressCallback`.

0.3.1 (2020-12-17)
------------------

* Let Discord bot gracefully handle initialization failures.
* Let transformer callback handler handle invalid configs gracefully, to simply exit.
* Better handling of edge cases of Discord client login.

0.3.0 (2020-12-16)
------------------

* Add (private) scripts (make venv, run checks).
* Update usage docs.
* Extend / rewrite discord client methods.
* Reuse existing ``tqdm`` :class:`transformers.trainer_callback.ProgressCallback` for progress tracking.
* Fancy aggregation of prediction runs, split train progress into epochs.

0.2.1 (2020-12-15)
------------------

* Correct ``setup.py`` validation.
* Add (private) distribution/docs build scripts.

0.2.0 (2020-12-15)
------------------

* Refactor blocking discord code into :mod:`~transformer_discord_notifier.discord` submodule.
* Fix behaviour for ``__del__`` with refactoring, so it work as intended.
* Improve documentation for :mod:`~transformer_discord_notifier.discord` module.

0.1.0 (2020-12-11)
------------------

* First release on PyPI.
* First working version, tested manually.
* Cleaned up skeleton files.
* Updated docs.

0.0.0 (2020-12-10)
------------------

* Initial code skeleton.
