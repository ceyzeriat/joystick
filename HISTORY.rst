0.3.1 (2016-11-29)
++++++++++++++++++

- fixed bug: cmap of scatter
- added taking into account scatter kwargs
- fixed bug: xnptsmax cannot be smaller than xnpts
- changed default value of xylim for graph, multigraph and scatter frames to (None, None, None, None)
- fixed bug: xylim auto-determination when no data is on the graph
- 

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
