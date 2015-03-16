This is `rdostats`, a tool used to generate summaries of open bugs for
[RDO][].

[RDO]: http://rdoproject.org/


## Usage

To fetch a report from Bugzilla:

    rdostats fetch

To generate a report:

    rdostats generate

## Configuration

Configuration is via a YAML file (deafults to `rdostats.yml`).  For
example:

    # This tells rdostats where to find things.
    basedir: ./output
    templatedir: ./templates

    # This tells rdostats where to connect
    bugzilla:
      url: "https://bugzilla.redhat.com"
      product: RDO

    # This is a dictionary of arbitarary key/value attributes
    # that will be provided to templates.
    report_attributes:
      base_url: http://people.redhat.com/~lkellogg/rdo

