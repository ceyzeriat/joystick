0.3.6 (2017-12-21)
++++++++++++++++++

- Fix AttributeError on set_facecolor for old version of matplotlib
- Added savefig to graphs, pointing to matplotlib.figure.Figure.savefig
- Added deprecation warnings
- Refactored colorbar related code (image and scatter frames)


0.3.4 (2017-05-27)
++++++++++++++++++

- Deprecation warning matplotlib
- Fixed bug GraphMulti when legend=False
- Added centerorig argument in Image


0.3.2 (2017-05-23)
++++++++++++++++++

- Removed the usage of "_init" and "_update"
- GraphMulti numbering shows labels if lbls is not None


0.3.1 (2016-11-29)
++++++++++++++++++

- fixed bug: increased interactivity on graphs when not running
- fixed bug on xylim of graph, multigraph and scatter


0.3.0 (2016-11-28)
++++++++++++++++++

- Added multi-lines graph-frames
- Added scatter grap-frames
- Deprecated the usage of "_init" and "_update"
- Added new decorator "callit" to define callback or callfront functions to an existing method
- Added new decorator "thread_it" to launch a function into a separate thread
- Added the possibility to use ax-related kwargs in all graph-frames
- Allowed xnpts and xnptsmax = None to apply no limit on the amount data plotted


0.1.4 (2016-10-14)
++++++++++++++++++

- Added image frames
- Added auto scroll-down on a text-frame when showing text in chronological order (rev=False)


0.1.0 (2016-09-26)
++++++++++++++++++

- Initial release
