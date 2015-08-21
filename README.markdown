# Laptop-Watchman

A fork of the watchman file-monitoring service optimized for laptops.

## Differences from facebook/watchman

- Secure management of state directory

- Better energy efficiency: no sub-second-frequency wakeups when there
  is nothing to do

## Purpose

Watchman exists to watch files and record when they actually change.  It can
also trigger actions (such as rebuilding assets) when matching files change.

## License

Watchman is made available under the terms of the Apache License 2.0.  See the
LICENSE file that accompanies this distribution for the full text of the
license.
