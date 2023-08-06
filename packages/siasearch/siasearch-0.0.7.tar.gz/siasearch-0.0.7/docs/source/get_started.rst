Get started
===========

To get connect to SiaSearch platform you need first to authorise yourself and create a "central" :class:`.SiaSearch`
object:

    >>> from siasearch import SiaSearch
    >>> sia = SiaSearch.login("http://custom-domain.siasearch.de", "user@example.com", "password")
    <SiaSearch object with user `user@example.com` connected to `http://custom-domain.siasearch.de`>

And then you can fetch the information about the columns that are queryable:

    >>> cols = sia.columns()
    >>> cols
    <Columns object containing columns: ['acceleration_level', 'curved_trajectory', 'dataset_name', 'forward_velocity',...
    >>> cols.curved_trajectory.levels
    ["'LEFT_BEND'", "'NO_BEND'", "'RIGHT_BEND'"]

and query them to get the resulting sequences:

    >>> query = sia.query("dataset_name = 'kitti' AND curved_trajectory = 'LEFT_BEND'")
    Query("dataset_name = 'kitti' AND curved_trajectory = 'LEFT_BEND'")
    >>> sequences = query.all()
    >>> sequences
    <Sequences class with 54 segments>
