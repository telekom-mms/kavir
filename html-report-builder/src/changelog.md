# Changelog

All notable changes to this component will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 2.0.0

### Added

* support for docker `kavir:1.1.0`

### Changed

* templating engine from `domintate` to `Jinja2`
  * The report is now built by using a template file
  * Added a `templates/` folder to store Jinja2 template files
* Structure of `config.json.template`
* Moved scope of included resources from `main.py` to `config.json.template`

## 1.1.0

### Added

* Info log to indicate that the html report was built successfully
* Examples for docker and html-report-builder

### Changed

* Debug log output now uses the `[DEBUG]` tag instead of the `[INFO]` tag
* Minor improvements of the structure of the html report
* Added a `styles/` folder to store css files
  * Moved `style.css` to `styles/simple.css`
* Minor changes in `styles/simple.css`

## 1.0.0

Initial version
