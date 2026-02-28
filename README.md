# Extractor: Contextual Password Profiler

A Python-based reconnaissance tool that scrapes target websites to generate highly contextual, customized wordlists. 

During penetration testing, generic password dictionaries often fail against targets who use company-specific terminology (e.g., product names, local landmarks, corporate slogans). **Extractor** solves this by crawling a target's public-facing infrastructure, extracting the most frequently used terminology, and automatically mutating those terms into common password formats.

## Features

* **Intelligent Web Crawling:** Uses Breadth-First Search (BFS) to crawl links up to a specified depth.
* **Scope Protection:** Automatically parses domains to ensure the crawler never accidentally leaves the target's primary infrastructure (in-scope only).
* **Length Filtering:** Drops useless short words (e.g., "a", "the", "is") by enforcing a minimum character limit.
* **Mutation Engine:** Automatically generates common password variants (e.g., `company` -> `Company!`, `COMPANY2026`, `Company123`).
* **Frequency Sorting:** Prioritizes words based on how frequently they appear on the target site.



